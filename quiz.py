"""
================================================================================
PROJECT: Interactive Python Quiz Challenge
DESCRIPTION: A multi-team quiz game that reads questions from external text files,
             manages turn rotation, handles passing mechanics, and validates answers.
================================================================================
"""

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================

# Print a stylized header banner for the quiz title
print("=" * 80)
print("PYTHON QUIZ CHALLENGE".center(80))
print("=" * 80)

# List of participating teams
teams = [
    "Team 1", "Team 2", "Team 3", "Team 4", "Team 5", "Team 6"
]

# Dictionary storing the correct answers corresponding to each question number
correct_answers = {
    1: "A",
    2: "D",
    3: "C",
    4: "D",
    5: "C",
    6: "B"
}

num_teams = len(teams)


# ==========================================
# 2. MAIN GAME LOOP (ITERATING THROUGH QUESTIONS)
# ==========================================

for i, team_name in enumerate(teams, start=1):
    print("\n" + "-" * 80)
    print(f"\n--- {team_name.upper()}'S TURN ---\n")
    
    try:
        # Open and display the question text directly from the current folder (Normal/Left-aligned)
        with open(f"Question{i}.txt", "r") as file:
            print(file.read())

        current_idx = i - 1                                 # Index of the team currently answering
        correct_ans = correct_answers.get(i, "").upper()      # Fetch the correct answer for this round
        attempts = 0                                        # Track how many teams have attempted/passed
        resolved = False                                    # Flag to check if the question has been resolved

        # ==========================================
        # 3. ANSWER & PASS SUB-LOOP
        # ==========================================
        while attempts < num_teams and not resolved:
            active_team = teams[current_idx]
            
            # Prompt the active team for their answer or pass choice
            user_input = input(f"\n{active_team}, enter option (A/B/C/D) or 'P' to Pass: ").strip().upper()

            # Handle the 'Pass' option
            if user_input == "P":
                print(f"{active_team} passes the question!")
                # Shift turn to the next team in a circular/wrap-around manner using modulo (%)
                current_idx = (current_idx + 1) % num_teams
                attempts += 1
                if attempts < num_teams:
                    print(f"Passes to -> {teams[current_idx].upper()}")
            
            # Handle valid answer choices (A, B, C, or D)
            elif user_input in ["A", "B", "C", "D"]:
                if user_input == correct_ans:
                    print(f"Correct answer by {active_team}!")
                else:
                    print(f"Wrong Answer! (Correct option was: {correct_ans})")
                resolved = True  # Mark question as resolved
            
            # Handle invalid inputs
            else:
                print("Invalid input! Please enter A, B, C, D, or P.")
        
        # Triggered if all teams passed without anyone attempting an answer
        if not resolved:
            print(f"\nAll teams passed. The correct answer was: {correct_ans}")

    # Handle missing question files gracefully
    except FileNotFoundError:
        print(f"[Error] Missing 'Question{i}.txt' in this folder. Please make sure it exists.")


# ==========================================
# 4. GAME COMPLETION
# ==========================================
print("\n" + "-" * 80)
print("QUIZ COMPLETE! THANK YOU FOR PARTICIPATING!".center(80))
print("=" * 80)

# Keeps the command line window open until you press Enter
input("\nPress Enter to exit the game...")