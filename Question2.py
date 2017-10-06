"""
 Thomas Herr
 200325519

 Generate a random number and ask the user to guess it
"""

import random

# Seed with current time
random.seed()

# Have no idea what kind of range you are looking for, use 10 to make it at least possible to win
randomNumber = random.randint(1, 10)

guess = input("Guess the random number (between 1 and 10):")

if(guess==randomNumber):
    print("You win! ", guess, " was the random number!")
else:
    print("Incorrect. Random number was: ", randomNumber, " Your Guess: ", guess)