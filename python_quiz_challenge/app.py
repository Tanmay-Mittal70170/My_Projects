import os
import re
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
QUESTIONS_FILE = os.path.join(BASE_DIR, "questions.txt")
SCORES_FILE = os.path.join(BASE_DIR, "quiz_scores.txt")

DEFAULT_KEYS = {
    1: ("A", "The first inner loop prints (5 - i) spaces, centering the stars into a pyramid."),
    2: ("D", "grades.update(...) modifies the dict in-place and returns None. Calling .get() on None raises an AttributeError."),
    3: ("B", "Default mutable list cart=[] is created once at function definition and shared across calls."),
    4: ("C", "Assigning 'score = score + 5' inside the function makes 'score' local before it is defined, raising UnboundLocalError."),
    5: ("B", "The for-loop variable 'i' remains in scope after the loop finishes with its last value from range(3), which is 2."),
    6: ("A", "The return statement exits the function immediately upon hitting the first even number (2).")
}

game_state = {}

def load_questions_from_file():
    """Parses 'Question X.' blocks without EVER deleting leading pattern spaces."""
    questions = []
    target_file = QUESTIONS_FILE
    if not os.path.exists(target_file) and os.path.exists(target_file + ".txt"):
        target_file = target_file + ".txt"

    if not os.path.exists(target_file):
        print(f"[ERROR] File not found: {QUESTIONS_FILE}")
        return questions

    with open(target_file, "r", encoding="utf-8") as file:
        content = file.read().replace("\u00a0", " ").replace("\t", "    ")

    raw_blocks = re.split(r'(?m)^(?=\s*Question\s+\d+)', content, flags=re.IGNORECASE)
    blocks = [b.strip() for b in raw_blocks if b.strip()]

    for idx, block in enumerate(blocks, start=1):
        lines = block.splitlines()
        lines[0] = re.sub(r'^\s*Question\s+\d+\s*[\.\:]?\s*', '', lines[0], flags=re.IGNORECASE)

        q_lines = []
        options = {"A": [], "B": [], "C": [], "D": []}
        current_opt = None
        ans_key = None
        exp_text = None

        for line in lines:
            stripped = line.strip()
            upper = stripped.upper()

            if upper.startswith(("ANSWER:", "ANS:")):
                ans_key = stripped.split(":", 1)[1].strip().upper()[:1]
                current_opt = "DONE"
                continue
            elif upper.startswith(("EXPLANATION:", "EXP:")):
                exp_text = stripped.split(":", 1)[1].strip()
                current_opt = "EXP"
                continue

            # Match A., B., C., D. at start of line
            opt_match = re.match(r'^\s*([A-D])[\.\)]\s?(.*)', line)
            if opt_match and current_opt not in ("DONE", "EXP"):
                current_opt = opt_match.group(1)
                first_opt_line = opt_match.group(2).rstrip()
                # If 'A.' is on its own line, don't append an empty first line
                if first_opt_line.strip() != "":
                    options[current_opt].append(first_opt_line)
            else:
                if current_opt in ("A", "B", "C", "D"):
                    # Keep the EXACT line spaces as written in questions.txt!
                    options[current_opt].append(line.rstrip())
                elif current_opt == "EXP":
                    exp_text += " " + stripped
                elif current_opt is None:
                    q_lines.append(line.rstrip())

        # Remove only empty top/bottom lines inside options, keeping all pattern spaces intact
        cleaned_options = {}
        for k, v in options.items():
            while v and not v[0].strip():
                v.pop(0)
            while v and not v[-1].strip():
                v.pop()
            cleaned_options[k] = "\n".join(v)

        default_ans, default_exp = DEFAULT_KEYS.get(idx, ("A", "Explained by Quizmaster."))
        questions.append({
            "id": idx,
            "question": "\n".join(q_lines).strip(),
            "options": cleaned_options,
            "answer": ans_key if ans_key else default_ans,
            "explanation": exp_text if exp_text else default_exp
        })

    print(f"[SUCCESS] Loaded {len(questions)} MCQ questions from {target_file}")
    return questions

def save_scores_to_file(scores, log_message=""):
    with open(SCORES_FILE, "w", encoding="utf-8") as file:
        file.write("=== PYTHON QUIZ CHALLENGE SCOREBOARD ===\n")
        for team_id, score in scores.items():
            file.write(f"Team {team_id}: {score} pts\n")
        if log_message:
            file.write(f"\nLast Action: {log_message}\n")

def init_game():
    global game_state
    questions = load_questions_from_file()
    primary_order = list(range(1, 13))
    scores = {str(i): 0 for i in range(1, 13)}
    save_scores_to_file(scores, "Game Initialized in Sequential Mode")
    
    game_state = {
        "questions": questions,
        "current_q_index": 0,
        "primary_team_order": primary_order,
        "active_team": 1,
        "tried_teams": [1],
        "wrong_options": [],
        "is_passed_question": False,
        "answer_revealed": False,
        "scores": scores,
        "quiz_over": False,
        "status_msg": "Question 1 assigned to Team 1 (Sequential Turn)"
    }

init_game()

def get_next_sequential_team(current_team, tried_teams):
    for offset in range(1, 13):
        candidate = ((current_team - 1 + offset) % 12) + 1
        if candidate not in tried_teams:
            return candidate
    return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/state", methods=["GET"])
def get_state():
    if not game_state.get("questions"):
        game_state["questions"] = load_questions_from_file()

    q_idx = game_state["current_q_index"]
    questions = game_state["questions"]
    current_q = questions[q_idx] if q_idx < len(questions) else None
    primary_team = (q_idx % 12) + 1
    
    return jsonify({
        "current_q_index": q_idx + 1,
        "total_questions": len(questions),
        "question_data": {
            "id": current_q["id"],
            "question": current_q["question"],
            "options": current_q["options"],
            "answer": current_q["answer"] if game_state["answer_revealed"] else None,
            "explanation": current_q["explanation"] if game_state["answer_revealed"] else None
        } if current_q else None,
        "primary_team": primary_team,
        "active_team": game_state["active_team"],
        "tried_teams": game_state["tried_teams"],
        "wrong_options": game_state["wrong_options"],
        "is_passed_question": game_state["is_passed_question"],
        "answer_revealed": game_state["answer_revealed"],
        "scores": game_state["scores"],
        "quiz_over": game_state["quiz_over"],
        "status_msg": game_state["status_msg"]
    })

@app.route("/api/submit", methods=["POST"])
def submit_option():
    if game_state["quiz_over"] or game_state["answer_revealed"]:
        return jsonify({"error": "Invalid action"}), 400

    data = request.json or {}
    choice = str(data.get("option", "")).strip().upper()
    if choice not in ("A", "B", "C", "D"):
        return jsonify({"error": "Select A, B, C, or D"}), 400

    q_idx = game_state["current_q_index"]
    current_q = game_state["questions"][q_idx]
    correct_answer = current_q["answer"].strip().upper()
    team = game_state["active_team"]

    if choice == correct_answer:
        points = 5 if game_state["is_passed_question"] else 10
        game_state["scores"][str(team)] += points
        game_state["answer_revealed"] = True
        game_state["status_msg"] = f"✔ Correct! Team {team} selected Option {choice} (+{points} pts)."
        save_scores_to_file(game_state["scores"], game_state["status_msg"])
    else:
        if choice not in game_state["wrong_options"]:
            game_state["wrong_options"].append(choice)
        
        next_team = get_next_sequential_team(team, game_state["tried_teams"])
        if next_team is None or len(game_state["wrong_options"]) >= 4:
            game_state["answer_revealed"] = True
            game_state["status_msg"] = f"✘ Option {choice} is incorrect! Revealing answer."
        else:
            game_state["active_team"] = next_team
            game_state["tried_teams"].append(next_team)
            game_state["is_passed_question"] = True
            game_state["status_msg"] = f"✘ Team {team} picked Option {choice} (Wrong). Passed in line to Team {next_team}!"

    return get_state()

@app.route("/api/pass", methods=["POST"])
def pass_question():
    if game_state["quiz_over"] or game_state["answer_revealed"]:
        return jsonify({"error": "Invalid action"}), 400

    data = request.json or {}
    target_team = data.get("target_team")
    current_team = game_state["active_team"]

    if target_team and int(target_team) not in game_state["tried_teams"]:
        next_team = int(target_team)
    else:
        next_team = get_next_sequential_team(current_team, game_state["tried_teams"])

    if next_team is None:
        game_state["answer_revealed"] = True
        game_state["status_msg"] = "All 12 teams passed! Revealing answer and explanation."
    else:
        game_state["active_team"] = next_team
        game_state["tried_teams"].append(next_team)
        game_state["is_passed_question"] = True
        game_state["status_msg"] = f"Team {current_team} passed! Question moves in line to Team {next_team}."

    return get_state()

@app.route("/api/reveal", methods=["POST"])
def reveal_now():
    game_state["answer_revealed"] = True
    game_state["status_msg"] = "Host revealed the answer and explanation."
    return get_state()

@app.route("/api/prev", methods=["POST"])
def prev_question():
    """Navigate back to the previous question"""
    prev_idx = game_state["current_q_index"] - 1
    if prev_idx >= 0:
        game_state["quiz_over"] = False
        game_state["current_q_index"] = prev_idx
        primary_team = (prev_idx % 12) + 1
        game_state["active_team"] = primary_team
        game_state["tried_teams"] = [primary_team]
        game_state["wrong_options"] = []
        game_state["is_passed_question"] = False
        game_state["answer_revealed"] = False
        game_state["status_msg"] = f"Moved back to Question {prev_idx + 1} (Assigned to Team {primary_team})."
    else:
        game_state["status_msg"] = "Already at Question 1!"
    return get_state()

@app.route("/api/next", methods=["POST"])
def next_question():
    next_idx = game_state["current_q_index"] + 1
    if next_idx >= len(game_state["questions"]):
        game_state["quiz_over"] = True
        game_state["status_msg"] = "Quiz Completed! Final scores saved to quiz_scores.txt."
    else:
        game_state["current_q_index"] = next_idx
        primary_team = (next_idx % 12) + 1
        game_state["active_team"] = primary_team
        game_state["tried_teams"] = [primary_team]
        game_state["wrong_options"] = []
        game_state["is_passed_question"] = False
        game_state["answer_revealed"] = False
        game_state["status_msg"] = f"Question {next_idx + 1} assigned to Team {primary_team} (Sequential Primary Turn)."
        
    return get_state()

@app.route("/api/reset", methods=["POST"])
def reset_quiz():
    init_game()
    return get_state()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)