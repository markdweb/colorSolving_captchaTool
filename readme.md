# 🎨 Color Solver (Emoji Puzzle Helper)

**Color Solver** is a lightweight Python GUI tool that instantly solves emoji-based color puzzles (commonly used in chatbots or mini-games). Just paste the puzzle message, click **Solve**, and get the correct color right away — no more manual counting!

**Author:** Mark Dhel “Makoy” Villarama  
**Purpose:** Personal-use utility to automate solving color-emoji captcha puzzles in Messenger/Chatbot games.

<img src="https://github.com/markdweb/colorSolving_captchaTool/blob/master/src/pic.png" width="100%"/>

---

## 📌 Features

### ✅ Instant Solve
- Paste the whole puzzle message (with emojis and number).  
- App automatically finds the target emoji and returns its color.

### 📋 Auto-Solve from Clipboard (New!)
- Automatically detects copied puzzle messages.  
- If enabled, the app fills the GUI input box and solves it instantly.

### 📩 Auto-Send to Messenger (New!)
- Copies solved color to clipboard and pastes it into Messenger.  
- Configurable delay before sending (1–10 sec).

### ⌨️ Global Hotkeys (New!)
- `CTRL + X` → Solve current puzzle  
- `CTRL + A` → Reset input box

### 🖥 Modern Floating UI
- Built with **CustomTkinter** for a clean, Guna-like design.  
- Supports dark/light mode toggle.  
- Multi-line input for long messages.

### 🔄 Reset & Copy
- One-click reset to paste new puzzles.  
- Copy solved result for quick answers.

### 🎯 Focused Design
- Works offline, no extra setup needed.  
- Lightweight `.exe` build with custom icon support.

---

## 📂 How to Use

### 1. Run App
Launch `ColorSolver.exe` (or run `color_solver.py` if using Python).

### 2. Paste Puzzle
Copy the full puzzle message from Messenger/Chatbot and paste it into the app’s text box.  
*(Optional: enable Auto-Solve to detect messages automatically from clipboard)*

### 3. Click Solve
The app will instantly highlight the correct emoji color.  
*(Optional: use `CTRL + X` to solve instantly)*

### 4. Auto-Send (Optional)
If enabled, the app will paste the solved color into Messenger after a set delay.

### 5. Copy/Reset
Copy the answer or reset the box to solve a new puzzle.  
*(Optional: use `CTRL + A` to reset instantly)*

---

## ⚙️ Tech Stack
- **Language:** Python 3.10+  
- **GUI Framework:** CustomTkinter  
- **Automation:** PyAutoGUI & Pyperclip  
- **Global Hotkeys:** Keyboard  
- **Build Tool:** PyInstaller  
- **Platform:** Windows (tested), should also work on macOS/Linux with Python

---

## 📝 Changelog / New Features

**v2.0 (Latest)**
- Added Auto-Solve from Clipboard feature: automatically detects puzzle messages from clipboard and fills the GUI.  
- Added Auto-Send to Messenger feature: automatically pastes solved color into Messenger after a configurable delay.  
- Added Global Hotkeys for convenience (`CTRL + X` to solve, `CTRL + A` to reset).  
- Updated GUI layout for better visibility of labels and sliders.  
- Maintained dark/light mode toggle for modern look.

---

## 📬 Contact
- **GitHub:** [github.com/markdweb](https://github.com/markdweb)  
- **Email:** `markdhelvillarama1029@gmail.com`
