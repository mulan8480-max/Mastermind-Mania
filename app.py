import streamlit as st
import random
from collections import Counter

# 1. Setup Page Config
st.set_page_config(page_title="Mastermind Mania", page_icon="🔐")

def play_mastermind_mania():
    st.title("Welcome to Mastermind Mania!")
    st.subheader("BY: JESS TORRES")
    
    # 2. Initialize Game State (The "Memory" of the app)
    if 'secret_number' not in st.session_state:
        all_digits = list(range(10))
        random.shuffle(all_digits)
        if all_digits[0] == 0:
            all_digits[0], all_digits[1] = all_digits[1], all_digits[0]
        st.session_state.secret_number = "".join(map(str, all_digits[:5]))
        st.session_state.history = []
        st.session_state.attempts = 0
        st.session_state.game_over = False

    st.write("I have a secret 5-digit number with unique digits. Try to guess it!")
    
    # 3. Game UI
    if not st.session_state.game_over:
        guess = st.text_input(f"Attempt {st.session_state.attempts + 1}/12 - Enter 5 unique digits:", key="game_input")

        if len(guess) == 5 and guess.isdigit():
            if st.button("Submit Guess"):
                st.session_state.attempts += 1
                
                # Scoring Logic
                a_count = 0
                b_count = 0
                secret = st.session_state.secret_number
                s_counts = Counter(secret)
                
                for i in range(5):
                    if guess[i] == secret[i]:
                        a_count += 1
                        s_counts[guess[i]] -= 1
                
                for i in range(5):
                    if guess[i] != secret[i] and s_counts.get(guess[i], 0) > 0:
                        b_count += 1
                        s_counts[guess[i]] -= 1
                
                result = f"Guess: {guess} | Result: {a_count}A, {b_count}B"
                st.session_state.history.append(result)

                if guess == secret:
                    st.success(f"EXCELLENT! You cracked the code: {secret}")
                    st.session_state.game_over = True
                elif st.session_state.attempts >= 12:
                    st.error(f"GAME OVER. The code was {secret}")
                    st.session_state.game_over = True
        elif len(guess) > 0 and (len(guess) != 5 or not guess.isdigit()):
            st.warning("Please enter exactly 5 digits.")

    # 4. Display History & Reset
    if st.session_state.history:
        st.write("### Guess History")
        for h in reversed(st.session_state.history):
            st.text(h)

    if st.session_state.game_over:
        if st.button("Play Again"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# Start the game
if __name__ == "__main__":
    play_mastermind_mania()