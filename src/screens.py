import customtkinter as ctk
import os


def show_home(parent, on_start, on_history):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(frame, text="CHESS OS v1.0", font=("Arial", 32, "bold")).pack(pady=60)

    ctk.CTkButton(frame, text="NEW GAME", width=200, height=45, command=on_start).pack(
        pady=10
    )
    ctk.CTkButton(
        frame,
        text="VIEW HISTORY",
        width=200,
        height=45,
        fg_color="#444",
        command=on_history,
    ).pack(pady=10)

    ctk.CTkLabel(frame, text="AI Generated • Honest Tech", font=("Arial", 10)).pack(
        side="bottom", pady=20
    )
    return frame


def show_history(parent, on_back):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkButton(frame, text="← MENU", width=80, command=on_back).pack(
        anchor="nw", padx=20, pady=10
    )

    ctk.CTkLabel(frame, text="LOGGED MATCHES", font=("Arial", 20, "bold")).pack()

    # Use a Monospace font so the box art doesn't break
    textbox = ctk.CTkTextbox(
        frame,
        width=550,
        height=450,
        font=("Courier New", 14),
        border_width=2,
        border_color="#444",
    )
    textbox.pack(pady=10, padx=20)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.normpath(
        os.path.join(current_dir, "..", "history", "matches.txt")
    )

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # If the file is empty, say so
            textbox.insert(
                "0.0", content if content.strip() else "History file is empty."
            )
    else:
        textbox.insert("0.0", "⚠️ No match history found.")

    textbox.configure(state="disabled")
    return frame
