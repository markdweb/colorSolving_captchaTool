import re
import customtkinter as ctk
from tkinter import messagebox

# 🎨 Color dictionary
COLOR_MAP = {
    "❤": "red", "❤️": "red",
    "💙": "blue", "💚": "green", "💛": "yellow", "🧡": "orange",
    "💜": "purple", "🤎": "brown", "🖤": "black", "🤍": "white",
    "🔴": "red", "🟠": "orange", "🟡": "yellow", "🟢": "green",
    "🔵": "blue", "🟣": "purple", "🟤": "brown",
    "⚫": "black", "⚪": "white",
    "🟥": "red", "🟧": "orange", "🟨": "yellow", "🟩": "green",
    "🟦": "blue", "🟪": "purple", "🟫": "brown",
}

# -----------------------------
# 🔎 Parsing functions
# -----------------------------
def clean_text(raw):
    return raw.replace("\r", "").strip()

def extract_number(fragment: str):
    fragment = fragment.replace("\uFE0F", "")
    digits = re.findall(r"\d+", fragment)
    if digits:
        return int("".join(digits))
    return None

def parse_message(raw_text):
    text = clean_text(raw_text)

    # Emoji line
    emoji_line = None
    for line in text.splitlines():
        if any(ch in COLOR_MAP for ch in line):
            emoji_line = line.strip()
            break

    if not emoji_line:
        return [], None

    # Emojis
    emoji_pattern = "(" + "|".join(map(re.escape, COLOR_MAP.keys())) + ")"
    emojis = re.findall(emoji_pattern, emoji_line)

    # Number in "Identify..."
    number = None
    match = re.search(r"Identify the color of (.+?) emoji", text, re.IGNORECASE)
    if match:
        number = extract_number(match.group(1))

    return emojis, number

# -----------------------------
# 🖱 Tooltip class
# -----------------------------
class CreateToolTip:
    """
    Tooltip for a widget that shows the actual color dynamically
    """
    def __init__(self, widget, default_text="Click to copy"):
        self.widget = widget
        self.default_text = default_text
        self.tipwindow = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        color_text = getattr(self.widget, "color_only", "")
        if self.tipwindow or not color_text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tipwindow = tw = ctk.CTkToplevel(self.widget)
        tw.overrideredirect(True)
        tw.geometry(f"+{x}+{y}")
        label = ctk.CTkLabel(
            tw,
            text=color_text,
            font=("Segoe UI", 10),
            fg_color="#333",
            text_color="white",
            corner_radius=5,
            padx=5,
            pady=2
        )
        label.pack()

    def hide_tip(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
        self.tipwindow = None

# -----------------------------
# 🎨 App Functions
# -----------------------------
def solve_color():
    raw_text = input_box.get("1.0", "end")
    emojis, index = parse_message(raw_text)

    if not emojis or not index:
        messagebox.showwarning("Warning", "Could not find emojis or number in the text!")
        return

    if index < 1 or index > len(emojis):
        messagebox.showwarning("Warning", f"Number {index} is out of range (1-{len(emojis)}).")
        return

    target = emojis[index - 1]
    color = COLOR_MAP.get(target, "Unknown")

    # Show full info in label
    result_label.configure(text=f"✅ Emoji #{index} is {target} → {color}")

    # Save color only for copying
    result_label.color_only = color

def copy_result(event=None):
    if hasattr(result_label, "color_only"):
        root.clipboard_clear()
        root.clipboard_append(result_label.color_only)
    # Hide tooltip immediately
    if hasattr(result_label, "tooltip") and result_label.tooltip.tipwindow:
        result_label.tooltip.hide_tip()

def reset_input():
    input_box.delete("1.0", "end")
    result_label.configure(text="")
    result_label.color_only = ""

def toggle_mode():
    global current_mode
    current_mode = "light" if current_mode == "dark" else "dark"
    ctk.set_appearance_mode(current_mode)
    mode_btn.configure(text=f"Switch to {'Dark' if current_mode=='light' else 'Light'} Mode")

# -----------------------------
# 🪟 Build Modern UI
# -----------------------------
ctk.set_default_color_theme("blue")
current_mode = "dark"
ctk.set_appearance_mode(current_mode)

root = ctk.CTk()
root.title("Color Solver")
root.geometry("520x420")
root.resizable(False, False)
root.attributes("-topmost", True)

# Main Frame
main_frame = ctk.CTkFrame(root, corner_radius=15)
main_frame.pack(fill="both", expand=True, padx=15, pady=15)

title = ctk.CTkLabel(main_frame, text="🎨 Color Solver", font=("Segoe UI", 18, "bold"))
title.pack(pady=(15, 5))

subtitle = ctk.CTkLabel(main_frame, text="Paste the full Messenger message below", font=("Segoe UI", 13))
subtitle.pack(pady=(0, 12))

# Multiline input
input_box = ctk.CTkTextbox(main_frame, width=460, height=160, font=("Consolas", 12))
input_box.insert("1.0", "👉 Paste here...")
input_box.pack(pady=5)

# Buttons
btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
btn_frame.pack(pady=12)

solve_btn = ctk.CTkButton(btn_frame, text="Solve Color", command=solve_color, width=180, height=40)
solve_btn.grid(row=0, column=0, padx=10)

reset_btn = ctk.CTkButton(btn_frame, text="Reset", command=reset_input, width=180, height=40, fg_color="gray")
reset_btn.grid(row=0, column=1, padx=10)

# Result Label
result_label = ctk.CTkLabel(main_frame, text="", font=("Segoe UI", 14, "bold"))
result_label.pack(pady=10)
result_label.color_only = ""
result_label.tooltip = CreateToolTip(result_label)
result_label.bind("<Button-1>", copy_result)

# Dark/Light Toggle Button
mode_btn = ctk.CTkButton(main_frame, text="Switch to Light Mode", command=toggle_mode, width=200, height=35)
mode_btn.pack(pady=10)

root.mainloop()
