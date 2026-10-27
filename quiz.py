print("=" * 80)
print("PYTHON QUIZ CHALLENGE".center(80))
print("=" * 80)

# Add or remove teams from this list anytime. 
# The loop below will automatically adjust!
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

# enumerate automatically counts your teams. 'i' becomes 1, 2, 3...
for i, team_name in enumerate(teams, start=1):
    print("\n" + "-" * 80)
    print("\n")
    print(f"--- {team_name.upper()}'S TURN ---\n")
    
    try:
        # It looks for Question1.txt for the 1st team, Question2.txt for the 2nd, etc.
        with open(f"Question{i}.txt", "r") as file:
            print(file.read())

        current_idx = i-1
        correct_ans = correct_answers.get(i, "").upper()
        attempts = 0
        resolved = False 

        while attempts < num_teams and not resolved:
            active_team = teams[current_idx]
            user_input = input(f"\n{active_team}, enter option (A/B/C/D) or 'P' to Pass: ").strip().upper()

            if user_input == "P":
                print(f"{active_team} passes the question !")
                current_idx = (current_idx + 1) % num_teams
                attempts +=1
                if attempts < num_teams:
                    print(f"Passes to {teams[current_idx].upper()}")
            elif user_input in ["A","B","C","D"]:
                if user_input == correct_ans:
                    print(f"correct answer by {active_team}!")
                else:
                    print("Wrong Answer! uhhh ohhh !")
                resolved = True
            else:
                print("Invalid input! please enter A, B, C, D or P.")
        if not resolved:
            print(f"\nAll teams passed. Correct answer was: {correct_ans}")

        
    except FileNotFoundError:
        print(f"[Error] Missing 'Question{i}.txt' in this folder.")

print("\n" + "-" * 80)
print("QUIZ COMPLETE!")

"""
In this code tanmay do kaam krne h :
1. jab team ka question wrong ho then woh question next team pr passe ho jaye and points show krre negative 
and all jo bhi h 
2. jab question khatam ho toh ek dum se next question aa jaye for example pehla question khatam hua toh 
enter krne par dusra question aaye , and baad me teams ke naame bhi daal denge aur acha banane ke liye 
3... raaghav ko bhi question nikalne dena 
"""