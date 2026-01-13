# 6.100A Fall 2025
# Problem Set 4
# Name: Jan Szmajda
# Collaborators: None


import random


############################################################
# Global variables
############################################################


AMOUNTS = [
    0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400,
    500, 750, 1000, 5000, 10000, 25000, 50000, 75000,
    100000, 200000, 300000, 400000, 500000, 750000, 1000000,
]

CASES = list(range(1, 27))

MAX_ROUND_NUMBER = 9


############################################################
# Game state display
############################################################


########## DO NOT MODIFY THIS FUNCTION ##########
def setup_game_board(active_cases, case_to_amount, player_case=None):
    """
    Create a visual representation of the game board, showing the prize
    amounts and the status of each case. Closed cases are displayed with
    their numbers, and opened cases (including the player's selected case)
    are marked with an "X" on the board.

    Parameters:
        active_cases (list): List of active (closed) case numbers.
        case_to_amount (dict): Dictionary mapping case numbers to prize amounts.
        player_case (int, optional): The player's selected case number. Defaults to None.

    Returns the formatted game board as a string, showing the prize amounts and
    the status of each case.
    """
    cell_width = 14
    case_cell_width = 5

    # Initialize the board with placeholders
    board = ["X".center(cell_width)] * 26
    middle_section = ["X".center(case_cell_width)] * 26

    # Populate the board with active case values
    for case in active_cases:
        amount = case_to_amount[case]
        idx = AMOUNTS.index(amount)
        board[idx] = f"${amount:,}".center(cell_width)
        middle_section[case - 1] = f"{case}".center(case_cell_width)

    # Ensure player's case prize is displayed on the prize board
    if player_case is not None:
        player_amount = case_to_amount[player_case]
        idx = AMOUNTS.index(player_amount)
        board[idx] = f"${player_amount:,}".center(cell_width)
        # Mark player's case as X in the case board
        middle_section[player_case - 1] = "X".center(case_cell_width)

    # Function to generate row separators based on cell width
    def generate_row_separator(columns, width):
        return "+" + "+".join(["-" * (width)] * columns) + "+\n"

    # Generate the board with ASCII art for values
    board_str = "Prize Board\n"
    board_str += generate_row_separator(4, cell_width)
    for i in range(0, 26, 4):
        row_str = "|"
        for j in range(4):
            if i + j < 26:
                row_str += f"{board[i + j]}|"
            else:
                row_str += " " * (cell_width) + "|"
        board_str += row_str + "\n"
        board_str += generate_row_separator(4, cell_width)

    # Add the middle section for case numbers
    middle_str = "Case Board\n"
    middle_str += generate_row_separator(5, case_cell_width)
    for i in range(0, 26, 5):
        row_str = "|"
        for j in range(5):
            case_idx = i + j
            if case_idx >= 26:
                row_str += " " * (case_cell_width) + "|"
                continue
            row_str += f"{middle_section[case_idx]}|"
        middle_str += row_str + "\n"
        middle_str += generate_row_separator(5, case_cell_width)

    return board_str + "\n" + middle_str
##################################################


########## DO NOT MODIFY THIS FUNCTION ##########
def print_game_board(prizes, case_status, player_case):
    """
    Print the current game board, showing the status of each case
    and the prize amounts for the remaining closed cases.

    Parameters:
        prizes (dict): Dictionary mapping case numbers to prize amounts.
        case_status (dict): Dictionary tracking the status of each case.
        player_case (int): The player's selected case number.

    Prints the formatted game board as a string.
    """
    active_cases = []
    for case in range(1, 27):
        if case_status[case] == 'closed':
            active_cases.append(case)

    game_board = setup_game_board(active_cases, prizes, player_case=player_case)
    print(game_board)
##################################################


############################################################
# Game setup
############################################################


def create_prize_dict():
    """
    Generate a dictionary mapping case numbers to randomly shuffled prize amounts.
    Each key is a case number and each value is a prize amount. The prize amounts
    are randomly shuffled to ensure that each game has a unique distribution of prizes.

    Returns a dictionary mapping case numbers to randomly shuffled prize amounts.
    """
    amounts = AMOUNTS[:]
    random.shuffle(amounts)
    d = {}

    #run through index of amounts and map each to a case in dictionary
    for i in range(len(AMOUNTS)):
        d[CASES[i]] = amounts[i]
    return d


############################################################
# User actions
############################################################


def validate_users_briefcase_choice(choice, case_status, case_action):
    """
    Validate the user's choice of briefcase number.

    If case_action is "open", the choice must be an integer between 1 and 26
    and the case must be closed.
    If case_action is "select", the choice must be an integer between 1 and 26.

    To ensure any accidental spaces typed by the players won't cause an error, strip
    any excess whitespace from the user input before checking its validity. It may
    be helpful to check if the user input is a string representing a number first.
    If the player selects an already opened case, their own case, or a non-number
    input, raise a ValueError.

    Parameters:
        choice (str): The player's input representing the briefcase number.
        case_status (dict): A dictionary where keys are briefcase numbers
            and values are either "closed", "opened", or "player_case".
        case_action (str): The action being performed. This should be either "open"
            (for opening a case) or "select" (for selecting a briefcase to hold).

    Raises a ValueError if the choice is not valid.
    """
    choice = choice.strip()
    nums = "1234567890"
    flag = False

    #checking if user input is all integers. if no, then error. if yes, cast to int
    for i in choice:
        if i not in nums:
            flag = True
    if flag == True:
        raise ValueError("Invalid input. Please select an available case.")
    else:
        choice = int(choice)

    #check if choice in list of integers
    if choice not in CASES:
            raise ValueError("Invalid input. Please select an available case.")

    #if case_action is open, check for case being closed
    if case_action == "open":
        for k,v in case_status.items():
                if choice == k and v != "closed":
                    raise ValueError("Invalid choice. Please select an unopened case.")


def select_briefcase(case_status):
    """
    Continuously prompt the player to input a briefcase number (1-26) until a valid
    and unopened case is chosen. Make sure to handle any raised ValueErrors.
    Mark the selected case as the player's case in the `case_status` dictionary.

    Parameters:
        case_status (dict): Dictionary tracking the status of each case, with values
            indicating whether a case is 'closed', 'opened', or the 'player_case'.

    Returns the player's selected case number as an integer.
    """
    flag = False
    unopened = []
    for k,v in case_status.items():
                if v == "closed":
                    unopened.append(k)

    #while flag is false prompt user to choose briefcase
    while flag == False:
        try:
            choice = input("Choose Your Case Number (1-26): ")
            validate_users_briefcase_choice(choice, case_status, "select")
            choice = int(choice.strip())
            case_status[choice] = "player_case"
            flag = True
        except ValueError as e:
            print(e)

    #printing available cases
    unopened.remove(choice)
    print(f"Available Cases: {unopened}")

    return choice


def open_briefcases(prizes, case_status, num_to_open, round_number):
    """
    Opens a specified number of briefcases and updates their status.

    Your implementation should follow these steps:
        1. Round and case prompting:
            For each briefcase to be opened in the round, display a message to indicate the
            current round and how many cases remain to be opened (e.g., "Round 1 - 6 Cases to Open").
            Prompt the player to select a briefcase to open by typing in a number. Make sure to handle
            any raised ValueErrors.
        2. Reveal the prize and update game state:
            Once a valid case is selected, reveal the prize inside the case and mark it as "opened" in
            the case_status dictionary. After each valid selection, display the remaining closed cases
            so the player knows which cases are still available.
        3. Repeat until all cases for the round are opened

    Parameters:
        prizes (dict): Dictionary mapping case numbers to prize amounts.
        case_status (dict): Dictionary tracking the status of each case.
        num_to_open (int): The number of cases to open in this round.
        round_number (int): The current round number, starting from 1.
    """
    flag = False

    unopened = []
    for k,v in case_status.items():
                if v == "closed":
                    unopened.append(k)

    #loop while there's still cases to open
    while num_to_open > 0:
        print(f"Round {round_number} - {num_to_open} Cases to Open")

        #user chooses & checking if user input is valid
        while flag == False:
            try:
                choice = input("Choose a case to open: ")
                validate_users_briefcase_choice(choice, case_status, "open")
                choice = int(choice.strip())
                case_status[choice] = "opened"
                flag = True
            except ValueError as e:
                print(e)

        #show user prize for case and list of available cases
        print(f"You selected case {choice} worth ${prizes[choice]:,.2f}")
        unopened.remove(choice)
        print(f"Available Cases: {unopened}")

        flag = False
        num_to_open -= 1

########## DO NOT MODIFY THIS FUNCTION ##########
def get_users_input_for_offer(prizes, case_status, bankers_offer, round_number):
    """
    Repeatedly prompt the player to accept or reject the banker's
    offer until a valid input ('yes', 'no', or 'auto') is received.

    If 'auto' is chosen, the auto_decision_helper will be used to decide.

    Parameters:
        prizes (dict): Dictionary mapping case numbers to prize amounts.
        case_status (dict): Dictionary tracking the status of each case.
        bankers_offer (int): The amount of the banker's offer.
        round_number (int): The current round number.

    Returns the player's decision ('yes' or 'no').
    """
    while True:
        try:
            accept_offer = input("Accept offer? (yes/no/auto): ").strip()
            if accept_offer == "auto":
                # Call the helper to auto-decide
                accept_offer = auto_decision_helper(prizes, case_status, bankers_offer, round_number)
                print(f"Auto decision: {accept_offer}")
                break
            if accept_offer not in ["yes", "no"]:
                raise ValueError("Invalid input. Please enter 'yes', 'no', or 'auto'.")
            break
        except ValueError as e:
            print(e)
    return accept_offer
##################################################


############################################################
# Banker actions
############################################################


########## DO NOT MODIFY THIS FUNCTION ##########
def calculate_bankers_offer(prizes, case_status):
    """
    Calculate the banker's offer. Average the values of the remaining (closed)
    cases and apply a randomly generated risk factor between 0.70 and 1.10.
    The offer is a percentage of this average value.

    Parameters:
        prizes (dict): Dictionary mapping case numbers to prize amounts.
        case_status (dict): Dictionary tracking the status of each case.

    Returns the banker's offer as an integer.
    """
    active_cases = []
    for case, status in case_status.items():
        if status == 'closed' or status == 'player_case':
            active_cases.append(case)

    remaining_amounts = []
    for case in active_cases:
        remaining_amounts.append(prizes[case])
    average_value = sum(remaining_amounts) / len(active_cases)
    risk_factor = random.uniform(0.70, 1.1)
    offer = risk_factor * average_value

    return round(offer)
##################################################


########## DO NOT MODIFY THIS FUNCTION ##########
def handle_bankers_offer(prizes, case_status, offers):
    """
    Calculate the banker's offer, display the previous and current offers,
    and return the current offer.

    Parameters:
        prizes (dict): Dictionary mapping case numbers to prize amounts.
        case_status (dict): Dictionary tracking the status of each case.
        offers (list): List of previous banker offers.

    Returns the current banker's offer as an integer.
    """
    offer = calculate_bankers_offer(prizes, case_status)
    if offers:
        print("Previous Banker Offers: " + ", ".join(f"${prev_offer:,.2f}" for prev_offer in offers))
    print(f"Current Banker's Offer: ${offer:,.2f}")
    return offer
##################################################


############################################################
# Game flow management
############################################################


########## DO NOT MODIFY THIS FUNCTION ##########
def get_num_cases_to_open(round_number):
    """
    Determine the number of briefcases to open during the current round.
    The number of cases decreases with each subsequent round, starting
    from 6 in the first round and reducing to 1 after the fifth round.

    Parameters:
        round_number (int): The current round count, starting from 1.

    Returns the number of cases to open in the current round.
    """
    return max(1, 7 - round_number)
##################################################


########## DO NOT MODIFY THIS FUNCTION ##########
def evaluate_deal(deal_amount, player_case_amount):
    """
    Evaluate the player's deal by comparing the banker's offer to their
    case's prize amount.

    Parameters:
        deal_amount (int): The amount of the banker's offer.
        player_case_amount (int): The prize amount in the player's selected case.

    Returns a message indicating if the player made a good, bad, or great deal.
    """
    if deal_amount < player_case_amount:
        return "You made a bad deal!"
    elif deal_amount > player_case_amount:
        return "You made a great deal!"
    else:
        return "You made a good deal!"
##################################################


def auto_decision_helper(prizes, case_status, bankers_offer, round_number):
    """
    The user only takes an offer after round 2. After that, the user averages the
    total of money left in the unopened briefcases.
    If that number is less than the banker's offer, they take the banker's deal

    This strategy should only use information that the player has access to in the game.

    Parameters:
        prizes (dict): Dictionary mapping case numbers to prize amounts.
        case_status (dict): Dictionary tracking the status of each case.
        bankers_offer (int): The amount of the banker's offer.
        round_number (int): The current round number.

    Returns the player's decision ('yes' or 'no').
    """
    unopened_cases = []
    total = 0
    count = 0

    if round_number > 2:
        #add all the unopened case numbers to list
        for k,v in case_status.items():
            if v == "closed" or v == "player_case":
                unopened_cases.append(k)
        #correspond prizes to unopened cases
        for key in prizes.keys():
            if key in unopened_cases:
                total += int(prizes[k])
                count += 1

        print(total)
        #if banker's offer greater than average, user takes the deal
        if bankers_offer > (total / count):
            return "yes"
        else:
            return "no"
    else:
        return "no"


def play_game():
    """
    Simulates the entire game of "Deal or No Deal".

    The implementation follows these steps:
        1. Print a welcome message and set up the game by initializing the available
           cases and mapping each case to a hidden prize amount. Also, initialize a
           data type to keep track of the banker's offers. Print the initial game
           board and prompt the player to select one case to keep until the end.
        2. Across multiple rounds, the player opens other cases, revealing their prizes.
           The number of cases to open depends on the current round number. Note that
           the current round should start at 1. Update the game state to reflect game
           progress.
        3. After each round, display the updated game board and the banker's offer.
           Remember to keep track of the banker's previous offers. The player decides
           whether to accept the offer or continue. If the player accepts the banker's
           offer, the game ends, and the deal is evaluated.
        4. If the player continues to the final round, they may switch their case
           for the one remaining unopened case or keep their original case.
        5. End the game by revealing the prize in the chosen case.

    Model the order in which statements are printed on the example at the end of Section 4.5.
    """
    case_status = {}
    for i in CASES:
        case_status[i] = "closed"

    offers = []
    bankers_offer = 0
    round_number = 1
    round_to_opens = {1:6, 2:5, 3:4, 4:3, 5:2, 6:1, 7:1, 8:1, 9:1}

    last_case = 0

    prize = create_prize_dict()

    print("Welcome to Deal or No Deal! Try your luck in finding the $1,000,000 briefcase.")
    print_game_board(prize, case_status, None)

    choice = select_briefcase(case_status)

    #while loop implementing all of our helper functions
    while round_number <= MAX_ROUND_NUMBER:
        num_to_open = round_to_opens[round_number]
        open_briefcases(prize, case_status, num_to_open, round_number)
        print_game_board(prize, case_status, choice)
        calculate_bankers_offer(prize, case_status)
        bankers_offer = handle_bankers_offer(prize, case_status, offers)
        offers.append(bankers_offer)
        accept_offer = get_users_input_for_offer(prize, case_status, bankers_offer, round_number)

        if accept_offer == "yes":
            print(f"Congrats, you won ${bankers_offer:,.2f}!")
            print(f"Your case contained ${prize[choice]:,.2f}. {evaluate_deal(bankers_offer, prize[choice])}")
            break

        round_number += 1

        #final round decision. while True loop for exceptions. if/elif for user choice
        if round_number > MAX_ROUND_NUMBER:
            while True:
                try:
                    final_decision = input("Do you want to switch cases? (yes/no): ")

                    if final_decision == "yes":
                        for k,v in case_status.items():
                            if v == "closed":
                                last_case = k
                        print(f"Congrats, your case #2 won ${prize[last_case]:,.2f}.")
                        break
                    elif final_decision == "no":
                        print(f"Congrats, your case #1 won ${prize[choice]:,.2f}.")
                        break
                    else:
                        raise ValueError("Invalid input. Please enter 'yes' or 'no'.")
                except ValueError as e:
                    print(e)

def manual_tests():
    """
    Run manual tests to verify the correctness of your implementations.
    """
    # Uncomment the following line to test your create_prize_dict() implementation
    # print(create_prize_dict())

    # Uncomment the following line to test your play_game() implementation
    play_game()
    pass


if __name__ == "__main__":
    manual_tests()
