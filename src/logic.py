import chess
import os
import datetime


class ChessLogic:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.board = chess.Board()
        self.move_history = []

    def get_history_path(self):
        # Go up one level from 'src' to the root, then into 'history'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(current_dir)
        history_dir = os.path.join(root_dir, "history")

        if not os.path.exists(history_dir):
            os.makedirs(history_dir)
        return os.path.join(history_dir, "matches.txt")

    def get_material_score(self):
        values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
        }
        w = sum(len(self.board.pieces(pt, chess.WHITE)) * v for pt, v in values.items())
        b = sum(len(self.board.pieces(pt, chess.BLACK)) * v for pt, v in values.items())
        diff = w - b
        if diff == 0:
            return "Material: Equal"
        return f"Advantage: {'White' if diff > 0 else 'Black'} (+{abs(diff)})"

    def save_game(self):
        if not self.move_history:
            return
        path = self.get_history_path()
        timestamp = datetime.datetime.now().strftime("%b %d, %Y | %H:%M")

        # --- THE COUNTER LOGIC ---
        numbered_moves = []
        for i in range(0, len(self.move_history), 2):
            move_num = (i // 2) + 1
            white_move = self.move_history[i]
            # Check if Black actually made a move yet
            black_move = (
                self.move_history[i + 1] if (i + 1) < len(self.move_history) else ""
            )
            numbered_moves.append(f"{move_num}. {white_move} {black_move}")

        full_move_text = " ".join(numbered_moves)
        # -------------------------

        entry = (
            f"┌──────────────────────────────────────────────────┐\n"
            f"  📅 MATCH: {timestamp}\n"
            f"  📜 MOVES: {full_move_text}\n"
            f"└──────────────────────────────────────────────────┘\n\n"
        )

        with open(path, "a", encoding="utf-8") as f:
            f.write(entry)
