# CmdEcho

CmdEcho is a terminal-based flashcard app for practicing and memorizing shell commands using the **Active Recall** learning technique.

## What is Active Recall?

Active Recall is a powerful study method where, instead of just reading or reviewing notes, you try to retrieve the answer from memory. 
This method has been shown to improve retention and understanding much more effectively than passive review.

## Features

- Practice shell commands with flashcard decks
- Tracks your previous scores for each deck
- Mark answers as correct or incorrect manually
- Skip questions you don’t know
- Arrow key navigation in menus and while editing answers

## Getting Started

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/CmdEcho.git
cd CmdEcho
```

### 2. Install dependencies

Make sure you have Python 3.7+ installed.  
Install required packages:

```sh
pip install -r requirements.txt
```

### 3. Run the app

```sh
python main.py
```

### 4. Using CmdEcho

- Use the arrow keys to select a deck and press Enter.
- Type your answer and press Enter.
- Mark your answer as correct (→) or incorrect (←) using the arrow keys.
- Press `?` to skip a question.
- Your previous scores are saved and shown in the menu.

### 5. Adding Decks

Add new decks as `.json` files in the `decks/` folder. Each deck is a list of cards with `"front"` and `"back"` fields.

Example:
```json
[
  {"front": "How do you list files?", "back": "ls"}
]
```

---

Thank you for using CmdEcho!  
If you have suggestions or want to contribute a new deck, feel free to open an issue or pull request.
