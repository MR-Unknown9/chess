import customtkinter as ctk
import os


def create_home_screen(parent, on_start, on_history):
    frame = ctk.CTkFrame(parent)
    ctk.CTkLabel(frame, text="CHESS OS", font=("Arial", 32, "bold")).pack(pady=50)

    ctk.CTkButton(frame, text="NEW GAME", command=on_start).pack(pady=10)
    ctk.CTkButton(frame, text="HISTORY", command=on_history).pack(pady=10)
    return frame


def create_history_screen(parent, on_back):
    frame = ctk.CTkFrame(parent)
    ctk.CTkButton(frame, text="← BACK", command=on_back).pack(
        anchor="nw", padx=10, pady=10
    )

    textbox = ctk.CTkTextbox(frame, width=500, height=400)
    textbox.pack(pady=20)

    # Path logic
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "history", "matches.txt")

    if os.path.exists(path):
        with open(path, "r") as f:
            textbox.insert("0.0", f.read())
    else:
        textbox.insert("0.0", "No history found.")

    textbox.configure(state="disabled")
    return frame
