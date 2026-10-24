from random import choice

words = [
    "python", "variable", "function", "integer", "boolean",
    "string", "syntax", "module", "object", "class",
    "import", "lambda", "loop", "index", "tuple", "dictionary"
]

select = choice(words)
guessed_letters = []

print("Word:", "_ " * len(select))

attempts = 6

while True:

    print("Guessed letters:", ", ".join(guessed_letters) if guessed_letters else "None")
    print("Attempts remaining:", attempts)

    guess = input("\nEnter Your guess: ").lower().strip()

    if len(guess)>1:
        print("Error: You Haved Entered More Than One Character!!")
        continue

    if len(guess) != 1 or not guess.isalpha():
        print("Error:You Entered the Wrong Choice!!")
        continue

    if guess in guessed_letters:
        print("Reminder:You Had Already Guessed this Letter please Enter something else!!")
        continue

    guessed_letters.append(guess)


    if guess in select:
        print("You are Right! The Letter", guess, "Is in the Word")
    else:
        print("You guessed it wrong!!")
        attempts -= 1
        print("Attempts remaining:", attempts)


    display = ""
    for letter in select:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "

    print("Word:", display)

 
    if "_" not in display:
        print("\nCongratulations! You Had Guessed the Word:", select)
        break


    if attempts == 0:
        print("\nSorry! You are Out of Attempts. The Word Was:", select)
        break

input("Press Enter To Exit...")