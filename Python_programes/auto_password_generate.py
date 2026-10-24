import random

# Define character sets directly using string literals
char_pool = "abcdefghijklmnopqrstuvwxyz"

type_count = 1

use_upper = input("Include uppercase letters? (Y/N): ").strip().upper()
use_digits = input("Include numbers? (Y/N): ").strip().upper()
use_symbols = input("Include symbols? (Y/N): ").strip().upper()

if use_upper == "Y":
    char_pool += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    type_count += 1

if use_digits == "Y":
    char_pool += "0123456789"
    type_count += 1

if use_symbols == "Y":
    # Standard ASCII punctuation characters
    char_pool += "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    type_count += 1

if type_count == 1:
    strength = "Weak"
elif type_count == 2:
    strength = "Moderate"
else:
    strength = "Strong"

length = int(input("Enter password length: "))
password = "".join(random.choices(char_pool, k=length))

print("\nGenerated Password:", password)
print("Password Strength:", strength)