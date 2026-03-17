# ♟️ Chess OS: The "I Swear It Works" Edition

Welcome to my Chess app. It used to be a messy 500-line terminal script that made my brain melt, so I asked an AI to "modularize" it. Now it has multiple files and a Home Screen. We're professional now.

## 📁 Why are there so many files?

To stop the "dizzy brain" feeling.

* **`main.py`**: The Manager. Switches screens so you don't have to restart the app like it's 1995.
* **`logic.py`**: The Brain. Does the math, saves the games, and handles the "Illegal Move" red box of shame.
* **`screens.py`**: The Designer. Handles the Home and History screens so they don't clutter the actual game.

---

## 🛠️ The "It Crashed" Fix

If you're on Linux, Python is missing its "eyes" (Tkinter).

**Run this or it won't open:**

```bash
sudo apt update && sudo apt install python3-tk
```

**Then grab the goods:**

```bash
pip install -r requirements.txt
```

---

## 🕹️ Pro Tips

* **Input**: Use Algebraic Notation (`e4`, `Nf3`). If the box turns **red**, you messed up.
* **History**: Saved to `/history/matches.txt` using Absolute Paths. The app knows where it lives, even if you don't.
* **Status**: It’s modular. It’s dark mode. It’s "AI Generated" (obviously).

---

## 📝 The "Maybe Someday" List

* [ ] A **Reset** button (so I can rage-quit faster).

* [ ] Actual **PNG images** (because Unicode pieces look like Tetris blocks).
* [ ] An **AI Opponent** (that actually tries).

---
*Disclaimer: No Grandmasters were harmed in the making of this spaghetti code.*
