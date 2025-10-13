import random

def get_user_choice():
    """
    Prompts the user to enter 'rock', 'paper', or 'scissors'.
    Validates the input and re-prompts until a valid choice is given.
    Returns the user's valid choice as a string.
    """
    choices = ['rock', 'paper', 'scissors']
    while True:
        user_input = input("Enter your choice (rock, paper, or scissors): ").lower()
        if user_input in choices:
            return user_input
        else:
            print("Invalid choice. Please enter 'rock', 'paper', or 'scissors'.")

def get_computer_choice():
    """
    Randomly selects 'rock', 'paper', or 'scissors'.
    Returns the computer's choice as a string.
    """
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def determine_winner(user_choice: str, computer_choice: str) -> str:
    """
    Determines the winner of a rock-paper-scissors round.
    
    Args:
        user_choice: The user's choice ('rock', 'paper', or 'scissors').
        computer_choice: The computer's choice ('rock', 'paper', or 'scissors').
        
    Returns:
        A string indicating the winner: 'User', 'Computer', or 'Tie'.
    """
    if user_choice == computer_choice:
        return 'Tie'
    
    # Define winning conditions
    winning_conditions = {
        'rock': 'scissors',
        'scissors': 'paper',
        'paper': 'rock'
    }
    
    if winning_conditions[user_choice] == computer_choice:
        return 'User'
    else:
        return 'Computer'

def play_round():
    """
    Orchestrates a single round of the game, gets choices, determines winner, and displays results.
    """
    user_choice = get_user_choice()
    computer_choice = get_computer_choice()
    winner = determine_winner(user_choice, computer_choice)

    print(f"You chose {user_choice}, Computer chose {computer_choice}.")
    if winner == 'User':
        print("You Win!")
    elif winner == 'Computer':
        print("Computer Wins!")
    else:
        print("It's a Tie!")

def main():
    """
    Main game loop to allow multiple rounds and a quit option.
    """
    while True:
        play_round()
        play_again = input("Play again? (yes/no): ").lower()
        if play_again != 'yes':
            break
    print("Thanks for playing!")

if __name__ == '__main__':
    main()
