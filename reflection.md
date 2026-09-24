# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game looked fine enough, but was not playable. Multiple issues caused it to be impossible to play. 
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  
  - game does not restart
  - hints number is higher/lower incorrectly in the opposite direction.
  - negative numbers are allowed even though it filters out strings, rounds decimals
  - number of allowed attempts is lower than indicated by game and are indicated incorrectly
  - sometimes doesn’t accept correct guess


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input   | Expected Behavior  | Actual Behavior                | Console Output / Error |
|---------|--------------------|--------------------------------|------------------------|
| 105     | hint lower/reject  | hints guess needs to be higher |                        |
| fiuhfgi | reject completely  | rejects, but uses attempt      |                        |
| -10     | hint higher/reject | hints guess needs to be lower  |                        |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude in VS code as my buddy.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
I hinted to Claude that the hints were incorrect, and while looking at the program, Claude caught the issue with changing behavior alternating on even or odd guesses. Claude indicated that this would result in correct guesses not being accepted on even guesses. This behavior explained some of the behavior I observed, and appeared resolved after implementing Claude’s suggested fix.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
Claude suggested moving the ‘submit guesses’ button in response to an issue with submitting guesses taking two guesses. This did not make any sense to me, but I am not familiar with Streamlit apps. I initially rejected it, prompted Claude to explain the change first. It gave an explanation about the behevior of buttons on the page that made more sense. I re-prompted Claude to make the change. I verified the change as a user that the two-click behavior was changed. 
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
By re-enacting the behavior that triggered the bugs.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
When testing string inputs clogging the guess history, I referred to the Developer Debug Info panel. It showed me that string inputs were not being added, but were still counting attempts. 
- Did AI help you design or understand any tests? How?
Yea, it helped me design some tests. I asked it to create tests for edge conditions, hints, and input handling which is handled with ease. However, my input handling strictly enforces a positive range and it did try to create some tests around higher/lower messages within the negative range. 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
I had to ask Claude with this because these are details that I did not look into while working on the project. Streamlit “reruns” are basically restarting (or re-running) the application files. This includes any variables that were set. Meanwhile session state is an object that persist between these runs that preserves variables that you may want to keep between runs such as our secret number.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
I absolutely love using AI to generate tests. It removes the least enjoyable part of a project for me and maintains a flow of thought of me asking myself “what could go wrong?”.
- What is one thing you would do differently next time you work with AI on a coding task?
It was really easy to jump into this project and start telling it what to do and accept changes that appeared reasonable enough. My issue with it is not being familiar with the code at all does make that review before accepting just a little less confident. I think reviewing the code, or having my AI assistant give me a high-level overview first could boost my confidence in allowing different changes.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
Not strictly the project, but the class so far has both improved my view of AI generated code, and made me weary. While it usually generates code that works, it can also lend itself to more convoluded workarounds resulting in overly complex code that can make troubleshooting more confusing, even with the assistance of AI.