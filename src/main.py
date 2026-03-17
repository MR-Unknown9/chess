import customtkinter as ctk
from logic import ChessLogic
import screens

class ChessApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CHESS OS")
        self.geometry("700x800")
        ctk.set_appearance_mode("dark")
        
        self.logic = ChessLogic()
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        self.switch_screen("home")

    def switch_screen(self, name):
        for child in self.container.winfo_children():
            child.destroy()

        if name == "home":
            screens.show_home(self.container, lambda: self.switch_screen("game"), lambda: self.switch_screen("history")).pack(fill="both", expand=True)
        elif name == "history":
            screens.show_history(self.container, lambda: self.switch_screen("home")).pack(fill="both", expand=True)
        elif name == "game":
            self.setup_game_ui()

    def setup_game_ui(self):
        self.logic.reset_game()
        
        # UI Elements
        ctk.CTkButton(self.container, text="← QUIT", width=80, fg_color="#722", command=self.quit_and_save).pack(anchor="nw", padx=10, pady=10)
        
        self.score_label = ctk.CTkLabel(self.container, text="Material: Equal", font=("Arial", 16))
        self.score_label.pack()

        self.board_label = ctk.CTkLabel(self.container, text=self.logic.board.unicode(), font=("Courier New", 50))
        self.board_label.pack(pady=30)

        self.entry = ctk.CTkEntry(self.container, placeholder_text="Move (e.g. e4)", width=250)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", lambda e: self.process_move())

    def process_move(self):
        move_text = self.entry.get()
        try:
            move = self.logic.board.parse_san(move_text)
            self.logic.move_history.append(self.logic.board.san(move))
            self.logic.board.push(move)
            
            # Update View
            self.board_label.configure(text=self.logic.board.unicode())
            self.score_label.configure(text=self.logic.get_material_score())
            self.entry.configure(border_color=["#979797", "#565b5e"]) # Reset color
            self.entry.delete(0, 'end')
        except:
            self.entry.configure(border_color="red") # The "Shame" border

    def quit_and_save(self):
        self.logic.save_game()
        self.switch_screen("home")

if __name__ == "__main__":
    app = ChessApp()
    app.mainloop()
