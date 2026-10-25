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

# isme questions ke answers set krlena abhi random krre h
correct_answers = {
    1:"A",
    2:"B",
    3:"C",
    4:"D",
    5:"C",
    6:"B"
}

num_teams = len(teams)

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
            
        input(f"\n{team_name}, press Enter to lock in your answer...")
        
    except FileNotFoundError:
        print(f"[Error] Missing 'Question{i}.txt' in this folder.")

# Print completion message when all turns are finished
print("\n" + "-" * 80)
print("QUIZ COMPLETE!")