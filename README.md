# Password Generator

A Python desktop app (tkinter) that creates strong random passwords, so you don't waste time thinking of one.

## Features

- Length slider (4-64)
- Choose character types: uppercase, lowercase, numbers, symbols
- Edit exactly which symbols are allowed (with a Reset button)
- Option to avoid look-alike characters (`I l 1 O 0`)
- Option for no repeated characters
- Strength label (Weak / Fair / Strong / Very strong)
- One-click Copy button
- Uses Python's `secrets` module for cryptographically secure randomness

## Run

Requires Python 3 with tkinter (Tk) support.

```
python3 passwordgenerator.py
```

If you get `No module named '_tkinter'`, install Tk for your Python (on macOS with Homebrew: `brew install python-tk`).

## Files

- `passwordgenerator.py` - current version
- `password_generator_v1.py` - original version (length + repetition only)
