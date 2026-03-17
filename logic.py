import chess
import os
import datetime


class ChessLogic:
    def __init__(self):
        self.board = chess.Board()
        self.move_history = []

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
            return "Equal"
        return f"+{diff}" if diff > 0 else f"{diff}"

    def save_to_file(self, history_str):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(script_dir, "history")
        if not os.path.exists(folder):
            os.makedirs(folder)

        path = os.path.join(folder, "matches.txt")
        with open(path, "a", encoding="utf-8") as f:
            f.write(
                f"\n[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] {history_str}\n"
            )
