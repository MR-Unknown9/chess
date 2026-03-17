import customtkinter as ctk
import chess
import os
import datetime


class ChessApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CHESS OS v1.0")
        self.geometry("700x800")
        ctk.set_appearance_mode("dark")

        # Container to hold the different screens
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)

        self.show_home_screen()

    def show_home_screen(self):
        # Clear the container
        for widget in self.container.winfo_children():
            widget.destroy()

        # --- HOME SCREEN UI ---
        title = ctk.CTkLabel(
            self.container, text="WELCOME TO CHESS OS", font=("Arial", 32, "bold")
        )
        title.pack(pady=(100, 20))

        subtitle = ctk.CTkLabel(
            self.container, text="Select an option to begin", font=("Arial", 16)
        )
        subtitle.pack(pady=10)

        start_btn = ctk.CTkButton(
            self.container,
            text="New Game",
            width=250,
            height=50,
            font=("Arial", 18),
            command=self.start_new_game,
        )
        start_btn.pack(pady=10)

        history_btn = ctk.CTkButton(
            self.container,
            text="View History Folder",
            width=250,
            height=50,
            font=("Arial", 18),
            fg_color="transparent",
            border_width=2,
            command=self.show_history_screen,
        )
        history_btn.pack(pady=10)

        exit_btn = ctk.CTkButton(
            self.container,
            text="Quit OS",
            width=250,
            height=50,
            font=("Arial", 18),
            fg_color="#444",
            hover_color="#666",
            command=self.quit,
        )
        exit_btn.pack(pady=10)

    def start_new_game(self):
        self.setup_game_screen()

    def setup_game_screen(self):
        # Clear the container
        for widget in self.container.winfo_children():
            widget.destroy()

        # Initialize Game Logic
        self.board = chess.Board()
        self.move_history = []

        # --- GAME SCREEN UI ---
        # Back Button
        back_btn = ctk.CTkButton(
            self.container, text="← Menu", width=80, command=self.show_home_screen
        )
        back_btn.pack(anchor="nw", padx=10, pady=10)

        self.board_label = ctk.CTkLabel(
            self.container, text=self.board.unicode(), font=("Courier New", 40)
        )
        self.board_label.pack(pady=20)

        self.info_label = ctk.CTkLabel(
            self.container, text="Material: Equal", font=("Arial", 16)
        )
        self.info_label.pack(pady=5)

        self.entry = ctk.CTkEntry(
            self.container, placeholder_text="Enter move (e.g. e4)", width=200
        )
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda event: self.handle_move())

        self.history_box = ctk.CTkTextbox(self.container, width=500, height=100)
        self.history_box.pack(pady=10)

        # Save / End buttons
        btn_frame = ctk.CTkFrame(self.container)
        btn_frame.pack(pady=10)

        save_btn = ctk.CTkButton(btn_frame, text="Save Game", command=self.save_game)
        save_btn.grid(row=0, column=0, padx=5)

        finish_btn = ctk.CTkButton(
            btn_frame, text="End Game", command=self.show_home_screen
        )
        finish_btn.grid(row=0, column=1, padx=5)

    def show_history_screen(self):
        # 1. Clear the screen
        for widget in self.container.winfo_children():
            widget.destroy()

        # 2. Setup UI
        back_btn = ctk.CTkButton(
            self.container, text="← Menu", width=80, command=self.show_home_screen
        )
        back_btn.pack(anchor="nw", padx=10, pady=10)

        # 3. GET THE CORRECT PATH
        # This finds the directory where board.py lives
        script_dir = os.path.dirname(os.path.abspath(__file__))
        history_folder = os.path.join(script_dir, "history")
        file_path = os.path.join(history_folder, "matches.txt")

        # 4. Display Logic
        history_display = ctk.CTkTextbox(self.container, width=600, height=500)
        history_display.pack(pady=10, padx=20)

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                history_display.insert("0.0", content)
        else:
            # Debug message to show you exactly where it is looking
            history_display.insert("0.0", f"Error: No file found at:\n{file_path}")

        history_display.configure(state="disabled")

    def calculate_material(self):
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
        leader = "White" if diff > 0 else "Black"
        return f"Advantage: {leader} (+{abs(diff)})"

    def format_history(self):
        formatted = ""
        for i in range(0, len(self.move_history), 2):
            move_num = (i // 2) + 1
            w_move = self.move_history[i]
            b_move = (
                self.move_history[i + 1] if (i + 1) < len(self.move_history) else ""
            )
            formatted += f"{move_num}. {w_move} {b_move} "
        return formatted.strip()

    def save_game(self):
        # Save to a history folder located next to this script (same logic used by show_history_screen)
        script_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(script_dir, "history")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, "matches.txt")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        history_str = self.format_history()

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- Game on {timestamp} ---\n{history_str}\n")
        print(f"💾 Saved to {file_path}")

    def handle_move(self):
        move_text = self.entry.get().strip()
        if not move_text:
            return

        try:
            move = self.board.parse_san(move_text)
            # Record the SAN before updating the board, to keep the notation correct
            san = self.board.san(move)
            self.board.push(move)
            self.move_history.append(san)

            # Update UI
            self.board_label.configure(text=self.board.unicode())
            self.info_label.configure(text=self.calculate_material())
            self.history_box.delete("0.0", "end")
            self.history_box.insert("0.0", " ".join(self.move_history))
            self.entry.delete(0, "end")
            self.entry.configure(border_color="")

            # Auto-save on game end
            if self.board.is_game_over():
                self.save_game()
                self.info_label.configure(text=f"Game Over: {self.board.result()}")
        except Exception:
            self.entry.configure(border_color="red")


if __name__ == "__main__":
    app = ChessApp()
    app.mainloop()
