# War Card Game

## Student Name
Chase McKenna

## App Description
War: The Card Game is an interactive, single-player version of the classic two-player card game. The user plays against the computer, drawing one card per round. The higher rank collects both cards, and tied ranks trigger the usual War tie-break. The app tracks the piles, displays the latest result and recent rounds, and ends when a player runs out of cards or the selected round limit is reached.

## Intended Users
This app is intended for people who want to play a quick, familiar card game in a web browser, including students learning to build simple interactive apps with Streamlit.

## Current Features
- Casino-style table design with a green felt theme, gold accents and custom fonts.
- Fully illustrated 52-card deck drawn as vector art (pips, aces and mirrored court cards) in `cards.py`, with no image files needed.
- Four selectable card-back designs (Crimson, Royal Blue, Emerald, Onyx).
- Animated card dealing, a glowing highlight for the winning card and a shaking "WAR" badge on ties.
- War rounds show the face-down cards and the revealed tie-breaker for every war in a chain.
- Scoreboard with live pile stacks, card counts, a share-of-deck bar and the war tally.
- Flip one round, play 10 at a time, or skip straight to the end.
- Momentum chart of both piles over time, a round log with mini cards and a stats panel (win rate, best streak, biggest pot).
- Match record (wins, losses, ties) kept across games in the same visit, with a celebration when you win.

## Running the App
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Features Still Planned
- Add a published online version so players can access the game without running it locally.
- Add optional sound effects for flips and wars.
