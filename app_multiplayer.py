import getpass
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_instructions():
    print("--- MASTERMIND-MANIA RULES ---")
    print("1. The Code-Setter picks 5 UNIQUE digits (0-9).")
    print("2. No digit can be repeated (e.g., 12345 is valid, 11223 is NOT).")
    print("3. Feedback provided:")
    print("   - BULLS: Correct digit, correct spot.")
    print("   - COWS: Correct digit, but wrong spot.")
    input("\nPress Enter to begin...")
    clear_screen()

def is_valid_5_digit_unique(entry):
    """Checks if the input is exactly 5 unique digits."""
    return len(entry) == 5 and entry.isdigit() and len(set(entry)) == 5

def get_valid_input(prompt, is_secret=False):
    """Ensures the player enters a valid 5-digit unique code."""
    while True:
        if is_secret:
            entry = getpass.getpass(prompt)
        else:
            entry = input(prompt)
            
        if is_valid_5_digit_unique(entry):
            return entry
        print("Invalid! Must be 5 digits with NO repetitions (e.g., 12345).")

def play_round(setter, guesser):
    print(f"\n{setter}, enter your secret 5-digit code.")
    secret = get_valid_input(f"Secret code (hidden): ", is_secret=True)
    clear_screen()
    
    print(f"--- {guesser}'s Turn to Guess! ---")
    attempts = 0
    
    while True:
        attempts += 1
        guess = get_valid_input(f"Attempt {attempts} - {guesser}: ")
        
        if guess == secret:
            print(f"BINGO! {guesser} cracked the code in {attempts} tries!")
            return attempts
        
        # Logic for 5-digit unique bulls and cows
        bulls = sum(1 for i in range(5) if guess[i] == secret[i])
        # Since digits are unique, cows is just common digits minus bulls
        cows = len(set(guess) & set(secret)) - bulls
        
        print(f">> {bulls} Bulls, {cows} Cows")

def main():
    clear_screen()
    print("Welcome to Mastermind-Mania (5-Digit Edition)")
    if input("View instructions? (y/n): ").lower() == 'y':
        show_instructions()
        
    p1 = input("Enter Name for Player 1: ") or "Player 1"
    p2 = input("Enter Name for Player 2: ") or "Player 2"
    
    scores = {p1: 0, p2: 0}
    
    while True:
        # Round A
        print(f"\n--- MATCH START: {p1} vs {p2} ---")
        p2_score = play_round(p1, p2)
        
        # Round B
        print(f"\n--- {p2} is now the Setter ---")
        p1_score = play_round(p2, p1)
        
        # Winner calculation for the match
        if p1_score < p2_score:
            print(f"\nWINNER: {p1}!")
            scores[p1] += 1
        elif p2_score < p1_score:
            print(f"\nWINNER: {p2}!")
            scores[p2] += 1
        else:
            print("\nIt's a DRAW!")
            
        print(f"OVERALL MATCHES WON -> {p1}: {scores[p1]} | {p2}: {scores[p2]}")
        
        if input("\nPlay another match? (y/n): ").lower() != 'y':
            break

    print("Thanks for playing!")

if __name__ == "__main__":
    main()