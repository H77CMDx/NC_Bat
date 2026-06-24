# NC Bat (No-Code Batch File Creator)

NC Bat is a sleek, visual, modern batch file creator built with Python and Tkinter. It allows users to build, organize, and export Windows batch script workflows without writing any code.

---

## Features

- **Modern UI/UX**: Custom dark and light monochrome themes with smooth micro-animations.
- **Visual Workflow Builder**: Add, edit, duplicate, remove, and reorder steps in your script.
- **Drag & Drop / Groups**: Group related steps together and drag-and-drop to quickly structure scripts.
- **Robust Editor Control**: Fully featured Undo (`Ctrl+Z`) and Redo (`Ctrl+Y`) system. 
- **Autosave & Recovery**: Automatically saves progress every 60 seconds, with recovery prompt on startup in case of an unexpected crash.
- **Smart Templates**: Save your frequent workflows as templates and manage them within the app.
- **BAT Import & Export**:
  - Export scripts directly to `.bat` with a built-in command safety checker.
  - Import existing `.bat` files to visually modify them.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher installed.

### Running Locally

To run the application, simply execute the main script:

```bash
python main.py
```

### Packaging into a Standalone Executable

To compile NC Bat into a single, standalone Windows executable (`NC Bat.exe` under the `dist/` directory):

1. Double-click or run `export.bat` in the terminal:
   ```cmd
   export.bat
   ```
2. The script will automatically:
   - Create and configure a local virtual environment (`.venv`).
   - Check and install required dependencies (including `Pillow` and `PyInstaller`).
   - Convert assets and package the application with custom icons.

---

## Keyboard Shortcuts

| Shortcut | Action |
| --- | --- |
| `Ctrl + N` | New Project |
| `Ctrl + S` | Save Project |
| `Ctrl + E` | Export `.bat` File |
| `Ctrl + Z` | Undo |
| `Ctrl + Y` | Redo |
| `Ctrl + D` | Duplicate Selected Step |
| `Delete` | Remove Selected Step |
| `Ctrl + Up` / `Down` | Move Selected Step Up/Down |
| `F2` | Edit Selected Step |
| `F11` | Toggle Fullscreen |
| `Escape` | Clear Search / Exit Fullscreen |
| `Enter` | Add Step (when field is focused) |

---

## Terms & Conditions

NC Bat is created by Hiroshi Kelner. Please refer to the **Terms & Conditions** in the application menu for licensing details.
