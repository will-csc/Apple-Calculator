# 🍎 AppleCalculator

A sleek Apple-style calculator built with Python and `Tkinter`. It supports basic math operations, square roots, percentages, keyboard input, and includes a calculation history viewer.

---

## 📸 Screenshot

![image](https://github.com/user-attachments/assets/03b3bec1-3ad2-4a9d-9484-f8ef392dc7b1)

---

## 🧠 Features

- Responsive and visually appealing graphical interface
- Basic operations: `+`, `-`, `*`, `/`, `%`, `√`, `.`
- Calculation history viewer (via a dedicated button)
- Full keyboard support:
  - `Enter`: calculate
  - `Backspace`: delete last character
  - `Esc`: clear input

---

## 🚀 Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/your-username/apple-calculator.git
cd apple-calculator
```

### 2. Install dependencies
```bash
pip install pillow
```

### 3. Run the project
```bash
python main.py
```

---

## Make it executable

### 1. Run the following command inside the folder
```bash
pyinstaller --noconfirm --onefile --windowed --icon=assets/apple.ico --add-data "assets;assets" main.py
```

---

## 📁 Project Structure

```Mathematical
.
├── assets/
│   ├── button_1.png
│   ├── button_2.png
│   └── ...
├── main.py
└── README.md
```

---

## ⚙️ Requirements

Python 3.7+
Pillow library (`pip install pillow`)
