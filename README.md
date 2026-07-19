## Overview

A chess engine and playable game built from scratch in Python — no external chess
libraries. It implements full move generation, check/checkmate detection, pin
detection, castling-free legal moves, pawn promotion, and FEN parsing, along with
a simple minimax + alpha-beta bot and a Pygame GUI.

## Features

- **Full rule engine** (`Engine.py`): `Piece` subclasses for King, Queen, Rook,
  Bishop, Knight, and Pawn, each with their own legal-move generation.
- **Check, checkmate & pin detection**: moves that would leave your own king in
  check are filtered out; `is_checkmate()` checks for escape squares, blocks, and
  captures.
- **FEN support**: positions can be loaded from a FEN string via `process_fen`.
- **Pawn promotion**: pawns automatically promote to a Queen on reaching the last
  rank.
- **Move search** (`main.py`): a minimax search with alpha-beta pruning
  (`Node`, `expand_to_depth`, `minimax`) that evaluates positions by material
  count (`HelperMethods.evaluate_position`), used to drive a simple bot.
- **Graphical interface** (`graphical_interface.py`): a Pygame board renderer
  with piece sprites and a text input box for entering moves in algebraic
  notation (e.g. `e2-e4`).

## Dependencies

- Python 3
- [pygame](https://www.pygame.org/) 2.6.1

## Installation

```bash
pip install -r requirements.txt
```

## Running the game

**Play against the bot in the terminal** (you play White, the bot plays Black):

```bash
python main.py
```

Enter moves in algebraic notation, e.g. `e2-e4`.

**Play with the graphical interface:**

```bash
python graphical_interface.py
```

Click the input box, type a move in algebraic notation (e.g. `e2-e4`), and press
Enter.

## File Structure

- `Engine.py` — Core chess engine: `Piece` classes, `Board`, and `ChessGame`
  (move validation, check/checkmate logic, FEN parsing).
- `HelperMethods.py` — Legal move aggregation across a whole side
  (`GetAllLegalMoves`), material counting, and position evaluation.
- `main.py` — Minimax + alpha-beta search and the human-vs-bot terminal game
  loop.
- `graphical_interface.py` — Pygame-based GUI and algebraic notation parsing.
- `pieces-basic-png/` — Piece sprite images used by the GUI.
- `chess_icon.png` — Window icon for the GUI.
- `requirements.txt` — Python dependencies.
