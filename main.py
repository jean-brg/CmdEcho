# IMPORTS
import curses
import json
import os
from blessed import Terminal
import random
from collections import deque
import readline

# VARIABLES
term = Terminal()
SCORE_FILE_PATH = "./scores.json"

# DECK FUNCTIONS
def listDecks(folder='decks'):
    return [f for f in os.listdir(folder) if f.endswith('.json')]

def loadDeck(deckPath):
    with open(deckPath, 'r') as f:
        return json.load(f)
    
# SCORE FUNCTIONS
def loadScores():
    if not os.path.exists(SCORE_FILE_PATH):
        return {}
    with open(SCORE_FILE_PATH, "r") as scoreFile:
        return json.load(scoreFile)

def saveScores(scores):
    with open(SCORE_FILE_PATH, "w") as scoreFile:
        json.dump(scores, scoreFile)

# MAIN FUNCTIONS
def study(deck):
    random.shuffle(deck)
    streak = 0
    isGameRunning = True
    cardQueue = deque(deck)
    seenCount = 0
    correct = 0
    total = len(deck)

    while cardQueue and isGameRunning:
        card = cardQueue.popleft()
        isCardMarked = False

        while not isCardMarked:
            print(term.clear())
            print(term.bold(f"{seenCount + 1}/{len(deck)} 🔥 {streak}\n"))
            print(term.bold(card["front"]))
            print("> ", end='', flush=True)
            userAnswer = input()

            isCorrect = userAnswer.strip() == card["back"].strip()

            print(term.clear())
            print(term.bold(f"{seenCount + 1}/{len(deck)} 🔥 {streak}\n"))
            print(card["front"])
            print(f"> {userAnswer}")
            print()

            if userAnswer.strip() == "?":
                print(f"> {term.yellow(card['back'])}")
                input("\nSkipped - Press Enter to continue")
                cardQueue.append(card)
                break
            elif isCorrect:
                print(f"> {term.green(card['back'])}")
            else:
                print(f"> {term.red(card['back'])}")

            print("\nMark wrong: ← | Mark right: → | q to quit")
            with term.cbreak():
                key = term.inkey()
                if key.name == 'KEY_RIGHT':
                    streak += 1
                    isCardMarked = True
                    seenCount += 1
                    correct += 1
                elif key.name == 'KEY_LEFT':
                    streak = 0
                    isCardMarked = True
                    seenCount += 1
                elif key == 'q':
                    isGameRunning = False
                    break
    return f"{correct}/{total}"

def menu(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.curs_set(0)
    stdscr.keypad(True)

    decks = listDecks()
    options = [os.path.splitext(d)[0] for d in decks] + ["Exit"]
    currentSelection = 0
    scores = loadScores()

    while True:
        stdscr.clear()

        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(1, 0, "EchoRecall")
        stdscr.attroff(curses.A_BOLD)
        stdscr.addstr(2, 0, "The essay way to practice and study shell commands\n")

        for i, option in enumerate(options):
            y = 4 + i
            score_str = ""
            if option != "Exit":
                deck_file = decks[i]  # i matches decks index
                prev_score = scores.get(deck_file)
                if prev_score is not None:
                    score_str = f" (Prev: {prev_score})"
            if i == currentSelection:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(y, 0, f"{i + 1}. {option}{score_str}")
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(y, 0, f"{i + 1}. {option}{score_str}")

        stdscr.addstr(6 + i, 0, "Use ↑ ↓ to choose a deck. Press ENTER to select a deck.")
        stdscr.addstr(7 + i, 0, "When practicing, you can write \"?\" to pass the question.")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_UP and currentSelection > 0:
            currentSelection -= 1
        elif key == curses.KEY_DOWN and currentSelection < len(options) - 1:
            currentSelection += 1
        elif key in [curses.KEY_ENTER, 10, 13]:
            if options[currentSelection] == "Exit":
                return None
            else:
                return os.path.join('decks', decks[currentSelection])


# EXECUTION
def main():
    scores = loadScores()
    while True:
        selectedDeckPath = curses.wrapper(menu)
        if not selectedDeckPath:
            break

        deck = loadDeck(selectedDeckPath)
        with term.fullscreen(), term.hidden_cursor():
            score = study(deck)
        # Save score
        deck_file = os.path.basename(selectedDeckPath)
        scores[deck_file] = score
        saveScores(scores)

if __name__ == "__main__":
    main()

# Prevent arrow keys from being printed