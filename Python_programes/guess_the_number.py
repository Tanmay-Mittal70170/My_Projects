from random import randint

again = "yes"

while again == "yes" or again == "Yes":

    number = randint(1, 100)

    for attempt in range(1, 8):

        try:
            user = int(input("Enter the number: "))

        except ValueError:
            print("You entered a wrong data type. Use Int only.")
            print("Try Again")
            continue

        if user > 100:
            print("The number exceeds the range (1-100)")
            continue

        else:

            if user > number:
                print("Too High")

            elif user < number:
                print("Too Low")

            else:
                print("Congratulations! You guessed it right. It's number", number)
                break

            print("The attempts remaining are", 7 - attempt)

    else:
        print("Game Over")
        print("The Secret number was", number)

    again = input("Do you want to play again? Yes/No: ")