import random

round=int(input("how many round You want to play"))

opt=["Scisor","Rock","Paper"]

comp_count=0

user_count=0

for i in range(round):

    user=input("enter your choice").capitalize()
    comp=random.choice(opt)

    while user not in opt:
        print("Invalid Choice Pls enter between Scisor, Rock and paper")
        user=input("Enter the Choice Again").capitalize()

    if user=="Scisor" and comp=="Rock":
        print("user-",user,"computer-",comp)
        print("user Wins")
        user_count+=1
    
    elif user=="Scisor" and comp=="Paper":
        print("user-",user,"computer-",comp)
        print("comp Wins")
        comp_count+=1

    elif user=="Rock" and comp=="Scisor":
        print("user-",user,"computer-",comp)
        print("user Wins")
        user_count+=1
    
    elif user=="Rock" and comp=="Paper":
        print("user-",user,"computer-",comp)
        print("comp Wins")
        comp_count+=1

    elif user=="Paper" and comp=="Rock":
        print("user-",user,"computer-",comp)
        print("User Wins")
        user_count+=1

    elif user=="Paper" and comp=="Scisor":
        print("user-",user,"computer-",comp)
        print("comp Wins")
        comp_count+=1

    else:
        print("user-",user,"computer-",comp)
        print("Thsi round is a Draw!!")

if comp_count>user_count:
    print("Final Score","-","user_points",user_count,"|","computer_point",comp_count) 
    print("Comp Wins This Game")

elif comp_count<user_count:
    print("Final Score","-","user_points",user_count,"|","computer_point",comp_count) 
    print("User Wins This Game")

else:
    print("Final Score","-","user_points",user_count,"|","computer_point",comp_count) 
    print("This Game is a Draw!!")

