# Problem Set 3, wordle.py
# Name: Jan Szmajda
# Collaborators: None
# Time spent: 6

# Wordle Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

def get_alphabet_hint(secret_word, all_guesses):
    """
    takes in the secret word and a list of all previous guesses and returns a string of hint text
    :param secret_word: a string, the word to be guessed
    :param all_guesses: a list of all the previous valid guesses the user inputed
    :return: a string which replaces letters that were incorrect guesses with underscores and puts
	     semi-correct guesses (correct letter, incorrect place) in /x/
    """
    # we have coded this for you
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    out_list = []
    for char in alphabet:
        out_list.append(" "+char+" ")

    for guess in all_guesses:
        for i, char in enumerate(list(guess)):
            # the letter is not in the secret word
            if char not in secret_word:
                out_list[alphabet.find(char)]=" _ "
            # the letter is in the secret word but in the incorrect spot
            elif char != secret_word[i]:
                out_list[alphabet.find(char)] = "/"+char+"/"
            # the letter is in the secret word and in the correct spot
            elif char == secret_word[i]:
                # there is another instance of the letter in the secret word that has not been guessed
                if secret_word.count(char) > guess.count(char):
                    out_list[alphabet.find(char)] = "/" + char + "/"
                # the letter has been guessed correctly in its spot(s)
                else:
                    out_list[alphabet.find(char)] = "|" + char.upper() + "|"
    return "".join(out_list)

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()

# end of helper code
# -----------------------------------

def check_user_input(secret_word, user_guess):
    """

    :param secret_word: a string, the word to be guessed
    :param user_guess: a string, the users guess
    :return: False if user_guess does not satisfy at least
	     one of the below conditions, True otherwise.
    1. must be the same length as secret_word
    2. must consist of only letters (uppercase or lowercase)
    3. must be a word found in words.txt
    """
    alphabet_and_nums = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"

    check = True

    # Checking if the characters in user_guess are letters or numbers
    char_flag = True
    for i in user_guess:
        if i not in alphabet_and_nums:
            char_flag = False

    # Checks for length, proper characters, and real word w/ flag
    if len(user_guess) != len(secret_word):
        print("Oops! That word length is not correct.")
        check = False
    elif char_flag == False:
        print("Oops! That is not a valid word.")
        check = False
    elif user_guess.lower() not in wordlist:
        print("Oops! That is not a real word.")
        check = False

    return check
    pass

def get_guessed_feedback(secret_word, user_guess):
    """

    :param secret_word: a string, the word to be guessed
    :param user_guess: a string, a valid user guess
    :return: a string with uppercase and lowercase letters and
	     underscores, each separated by a space (e.g. 'B _ _ _ s')
    """
    final = ""

    # Runs through index, checking for each condition in order
    for i in range(len(user_guess)):
        if user_guess[i] == secret_word[i]:
            final += str(user_guess[i].upper()) + " "
        elif user_guess[i] in secret_word:
            final += str(user_guess[i].lower()) + " "
        else:
            final += "_" + " "

    stripped = final.strip()    # Stripping the final string from whitespaces

    return stripped
    pass

def wordle(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Wordle.

    * At the start of the game, let the user know how many letters the
      secret_word contains and how many guesses and warnings they start with.

    * The user should start with 6 guesses and 3 warnings

    * Before each round, you should display to the user how many guesses
      they have left.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a valid word!

    * The user should receive feedback immediately after each guess about
      whether their guess is valid, how closely it matches the secret_word,
      and the alphabet hint.

    * After each guess, you should display to the user the progression of
      their partially guessed words so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    warnings = 3
    guesses = 6

    loop_flag = False
    win_flag = False

    wordle_list = []
    wordle_str = ""
    wordle_str_count = 0

    print("Welcome to the game Wordle!")
    print(f"I am thinking of a word that is {len(secret_word)} letters long.")
    print(f"You have {warnings} warnings remaining.")

    while loop_flag == False:
        print(f"You have {guesses} guesses left.")
        user_guess = input("Please guess a word: ").lower()

        if check_user_input(secret_word, user_guess) == True:   # If user guess passes checks
            print("WORDLE response:")
            if wordle_str_count == 0:   # Making wordle guesses stack like in real game
                wordle_list.append(user_guess)
                wordle_str += get_guessed_feedback(secret_word, user_guess)
                wordle_str_count += 1
            elif wordle_str_count != 0:
                wordle_list.append(user_guess)
                wordle_str += "\n" + get_guessed_feedback(secret_word, user_guess)
            print(wordle_str)

            print("Alphabet HINT:")
            print(get_alphabet_hint(secret_word, wordle_list))

            guesses -= 1
        else:    # If user guess doesn't pass checks
            if warnings > 0:
                warnings -= 1
                print(f"You have {warnings} warnings remaining.")
            elif warnings == 0:
                guesses -= 1
                print(f"You have {warnings} warnings remaining.")

        if user_guess == secret_word:   # Checks to see if user is out of guesses or won
            loop_flag = True
            win_flag = True
        elif guesses == 0:
            loop_flag = True
            win_flag = False

        if loop_flag == False:  #Printing dashes when loop continues
            print("-------------------")





    # Finding amount of unique letters for score
    unique_str = ""
    for i in secret_word:
        if i not in unique_str:
            unique_str += str(i)
    unique_letters = len(unique_str)

    # Win/Loss check to print out necessary strings
    if win_flag == True:
        print("Congratulations, you won!")
        print(f"You guessed the correct word in {9 - (warnings + guesses)} tries!")
        print(f"Your total score is {guesses * unique_letters * len(secret_word)}")
    elif win_flag == False:
        print(f"Sorry, you ran out of guesses. The word was {secret_word}.")


    pass

# When you've completed your wordle function,
# you can test it with the code below.
# (hint: you might want to pick your own
# secret_word while you're doing your own testing)


if __name__ == "__main__":

    pass

    # To test, first comment out the pass line above.

    # To test with your own chosen secret word,
    # change the line below to a specific word to test:
    # secret_word = "tact"

    # To test with a randomly chosen secret word,
    # uncomment the line below for a randomly generated word:
    # secret_word = choose_word(wordlist)

    # Now uncomment this line to test the gameplay!
    # wordle(secret_word)
