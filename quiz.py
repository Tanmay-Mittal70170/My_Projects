# Print a formatted title banner for the quiz challenge
print("=" * 80)
print("PYTHON QUIZ CHALLENGE".center(80))
print("=" * 80)

# List of participating teams. 
# You can add or remove teams here, and the loop will automatically adjust!
teams = [
    "Team 1", "Team 2", "Team 3", "Team 4", "Team 5",
    "Team 6", "Team 7", "Team 8", "Team 9", "Team 10"
]

# Dictionary storing the correct answers for each question corresponding to the round/team number
correct_answers = {
    1: "A",
    2: "B",
    3: "C",
    4: "D",
    5: "C",
    6: "B"
}

# Store the total number of teams for modulo arithmetic (passing logic)
num_teams = len(teams)

# Main loop: Iterate through each team, starting numbering from 1
for i, team_name in enumerate(teams, start=1):
    print("\n" + "-" * 80)
    print("\n")
    print(f"--- {team_name.upper()}'S TURN ---\n")
    
    try:
        # Try to open and read the respective question text file (e.g., Question1.txt, Question2.txt)
        with open(f"Question{i}.txt", "r") as file:
            print(file.read())

        # Initialize tracking variables for the current question
        current_idx = i - 1                        # Index of the team currently answering
        correct_ans = correct_answers.get(i, "").upper()  # Fetch correct answer for this round
        attempts = 0                               # Count how many teams have attempted/passed
        resolved = False                           # Flag to check if the question has been answered

        # Loop to handle answering and passing the question to subsequent teams if passed
        while attempts < num_teams and not resolved:
            active_team = teams[current_idx]
            
            # Get user input and convert it to uppercase for uniform comparison
            user_input = input(f"\n{active_team}, enter option (A/B/C/D) or 'P' to Pass: ").strip().upper()

            # Handle the 'Pass' option
            if user_input == "P":
                print(f"{active_team} passes the question !")
                # Shift turn to the next team in a circular/wrap-around manner using modulo (%)
                current_idx = (current_idx + 1) % num_teams
                attempts += 1
                if attempts < num_teams:
                    print(f"Passes to {teams[current_idx].upper()}")
            
            # Handle valid option inputs (A, B, C, or D)
            elif user_input in ["A", "B", "C", "D"]:
                if user_input == correct_ans:
                    print(f"Correct answer by {active_team}!")
                else:
                    print("Wrong Answer! uhhh ohhh !")
                resolved = True  # Question is now resolved (either correct or wrong)
            
            # Handle invalid inputs
            else:
                print("Invalid input! Please enter A, B, C, D, or P.")
        
        # If all teams passed without attempting an answer
        if not resolved:
            print(f"\nAll teams passed. Correct answer was: {correct_ans}")

    # Handle the error if the corresponding question text file is missing
    except FileNotFoundError:
        print(f"[Error] Missing 'Question{i}.txt' in this folder.")

# Print completion message when all turns are finished
print("\n" + "-" * 80)
print("QUIZ COMPLETE!")