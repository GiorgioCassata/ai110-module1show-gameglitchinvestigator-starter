import random
import streamlit as st

#FIX: moved game logic out of app.py and into logic_utils.py so it can be unit tested
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    #FIX: start attempts at 0 instead of 1 to avoid an off-by-one on the attempt count
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

#FIX: use st.empty() as a placeholder so this message can be refreshed after each guess
# instead of only showing the stale value from the initial page render
attempts_info = st.empty()
#FIX: show the actual difficulty range (low/high) instead of a hardcoded "1 and 100"
attempts_info.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

#FIX: wrap the guess input and submit button in a form so pressing Enter submits the guess
with st.form("guess_form"):
    raw_guess = st.text_input(
        "Enter your guess:",
        key=f"guess_input_{difficulty}"
    )
    submit = st.form_submit_button("Submit Guess 🚀")

col1, col2 = st.columns(2)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)


if new_game:
    st.session_state.attempts = 0
    #FIX: use the current difficulty's low/high instead of a hardcoded 1-100 range
    st.session_state.secret = random.randint(low, high)
    #FIX: reset status and history too, so a previous win/loss doesn't carry over
    # into the new game
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:

    #FIX: pass low/high so parse_guess can reject out-of-range guesses
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        #FIX: don't append invalid raw input to history, and don't count it as an attempt
        st.error(err)
    else:
        #FIX: only increment attempts once the guess has been successfully parsed,
        # so invalid input no longer consumes an attempt
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        #FIX: always compare against the int secret; previously every other attempt
        # compared against str(secret), which broke the guess comparison
        secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

    #FIX: refresh the attempts-left message after each guess instead of leaving
    # the placeholder showing its initial value
    attempts_info.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {max(attempt_limit - st.session_state.attempts, 0)}"
    )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
