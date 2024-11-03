import streamlit as st
import random

st.set_page_config(page_title="RPS game", page_icon="✊📄✂️")

st.title("Rock-Paper-Scissors Game")
st.write("Play against the computer and see if you can win the best of three!")

# Emojis for rock, paper, scissors
emojis = {"Rock": "✊", "Paper": "📄", "Scissors": "✂️"}
options = list(emojis.keys())

# Initialize session state variables for score tracking
if 'user_score' not in st.session_state:
    st.session_state.user_score = 0
if 'computer_score' not in st.session_state:
    st.session_state.computer_score = 0
if 'round_number' not in st.session_state:
    st.session_state.round_number = 1

# User's choice
user_choice = st.selectbox("Choose your move:", options)

# Play button to start each round
if st.button("Play!"):
    # Computer randomly chooses
    computer_choice = random.choice(options)
    
    # Display choices
    st.write(f"### You chose: {emojis[user_choice]} {user_choice}")
    st.write(f"### Computer chose: {emojis[computer_choice]} {computer_choice}")
    
    # Determine the winner
    if user_choice == computer_choice:
        st.write("It's a tie! 🤝")
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        st.write("You win this round! 🎉")
        st.session_state.user_score += 1
    else:
        st.write("Sorrey u lose! womp, womp, womp... 😢")
        st.session_state.computer_score += 1
    
    # Update round number
    st.session_state.round_number += 1

    # Check for best of three
    if st.session_state.user_score == 2:
        st.balloons()
        st.write("### Ayee! 🎉 You won the best of three!")
        st.session_state.user_score = 0
        st.session_state.computer_score = 0
        st.session_state.round_number = 1
    elif st.session_state.computer_score == 2:
        st.write("### Sorry, maybe u r out of luck😢")
        st.session_state.user_score = 0
        st.session_state.computer_score = 0
        st.session_state.round_number = 1

# Display the scores and round number
st.write(f"### Round: {st.session_state.round_number}")
st.write(f"Your Score: {st.session_state.user_score} | Computer Score: {st.session_state.computer_score}")

# Reset button to start over
if st.button("Reset Game"):
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.round_number = 1
    st.write("Game reset! Good luck!")

