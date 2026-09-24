# **# 🎮 Game Glitch Investigator: The Impossible Guesser**

**## 🚨 The Situation**

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

**## 🛠️ Setup**

1\. Install dependencies: `pip install -r requirements.txt`
2\. Run the broken app: `python -m streamlit run app.py`

**## 🕵️‍♂️ Your Mission**

1\. ****Play the game.**** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2\. ****Find the State Bug.**** Why does the secret number change every time you click "Submit"? Ask ChatGPT: **"How do I keep a variable from resetting in Streamlit when I click a button?"**
3\. ****Fix the Logic.**** The hints ("Higher/Lower") are wrong. Fix them.
4\. ****Refactor & Test.**** - Move the logic into `logic_utils.py`.
- Run `pytest` in your terminal.
- Keep fixing until all tests pass!

**## 📝 Document Your Experience**

- [x] Describe the game's purpose.
The games purpose is to generate a secret number, and allow the player to make a limited number of attempts to guess the number.
- [x] Detail which bugs you found.
  - game does not restart
  - hints number is higher/lower incorrectly in the opposite direction.
  - negative numbers are allowed even though it filters out strings, rounds decimals
  - number of allowed attempts is lower than indicated by game and are indicated incorrectly
  - on alternating guesses the game would have altering behavior in allowed guesses and also scoring.
- [x] Explain what fixes you applied.
  * "New Game" now resets status to "playing" and clears history 
  * Swapped the messages in check_guess so guessing too high now says "Go LOWER" and too low says "Go HIGHER".
  * Function parse_guess now takes low/high and rejects any parsed value outside that range, not just non-numeric strings.
  * Attempts now start at 0 and only increment on a *valid* parsed guess, and the "Attempts left" message is refreshed after each guess.
  * Removed the attempts % 2 branches that alternated behavior on correct guesses and scoring.
  

**## 📸 Demo Walkthrough**

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

**## Demo Walkthrough**
1\. User enters a guess of 40
2\. Game returns "Too Low"
3\. User enters a guess of 70, and the game shows "Too High"
4\. Score updates correctly after each guess
5\. Game ends after the correct guess

****Screenshot**** **(optional)**: <!-- Insert a screenshot of your fixed, winning game here -->

**## 🧪 Test Results**

```
================================================================ test session starts ================================================================
platform darwin -- Python 3.12.7, pytest-7.4.4, pluggy-1.0.0
rootdir: ***/CodePath_AI110/ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.9.0, ddtrace-3.3.0, dash-3.1.0
collected 25 items                                                                                                                                  

tests/test_game_logic.py .........................                                                                                            [100%]

================================================================ 25 passed in 0.01s =================================================================
```

**## 🚀 Stretch Features**

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]

