print("=" * 80)
print("PYTHON QUIZ CHALLENGE".center(80))
print("=" * 80)

# Add or remove teams from this list anytime. 
# The loop below will automatically adjust!
teams = [
    "Team 1", "Team 2", "Team 3", "Team 4", "Team 5",
    "Team 6", "Team 7", "Team 8", "Team 9", "Team 10"
]

# enumerate automatically counts your teams. 'i' becomes 1, 2, 3...
for i, team_name in enumerate(teams, start=1):
    print("\n" + "-" * 80)
    print("\n")
    print(f"--- {team_name.upper()}'S TURN ---\n")
    
    try:
        # It looks for Question1.txt for the 1st team, Question2.txt for the 2nd, etc.
        with open(f"Question{i}.txt", "r") as file:
            print(file.read())
            
        input(f"\n{team_name}, press Enter to lock in your answer...")
        
    except FileNotFoundError:
        print(f"[Error] Missing 'Question{i}.txt' in this folder.")

print("\n" + "-" * 80)
print("QUIZ COMPLETE!")

