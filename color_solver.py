import re
import time
import threading
import customtkinter as ctk
import pyautogui
import keyboard
import pyperclip

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
# Parsing functions
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
    emoji_line = None
    for line in text.splitlines():
        if any(ch in COLOR_MAP for ch in line):
            emoji_line = line.strip()
            break
    if not emoji_line:
        return [], None
    emoji_pattern = "(" + "|".join(map(re.escape, COLOR_MAP.keys())) + ")"
    emojis = re.findall(emoji_pattern, emoji_line)
    number = None
    match = re.search(r"Identify the color of (.+?) emoji", text, re.IGNORECASE)
    if match:
        number = extract_number(match.group(1))
    return emojis, number

# -----------------------------
# App functions
# -----------------------------
def show_toast(msg: str):
    toast_label.configure(text=msg)
    toast_label.pack(pady=(0, 8))
    root.after(2000, lambda: toast_label.pack_forget())

def solve_color():
    raw_text = input_box.get("1.0", "end")
    emojis, index = parse_message(raw_text)
    if not emojis or not index:
        show_toast("⚠️ Could not find emojis/number")
        return
    if index < 1 or index > len(emojis):
        show_toast(f"⚠️ Number {index} is out of range")
        return
    target = emojis[index - 1]
    color = COLOR_MAP.get(target, "Unknown")
    result_label.configure(text=f"✅ Emoji #{index} is {target} → {color}")
    if auto_send_enabled.get():
        root.clipboard_clear()
        root.clipboard_append(color)
        delay = delay_seconds.get()
        time.sleep(delay)
        pyautogui.hotkey("ctrl", "v")
        pyautogui.press("enter")
        show_toast(f"📩 Sent '{color}' to Messenger")

def reset_input():
    input_box.delete("1.0", "end")
    result_label.configure(text="")
    show_toast("🔄 Reset done")

def toggle_mode():
    if theme_switch.get() == 1:
        ctk.set_appearance_mode("dark")
    else:
        ctk.set_appearance_mode("light")

def update_delay_label(value):
    delay_label_var.set(f"{int(float(value))} sec")

# -----------------------------
# Build UI
# -----------------------------
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("Color Solver")
root.geometry("500x550")
root.resizable(False, False)
root.attributes("-topmost", True)

auto_send_enabled = ctk.BooleanVar(value=True)
auto_solve_enabled = ctk.BooleanVar(value=True)
delay_seconds = ctk.IntVar(value=5)
delay_label_var = ctk.StringVar(value="5 sec")

# Top bar
top_bar = ctk.CTkFrame(root, fg_color="transparent")
top_bar.pack(fill="x", pady=(10, 5), padx=10)

title = ctk.CTkLabel(top_bar, text="🎨 Color Solver", font=("Segoe UI", 18, "bold"))
title.pack(side="left")

theme_switch = ctk.CTkSwitch(top_bar, text="Dark Mode", command=toggle_mode)
theme_switch.select()
theme_switch.pack(side="right")

# Subtitle
subtitle = ctk.CTkLabel(root, text="Paste the full Messenger message below", font=("Segoe UI", 13))
subtitle.pack(pady=(0, 8))

# Input box
input_box = ctk.CTkTextbox(root, width=460, height=110, font=("Consolas", 12))
input_box.pack(pady=5)

# Buttons
btn_frame = ctk.CTkFrame(root, fg_color="transparent")
btn_frame.pack(pady=8)

solve_btn = ctk.CTkButton(btn_frame, text="Solve Color", command=solve_color, width=180, height=35)
solve_btn.grid(row=0, column=0, padx=10)

reset_btn = ctk.CTkButton(btn_frame, text="Reset", command=reset_input, width=180, height=35, fg_color="gray")
reset_btn.grid(row=0, column=1, padx=10)

# Result label
result_label = ctk.CTkLabel(root, text="", font=("Segoe UI", 14, "bold"))
result_label.pack(pady=10)

# Auto options
auto_frame = ctk.CTkFrame(root, fg_color="transparent")
auto_frame.pack(pady=12)

auto_check = ctk.CTkCheckBox(auto_frame, text="Auto-send to Messenger", variable=auto_send_enabled)
auto_check.grid(row=0, column=0, padx=5)

auto_solve_check = ctk.CTkCheckBox(auto_frame, text="Auto-solve from Clipboard", variable=auto_solve_enabled)
auto_solve_check.grid(row=1, column=0, padx=5, pady=5)

delay_slider = ctk.CTkSlider(
    auto_frame, from_=1, to=10, variable=delay_seconds, number_of_steps=9,
    width=160, command=update_delay_label
)
delay_slider.grid(row=0, column=1, padx=10)

delay_label = ctk.CTkLabel(auto_frame, textvariable=delay_label_var, width=50)
delay_label.grid(row=0, column=2, padx=5)

hotkey_hint = ctk.CTkLabel(
    root,
    text="⚡ Hotkeys: CTRL+X = Solve | CTRL+A = Reset",
    font=("Segoe UI", 12, "italic"),
    text_color="gray"
)
hotkey_hint.pack(pady=(5, 10))

toast_label = ctk.CTkLabel(root, text="", font=("Segoe UI", 12), text_color="green")

# -----------------------------
# Global hotkeys
# -----------------------------
def hotkey_listener_solve():
    while True:
        keyboard.wait("ctrl+x")
        root.after(0, solve_color)

def hotkey_listener_reset():
    while True:
        keyboard.wait("ctrl+a")
        root.after(0, reset_input)

threading.Thread(target=hotkey_listener_solve, daemon=True).start()
threading.Thread(target=hotkey_listener_reset, daemon=True).start()

# -----------------------------
# Clipboard listener with optional auto-solve
# -----------------------------
def clipboard_listener():
    last_text = ""
    while True:
        try:
            text = pyperclip.paste()
            if text != last_text and text.strip():
                last_text = text
                if any(ch in COLOR_MAP for ch in text) and "identify" in text.lower():
                    root.after(0, lambda t=text: (
                        input_box.delete("1.0", "end"),
                        input_box.insert("1.0", t),
                        solve_color() if auto_solve_enabled.get() else None
                    ))
        except Exception as e:
            print("Clipboard error:", e)
        time.sleep(0.5)

threading.Thread(target=clipboard_listener, daemon=True).start()

root.mainloop()
