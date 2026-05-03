import streamlit as st

# --- 1. INITIALIZATION (The App Memory) ---
if "phase" not in st.session_state:
    st.session_state.phase = "setup"  # setup, p1_set, p2_guess, p2_set, p1_guess, results
    st.session_state.p1_name = "Player 1"
    st.session_state.p2_name = "Player 2"
    st.session_state.secret_code = ""
    st.session_state.p1_tries = 0
    st.session_state.p2_tries = 0
    st.session_state.current_attempts = 0
    st.session_state.history = []

def is_valid(code):
    return len(code) == 5 and code.isdigit() and len(set(code)) == 5

def calculate_feedback(guess, secret):
    bulls = sum(1 for i in range(5) if guess[i] == secret[i])
    cows = len(set(guess) & set(secret)) - bulls
    return bulls, cows

# --- 2. HEADER & INSTRUCTIONS ---
st.title("🧩 Mastermind-Mania: 5-Digit Pro")
with st.expander("Show How to Play"):
    st.write("""
    - **Bulls**: Correct digit in the correct spot.
    - **Cows**: Correct digit in the wrong spot.
    - **Rules**: Codes must be 5 digits and NO repetitions.
    """)

# --- 3. GAME PHASES ---

# PHASE: SETUP NAMES
if st.session_state.phase == "setup":
    st.header("Who is playing?")
    st.session_state.p1_name = st.text_input("Player 1 Name", st.session_state.p1_name)
    st.session_state.p2_name = st.text_input("Player 2 Name", st.session_state.p2_name)
    if st.button("Start Game"):
        st.session_state.phase = "p1_set"
        st.rerun()

# PHASE: P1 SETS CODE
elif st.session_state.phase == "p1_set":
    st.header(f"{st.session_state.p1_name}, set your secret code")
    code = st.text_input("Enter 5 unique digits:", type="password", help="Hide this from your opponent!")
    if st.button("Lock Secret Code"):
        if is_valid(code):
            st.session_state.secret_code = code
            st.session_state.phase = "p2_guess"
            st.session_state.current_attempts = 0
            st.session_state.history = []
            st.rerun()
        else:
            st.error("Invalid code! Must be 5 unique digits.")

# PHASE: P2 GUESSES
elif st.session_state.phase == "p2_guess":
    st.header(f"{st.session_state.p2_name}'s Turn to Guess")
    guess = st.text_input(f"Enter Guess #{st.session_state.current_attempts + 1}", max_chars=5)
    
    if st.button("Submit Guess"):
        if is_valid(guess):
            st.session_state.current_attempts += 1
            if guess == st.session_state.secret_code:
                st.session_state.p2_tries = st.session_state.current_attempts
                st.session_state.phase = "p2_set"
                st.balloons()
                st.success(f"Correct! {st.session_state.p2_name} took {st.session_state.p2_tries} tries.")
                st.button("Continue to Next Round")
            else:
                b, c = calculate_feedback(guess, st.session_state.secret_code)
                st.session_state.history.append(f"Guess: {guess} | Bulls: {b}, Cows: {c}")
        else:
            st.error("Invalid guess!")

    for h in reversed(st.session_state.history):
        st.write(h)

# PHASE: P2 SETS CODE
elif st.session_state.phase == "p2_set":
    st.header(f"{st.session_state.p2_name}, set your secret code")
    code = st.text_input("Enter 5 unique digits:", type="password")
    if st.button("Lock Secret Code"):
        if is_valid(code):
            st.session_state.secret_code = code
            st.session_state.phase = "p1_guess"
            st.session_state.current_attempts = 0
            st.session_state.history = []
            st.rerun()
        else:
            st.error("Invalid code!")

# PHASE: P1 GUESSES
elif st.session_state.phase == "p1_guess":
    st.header(f"{st.session_state.p1_name}'s Turn to Guess")
    guess = st.text_input(f"Enter Guess #{st.session_state.current_attempts + 1}", max_chars=5)
    
    if st.button("Submit Guess"):
        if is_valid(guess):
            st.session_state.current_attempts += 1
            if guess == st.session_state.secret_code:
                st.session_state.p1_tries = st.session_state.current_attempts
                st.session_state.phase = "results"
                st.balloons()
                st.rerun()
            else:
                b, c = calculate_feedback(guess, st.session_state.secret_code)
                st.session_state.history.append(f"Guess: {guess} | Bulls: {b}, Cows: {c}")
    
    for h in reversed(st.session_state.history):
        st.write(h)

# PHASE: FINAL RESULTS
elif st.session_state.phase == "results":
    st.header("🏆 Final Results")
    st.write(f"{st.session_state.p1_name}: {st.session_state.p1_tries} attempts")
    st.write(f"{st.session_state.p2_name}: {st.session_state.p2_tries} attempts")
    
    if st.session_state.p1_tries < st.session_state.p2_tries:
        st.success(f"{st.session_state.p1_name} Wins!")
    elif st.session_state.p2_tries < st.session_state.p1_tries:
        st.success(f"{st.session_state.p2_name} Wins!")
    else:
        st.info("It's a Tie!")
    
    if st.button("Play Again"):
        st.session_state.phase = "setup"
        st.rerun()