import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import json
import os
import re
import datetime
import copy
import urllib.request
import threading
import sys

APP_DISPLAY_NAME = "NC Bat"
APP_VERSION = "2.6"
APP_NAME = f"{APP_DISPLAY_NAME} v{APP_VERSION}"
AUTO_SAVE_INTERVAL = 60_000

UPDATE_URL   = "https://nocodebat.weebly.com/download.html"
SUPPORT_URL  = "https://nocodebat.weebly.com/support-the-project.html"
FEEDBACK_URL = "https://nocodebat.weebly.com/give-feedback.html"
VERSION_FILE_URL = "https://gist.githubusercontent.com/H77CMDx/e190881a5ea4cee1f5c1eb225dbec07f/raw/NC_Bat_version.txt"
GIST_API_URL     = "https://api.github.com/gists/e190881a5ea4cee1f5c1eb225dbec07f"

# ─── Monochrome modern theme ─────────────────────────────────────────────────
THEMES = {
    "dark": {
        "bg":                "#0A0A0A",
        "sidebar_bg":        "#111111",
        "panel_bg":          "#111111",
        "border":            "#222222",
        "accent":            "#EFEFEF",
        "accent_hover":      "#FFFFFF",
        "accent_fg":         "#0A0A0A",
        "danger":            "#E53535",
        "danger_hover":      "#FF5555",
        "text":              "#F0F0F0",
        "text_muted":        "#808080",
        "text_light":        "#3A3A3A",
        "entry_bg":          "#0D0D0D",
        "entry_border":      "#2A2A2A",
        "entry_focus":       "#707070",
        "listbox_bg":        "#111111",
        "listbox_sel":       "#242424",
        "listbox_sel_fg":    "#FFFFFF",
        "scrollbar":         "#2A2A2A",
        "header_bg":         "#0A0A0A",
        "sep":               "#1C1C1C",
        "code_bg":           "#080808",
        "code_fg":           "#E8E8E8",
        "btn_secondary_bg":  "#1A1A1A",
        "btn_secondary_fg":  "#E0E0E0",
        "btn_secondary_hover":"#2C2C2C",
        "btn_ghost_bg":      "#111111",
        "btn_ghost_fg":      "#A0A0A0",
        "btn_ghost_hover":   "#1C1C1C",
        "status_bg":         "#0A0A0A",
        # row tints used in listboxes
        "alt_row_bg":        "#141414",
        "alb_hover_bg":      "#1A1A1A",
        "alb_alt_row_bg":    "#161616",
    },
    "light": {
        "bg":                "#F2F2F2",
        "sidebar_bg":        "#E8E8E8",
        "panel_bg":          "#E8E8E8",
        "border":            "#C8C8C8",
        "accent":            "#1A1A1A",
        "accent_hover":      "#000000",
        "accent_fg":         "#FFFFFF",
        "danger":            "#D32F2F",
        "danger_hover":      "#B71C1C",
        "text":              "#111111",
        "text_muted":        "#606060",
        "text_light":        "#B0B0B0",
        "entry_bg":          "#FFFFFF",
        "entry_border":      "#C0C0C0",
        "entry_focus":       "#888888",
        "listbox_bg":        "#E8E8E8",
        "listbox_sel":       "#505050",
        "listbox_sel_fg":    "#FFFFFF",
        "scrollbar":         "#C0C0C0",
        "header_bg":         "#F2F2F2",
        "sep":               "#D8D8D8",
        "code_bg":           "#FAFAFA",
        "code_fg":           "#1A1A1A",
        "btn_secondary_bg":  "#DCDCDC",
        "btn_secondary_fg":  "#111111",
        "btn_secondary_hover":"#CACACA",
        "btn_ghost_bg":      "#E8E8E8",
        "btn_ghost_fg":      "#505050",
        "btn_ghost_hover":   "#D8D8D8",
        "status_bg":         "#F2F2F2",
        # row tints used in listboxes
        "alt_row_bg":        "#E0E0E0",
        "alb_hover_bg":      "#D4D4D4",
        "alb_alt_row_bg":    "#DADADA",
    },
}

def _apply_theme_globals(theme_key):
    """Update all module-level color globals to the given theme."""
    global _T, _ACCENT, _ACCENT_HOVER, _ACCENT_FG, _DANGER, _DANGER_HOVER
    global _BTN_SEC_BG, _BTN_SEC_FG, _BTN_SEC_HOV
    global _BTN_GHO_BG, _BTN_GHO_FG, _BTN_GHO_HOV
    global _PANEL_BG, _HEADER_BG, _TEXT, _TEXT_MUTED, _TEXT_LIGHT
    global _ENTRY_BG, _ENTRY_BORDER, _ENTRY_FOCUS
    global _LB_BG, _LB_SEL, _LB_SEL_FG, _SCROLLBAR
    global _CODE_BG, _CODE_FG, _BG, _BORDER, _SEP, _STATUS_BG
    global _ALT_ROW_BG, _ALB_HOVER_BG, _ALB_ALT_ROW_BG
    _T            = THEMES[theme_key]
    _ACCENT       = _T["accent"]
    _ACCENT_HOVER = _T["accent_hover"]
    _ACCENT_FG    = _T["accent_fg"]
    _DANGER       = _T["danger"]
    _DANGER_HOVER = _T["danger_hover"]
    _BTN_SEC_BG   = _T["btn_secondary_bg"]
    _BTN_SEC_FG   = _T["btn_secondary_fg"]
    _BTN_SEC_HOV  = _T["btn_secondary_hover"]
    _BTN_GHO_BG   = _T["btn_ghost_bg"]
    _BTN_GHO_FG   = _T["btn_ghost_fg"]
    _BTN_GHO_HOV  = _T["btn_ghost_hover"]
    _PANEL_BG     = _T["panel_bg"]
    _HEADER_BG    = _T["header_bg"]
    _TEXT         = _T["text"]
    _TEXT_MUTED   = _T["text_muted"]
    _TEXT_LIGHT   = _T["text_light"]
    _ENTRY_BG     = _T["entry_bg"]
    _ENTRY_BORDER = _T["entry_border"]
    _ENTRY_FOCUS  = _T["entry_focus"]
    _LB_BG        = _T["listbox_bg"]
    _LB_SEL       = _T["listbox_sel"]
    _LB_SEL_FG    = _T["listbox_sel_fg"]
    _SCROLLBAR    = _T["scrollbar"]
    _CODE_BG      = _T["code_bg"]
    _CODE_FG      = _T["code_fg"]
    _BG           = _T["bg"]
    _BORDER       = _T["border"]
    _SEP          = _T["sep"]
    _STATUS_BG    = _T["status_bg"]
    _ALT_ROW_BG      = _T["alt_row_bg"]
    _ALB_HOVER_BG    = _T["alb_hover_bg"]
    _ALB_ALT_ROW_BG  = _T["alb_alt_row_bg"]

_apply_theme_globals("dark")


# ─── TextAreaVar – wraps tk.Text with a StringVar-compatible interface ────────
class TextAreaVar:
    def __init__(self, widget):
        self._w = widget

    def get(self):
        return self._w.get("1.0", "end-1c")

    def set(self, v):
        self._w.delete("1.0", "end")
        self._w.insert("1.0", v)


# ─── Widgets ─────────────────────────────────────────────────────────────────
class RoundedButton(tk.Canvas):
    """Canvas-based rounded button with polygon points cache."""
    _pts_cache: dict = {}

    def __init__(self, parent, text, command=None, style="primary",
                 width=120, height=38, radius=8, font_size=14, **kwargs):
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, bd=0, **kwargs)
        self.command  = command
        self.text     = text
        self.style    = style
        self.w        = width
        self.h        = height
        self.r        = radius
        self.fs       = font_size
        self._hovered = False
        self._pressed = False
        self._update_color_pair()
        self.bind("<Enter>",           self._enter)
        self.bind("<Leave>",           self._leave)
        self.bind("<ButtonPress-1>",   self._press)
        self.bind("<ButtonRelease-1>", self._click)

    def _update_color_pair(self):
        s = self.style
        if s == "primary":
            self._bg_norm, self._bg_hov, self._fg = _ACCENT,     _ACCENT_HOVER, _ACCENT_FG
        elif s == "danger":
            self._bg_norm, self._bg_hov, self._fg = _DANGER,     _DANGER_HOVER, "#FFF"
        elif s == "secondary":
            self._bg_norm, self._bg_hov, self._fg = _BTN_SEC_BG, _BTN_SEC_HOV,  _BTN_SEC_FG
        else:  # ghost
            self._bg_norm, self._bg_hov, self._fg = _BTN_GHO_BG, _BTN_GHO_HOV,  _BTN_GHO_FG
        self._font = ("Segoe UI", self.fs, "bold" if s in ("primary", "danger") else "normal")

    def apply_theme(self, theme):
        self._draw()

    def _draw(self):
        self.delete("all")
        if self._pressed:
            bg = self._bg_norm  # pressed = back to normal (sunken feel)
        elif self._hovered:
            bg = self._bg_hov
        else:
            bg = self._bg_norm
        key = (self.w, self.h, self.r)
        pts = RoundedButton._pts_cache.get(key)
        if pts is None:
            w, h, r = self.w, self.h, self.r
            pts = [r,0, w-r,0, w,0, w,r, w,h-r, w,h, w-r,h, r,h, 0,h, 0,h-r, 0,r, 0,0, r,0]
            RoundedButton._pts_cache[key] = pts
        self.create_polygon(pts, smooth=True, fill=bg, outline="")
        self.create_text(self.w // 2, self.h // 2, text=self.text,
                         fill=self._fg, font=self._font)

    def _enter(self, _):
        self._hovered = True
        self._pressed = False
        self._draw()
        self.configure(cursor="hand2")

    def _leave(self, _):
        self._hovered = False
        self._pressed = False
        self._draw()
        self.configure(cursor="")

    def _press(self, _):
        self._pressed = True
        self._draw()

    def _click(self, _):
        self._pressed = False
        self._draw()
        if self.command:
            self.command()


class StyledEntry(tk.Frame):
    def __init__(self, parent, textvariable=None, placeholder="", **kwargs):
        super().__init__(parent, bd=0)
        self._ph    = placeholder
        self._is_ph = False
        self._var   = textvariable or tk.StringVar()
        self._e     = tk.Entry(self, textvariable=self._var, relief="flat", bd=0,
                                font=("Segoe UI", 14),
                                bg=_ENTRY_BG, fg=_TEXT,
                                insertbackground=_TEXT,
                                selectbackground=_ACCENT, selectforeground=_ACCENT_FG,
                                **kwargs)
        self._e.pack(fill="both", expand=True, padx=10, pady=7)
        self.config(bg=_ENTRY_BG,
                    highlightbackground=_ENTRY_BORDER,
                    highlightcolor=_ENTRY_BORDER,
                    highlightthickness=1)
        self._e.bind("<FocusIn>",  self._fin)
        self._e.bind("<FocusOut>", self._fout)
        if placeholder:
            self._set_ph()

    def _set_ph(self):
        self._e.delete(0, "end")
        self._e.insert(0, self._ph)
        self._is_ph = True
        self._e.config(fg=_TEXT_LIGHT)

    def _fin(self, _):
        if self._is_ph:
            self._e.delete(0, "end")
            self._is_ph = False
        self._e.config(fg=_TEXT)
        self.config(highlightbackground=_ENTRY_FOCUS,
                    highlightcolor=_ENTRY_FOCUS,
                    highlightthickness=2)

    def _fout(self, _):
        self.config(highlightbackground=_ENTRY_BORDER,
                    highlightcolor=_ENTRY_BORDER,
                    highlightthickness=1)
        if not self._e.get() and self._ph:
            self._set_ph()

    def get(self):
        return "" if self._is_ph else self._e.get()

    def set(self, v):
        self._e.delete(0, "end")
        self._is_ph = False
        if v:
            self._e.insert(0, v)
            self._e.config(fg=_TEXT)
        elif self._ph:
            self._set_ph()

    def apply_theme(self, _theme=None):
        pass


class StyledTextArea(tk.Frame):
    """Multi-line styled text input that returns a TextAreaVar."""
    def __init__(self, parent, height=4, **kwargs):
        super().__init__(parent, bd=0)
        self._t = tk.Text(self, relief="flat", bd=0,
                          font=("Segoe UI", 13),
                          bg=_ENTRY_BG, fg=_TEXT,
                          insertbackground=_TEXT,
                          selectbackground=_ACCENT, selectforeground=_ACCENT_FG,
                          height=height, wrap="none",
                          padx=10, pady=6,
                          **kwargs)
        sb = tk.Scrollbar(self, orient="vertical", command=self._t.yview,
                          relief="flat", bd=0, width=6,
                          bg=_SCROLLBAR, troughcolor=_ENTRY_BG,
                          activebackground=_ACCENT)
        self._t.configure(yscrollcommand=sb.set)
        self._t.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.config(bg=_ENTRY_BG,
                    highlightbackground=_ENTRY_BORDER,
                    highlightcolor=_ENTRY_BORDER,
                    highlightthickness=1)
        self._t.bind("<FocusIn>",  self._fin)
        self._t.bind("<FocusOut>", self._fout)
        self.var = TextAreaVar(self._t)

    def _fin(self, _):
        self.config(highlightbackground=_ENTRY_FOCUS,
                    highlightcolor=_ENTRY_FOCUS,
                    highlightthickness=2)

    def _fout(self, _):
        self.config(highlightbackground=_ENTRY_BORDER,
                    highlightcolor=_ENTRY_BORDER,
                    highlightthickness=1)


class ThemedListbox(tk.Frame):
    def __init__(self, parent, show_scrollbar=True, **kwargs):
        super().__init__(parent, bd=0, highlightthickness=0, bg=_LB_BG)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.lb = tk.Listbox(self, relief="flat", bd=0, activestyle="none",
                              font=("Segoe UI", 13),
                              bg=_LB_BG, fg=_TEXT,
                              selectbackground=_LB_SEL,
                              selectforeground=_LB_SEL_FG,
                              selectborderwidth=0,
                              **kwargs)
        sb = tk.Scrollbar(self, orient="vertical", command=self.lb.yview,
                           relief="flat", bd=0, width=6,
                           bg=_SCROLLBAR, troughcolor=_LB_BG,
                           activebackground=_ACCENT)
        self.lb.configure(yscrollcommand=sb.set)
        self.lb.grid(row=0, column=0, sticky="nsew")
        if show_scrollbar:
            sb.grid(row=0, column=1, sticky="ns")
        self._sb = sb

    def apply_theme(self, _theme=None): pass
    def insert(self, *a, **kw):   return self.lb.insert(*a, **kw)
    def delete(self, *a, **kw):   return self.lb.delete(*a, **kw)
    def curselection(self):        return self.lb.curselection()
    def selection_set(self, *a):   return self.lb.selection_set(*a)
    def bind(self, *a, **kw):      return self.lb.bind(*a, **kw)
    def size(self):                return self.lb.size()


class Tooltip:
    """Lightweight popup tooltip shown on widget hover."""
    def __init__(self, widget, text):
        self._w   = widget
        self._txt = text
        self._win = None
        widget.bind("<Enter>",       self._show, add="+")
        widget.bind("<Leave>",       self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def update_text(self, text):
        self._txt = text

    def _show(self, _e=None):
        if self._win:
            return
        self._win = w = tk.Toplevel(self._w)
        w.overrideredirect(True)
        w.attributes("-topmost", True)
        w.configure(bg=_BORDER)
        inner = tk.Frame(w, bg=_PANEL_BG, padx=9, pady=5)
        inner.pack(padx=1, pady=1)
        tk.Label(inner, text=self._txt, font=("Segoe UI", 11),
                 bg=_PANEL_BG, fg=_TEXT_MUTED, wraplength=220).pack()
        w.update_idletasks()
        tw = w.winfo_width()
        wx = self._w.winfo_rootx() + self._w.winfo_width() // 2 - tw // 2
        wy = self._w.winfo_rooty() + self._w.winfo_height() + 4
        w.geometry(f"+{max(0, wx)}+{wy}")

    def _hide(self, _e=None):
        if self._win:
            self._win.destroy()
            self._win = None


class CodeLineNumbers(tk.Canvas):
    """Canvas that renders line numbers synced to a Text widget."""
    def __init__(self, parent, text_widget, **kwargs):
        super().__init__(parent, **kwargs)
        self._t = text_widget
        self.configure(bg=_CODE_BG, highlightthickness=0, bd=0, width=34)

    def redraw(self, *_):
        self.delete("all")
        try:
            i = self._t.index("@0,0")
        except Exception:
            return
        while True:
            dline = self._t.dlineinfo(i)
            if dline is None:
                break
            y      = dline[1]
            lineno = int(str(i).split(".")[0])
            self.create_text(28, y + 6, anchor="ne", text=str(lineno),
                             fill=_TEXT_MUTED, font=("Consolas", 11))
            next_i = self._t.index(f"{i}+1line")
            if next_i == i:
                break
            i = next_i


# ─── Translations ─────────────────────────────────────────────────────────────
TRANSLATIONS = {
    "en": {
        "app_title": APP_NAME,
        "steps": "Steps",
        "move_up": "Move Up",
        "move_down": "Move Down",
        "remove": "Remove",
        "duplicate": "Duplicate",
        "edit": "Edit",
        "undo": "Undo",
        "redo": "Redo",
        "add_step": "Add Step",
        "save_bat": "Export  .bat",
        "generated_code": "Generated Code",
        "add_step_section": "Add Step",
        "no_options": "No options needed",
        "nothing_to_save": "Nothing to save",
        "add_one_step": "Add at least one step.",
        "saved": "Saved",
        "saved_to": "Saved to:\n{path}",
        "check_updates": "Check for updates",
        "you_are_running": "You are running {version}.\n\nYou will be redirected to the download page.",
        "file": "File",
        "edit_menu": "Edit",
        "new_project": "New Project",
        "open_project": "Open Project",
        "save_project": "Save Project",
        "save_project_as": "Save Project As",
        "import_bat": "Import .bat File",
        "exit": "Exit",
        "templates": "Templates",
        "save_as_template": "Save as Template",
        "load_template": "Load Template",
        "manage_templates": "Manage Templates",
        "extras": "Extras",
        "twitter": "Twitter: @hiroshiken71",
        "support_project": "Support the Project",
        "give_feedback": "Give Feedback",
        "help": "Help",
        "instruction_manual": "Instruction Manual",
        "debug": "Debug",
        "about": "About",
        "terms": "Terms & Conditions",
        "open_config_folder": "Open Config Folder",
        "accept_terms": "I Accept",
        "decline_terms": "I Decline",
        "must_accept_terms": "You must accept the Terms & Conditions to use NC Bat.",
        "terms_agreement": "Terms & Conditions Agreement",
        "select_language": "Select Language",
        "language": "Language",
        "english": "English",
        "french": "Francais",
        "search": "Search actions...",
        "create_group": "Create Group",
        "ungroup": "Ungroup",
        "rename_group": "Rename Group",
        "select_steps_to_group": "Select at least one step to group.",
        "select_group_to_ungroup": "Select a group to ungroup.",
        "select_group_to_rename": "Select a group to rename.",
        "group_name": "Group Name",
        "enter_group_name": "Enter group name:",
        "items_in_group": "Items in Group",
        "items_outside_group": "Items Outside Group",
        "add": "Add",
        "imported_bat": "Imported BAT",
        "no_actions_found": "No actions found in BAT file",
        "imported_actions": "Imported {count} actions into group '{name}'",
        "template_saved": "Template saved successfully!",
        "template_loaded": "Template loaded successfully!",
        "select_template": "Select a template to load:",
        "no_templates": "No templates available.",
        "load_button": "Load",
        "manage_templates_title": "Manage Templates",
        "delete_selected": "Delete Selected",
        "close": "Close",
        "confirm_delete": "Are you sure you want to delete this template?",
        "project_saved": "Project saved successfully!",
        "project_loaded": "Project loaded successfully!",
        "unsaved_changes": "Unsaved Changes",
        "save_before_exit": "Do you want to save your project before exiting?",
        "edit_step": "Edit Step",
        "update_step": "Save Changes",
        "cancel": "Cancel",
        "rename_project": "Rename Project",
        "project_name_prompt": "Enter project name:",
        "help_content": f"""Instruction Manual - {APP_NAME}

1. CHOOSE AN ACTION
   Select an action from the list in the center panel.
   Use the search bar to quickly filter actions.
   Press Escape to clear the search and show all actions.
   A description of the selected action appears below the list.

2. FILL IN THE FIELDS
   Each action shows only the fields you need.

3. ADD THE STEP
   Click "Add Step" (or press Enter in a field) to append it to your workflow.
   The new step is automatically selected in the steps list.

4. ORGANIZE YOUR STEPS
   Move Up / Move Down, Edit, Duplicate, Remove.
   Drag and drop steps to reorder them quickly.
   Double-click any step to edit it immediately.
   Right-click any step for a quick-access context menu.
   Use Create Group, Ungroup, and Rename Group to organize.

5. UNDO / REDO
   Press Ctrl+Z to undo and Ctrl+Y to redo any action.

6. KEYBOARD SHORTCUTS
   Ctrl+S       Save project
   Ctrl+N       New project
   Ctrl+Z       Undo
   Ctrl+Y       Redo
   Ctrl+D       Duplicate selected step
   Ctrl+E       Export .bat
   Delete       Remove selected step
   Ctrl+Up      Move step up
   Ctrl+Down    Move step down
   F2           Edit selected step
   F11          Toggle fullscreen
   Escape       Clear search / exit fullscreen
   Enter        Add step (when a field is focused)

7. EXPORT
   Click "Export .bat" to save your workflow as a batch file.
   The safety checker will warn you about dangerous commands.

8. PROJECT NAME
   Click the project name in the header to rename it inline.
   You can also use File > Rename Project.
   The name is saved inside the .ncbat file and shown in the title bar.

9. AUTOSAVE & RECOVERY
   NC Bat autosaves your work every 60 seconds.
   If a recent unsaved session is detected on startup,
   NC Bat will offer to recover it automatically.""",
        "debug_content": """DEBUG TROUBLESHOOTING

1. Application Won't Start
   Try running as administrator.

2. "Windows Protected Your PC"
   Click "More info" then "Run anyway".

3. Batch File Doesn't Execute
   Right-click the .bat and "Run as administrator".

4. Cannot Save/Load
   Check disk space and write permissions.

5. Antivirus Quarantining
   This is a false positive. Add NC Bat to exclusions.

6. Steps List Blank After Load
   Your .ncbat file may reference an old action key.
   Re-open and re-add the affected steps manually.

7. Autosave Recovery
   NC Bat autosaves every 60 seconds to:
     %USERPROFILE%\\.ncbat\\autosave\\
   On startup, NC Bat offers to recover the most recent
   autosave if it is less than 8 hours old.
   You can also open autosave files manually via File > Open.""",
        "about_content": f"""{APP_NAME}

Copyright 2026 Hiroshi Kelner
All Rights Reserved

{APP_DISPLAY_NAME} is a visual batch file creator.

Creator : Hiroshi Kelner
Twitter : @hiroshiken71
Website : https://nocodebat.weebly.com

Version      : {APP_VERSION}
Release Date : 2026""",
        "terms_content": f"""TERMS AND CONDITIONS

{APP_NAME} - End User License Agreement
Copyright 2026 Hiroshi Kelner. All Rights Reserved.

LICENSE GRANT
By using {APP_DISPLAY_NAME}, you receive a non-exclusive license to use it
on any computers you own for personal, educational, or commercial projects.

USER RESPONSIBILITY
YOU ASSUME ALL RESPONSIBILITY for batch files you create.

INTELLECTUAL PROPERTY
You may NOT claim {APP_DISPLAY_NAME} as your own or redistribute it.

YOUR FILES ARE YOURS
Batch files you create belong to you entirely.

By using {APP_DISPLAY_NAME}, you agree to these terms.

Thank you for using {APP_DISPLAY_NAME}!
- Hiroshi Kelner""",
    },
    "fr": {
        "app_title": APP_NAME,
        "steps": "Étapes",
        "move_up": "Monter",
        "move_down": "Descendre",
        "remove": "Supprimer",
        "duplicate": "Dupliquer",
        "edit": "Modifier",
        "undo": "Annuler",
        "redo": "Rétablir",
        "add_step": "Ajouter une étape",
        "save_bat": "Exporter .bat",
        "generated_code": "Code généré",
        "add_step_section": "Ajouter une étape",
        "no_options": "Aucune option requise",
        "nothing_to_save": "Rien à enregistrer",
        "add_one_step": "Ajoutez au moins une étape.",
        "saved": "Enregistré",
        "saved_to": "Enregistré dans :\n{path}",
        "check_updates": "Vérifier les mises à jour",
        "you_are_running": "Vous utilisez {version}.\n\nRedirection vers la page de téléchargement.",
        "file": "Fichier",
        "edit_menu": "Édition",
        "new_project": "Nouveau projet",
        "open_project": "Ouvrir un projet",
        "save_project": "Enregistrer le projet",
        "save_project_as": "Enregistrer sous",
        "import_bat": "Importer un .bat",
        "exit": "Quitter",
        "templates": "Modèles",
        "save_as_template": "Enregistrer comme modèle",
        "load_template": "Charger un modèle",
        "manage_templates": "Gérer les modèles",
        "extras": "Extras",
        "twitter": "Twitter: @hiroshiken71",
        "support_project": "Soutenir le projet",
        "give_feedback": "Donner votre avis",
        "help": "Aide",
        "instruction_manual": "Manuel d'instructions",
        "debug": "Débogage",
        "about": "À propos",
        "terms": "Conditions d'utilisation",
        "open_config_folder": "Ouvrir le dossier de config",
        "accept_terms": "J'accepte",
        "decline_terms": "Je refuse",
        "must_accept_terms": "Vous devez accepter les conditions pour utiliser NC Bat.",
        "terms_agreement": "Accord des conditions d'utilisation",
        "select_language": "Sélectionner la langue",
        "language": "Langue",
        "english": "English",
        "french": "Français",
        "search": "Rechercher des actions...",
        "create_group": "Créer un groupe",
        "ungroup": "Dégrouper",
        "rename_group": "Renommer",
        "select_steps_to_group": "Sélectionnez au moins une étape.",
        "select_group_to_ungroup": "Sélectionnez un groupe.",
        "select_group_to_rename": "Sélectionnez un groupe.",
        "group_name": "Nom du groupe",
        "enter_group_name": "Entrez le nom du groupe :",
        "items_in_group": "Éléments dans le groupe",
        "items_outside_group": "Éléments hors du groupe",
        "add": "Ajouter",
        "imported_bat": "BAT importé",
        "no_actions_found": "Aucune action trouvée",
        "imported_actions": "{count} actions importées dans '{name}'",
        "template_saved": "Modèle enregistré !",
        "template_loaded": "Modèle chargé !",
        "select_template": "Sélectionnez un modèle :",
        "no_templates": "Aucun modèle disponible.",
        "load_button": "Charger",
        "manage_templates_title": "Gérer les modèles",
        "delete_selected": "Supprimer",
        "close": "Fermer",
        "confirm_delete": "Supprimer ce modèle ?",
        "project_saved": "Projet enregistré !",
        "project_loaded": "Projet chargé !",
        "unsaved_changes": "Modifications non enregistrées",
        "save_before_exit": "Voulez-vous enregistrer avant de quitter ?",
        "edit_step": "Modifier l'étape",
        "update_step": "Enregistrer",
        "cancel": "Annuler",
        "rename_project": "Renommer le projet",
        "project_name_prompt": "Nom du projet :",
        "help_content": f"""Manuel d'instructions - {APP_NAME}

1. CHOISIR UNE ACTION
   Selectionnez une action dans la liste du panneau central.
   Utilisez la barre de recherche pour filtrer rapidement.
   Appuyez sur Echap pour effacer la recherche et tout afficher.
   Une description de l'action s'affiche sous la liste.

2. REMPLIR LES CHAMPS
   Chaque action affiche uniquement les champs necessaires.

3. AJOUTER L'ETAPE
   Cliquez sur "Ajouter une etape" (ou appuyez sur Entree dans un champ).
   La nouvelle etape est automatiquement selectionnee.

4. ORGANISER LES ETAPES
   Monter / Descendre, Modifier, Dupliquer, Supprimer.
   Glissez-deposez les etapes pour les reordonner.
   Double-cliquez sur une etape pour la modifier directement.
   Clic droit sur une etape pour le menu contextuel rapide.
   Utilisez Creer un groupe, Degrouper, Renommer le groupe.

5. ANNULER / RETABLIR
   Ctrl+Z pour annuler, Ctrl+Y pour retablir.

6. RACCOURCIS CLAVIER
   Ctrl+S       Enregistrer le projet
   Ctrl+N       Nouveau projet
   Ctrl+Z       Annuler
   Ctrl+Y       Retablir
   Ctrl+D       Dupliquer l'etape selectionnee
   Suppr        Supprimer l'etape selectionnee
   Ctrl+Haut    Monter l'etape
   Ctrl+Bas     Descendre l'etape
   F2           Modifier l'etape selectionnee
   F11          Plein ecran
   Echap        Effacer la recherche / quitter le plein ecran
   Entree       Ajouter une etape (dans un champ)

7. EXPORTER
   Cliquez sur "Exporter .bat" pour enregistrer votre script.

8. NOM DU PROJET
   Cliquez sur le nom du projet dans l'en-tete pour le renommer.
   Vous pouvez aussi utiliser Fichier > Renommer le projet.
   Le nom est enregistre dans le fichier .ncbat et affiche dans la barre de titre.

9. SAUVEGARDE AUTOMATIQUE
   NC Bat sauvegarde votre travail toutes les 60 secondes.
   Si une session non enregistree est detectee au demarrage,
   NC Bat proposera de la recuperer automatiquement.""",
        "debug_content": """DEPANNAGE

1. L'application ne demarre pas
   Essayez d'executer en tant qu'administrateur.

2. "Windows a protege votre PC"
   Cliquez sur "Plus d'informations" puis "Executer quand meme".

3. Le fichier batch ne s'execute pas
   Clic droit sur le .bat et "Executer en tant qu'administrateur".

4. Impossible de sauvegarder / charger
   Verifiez l'espace disque et les permissions d'ecriture.

5. Antivirus en quarantaine
   C'est un faux positif. Ajoutez NC Bat aux exclusions.

6. Liste des etapes vide apres chargement
   Votre fichier .ncbat reference peut-etre une ancienne action.
   Rouvrez et reconstruisez les etapes concernees manuellement.

7. Recuperation de sauvegarde automatique
   NC Bat sauvegarde toutes les 60 secondes dans :
     %USERPROFILE%\\.ncbat\\autosave\\
   Au demarrage, NC Bat propose de recuperer la derniere
   sauvegarde automatique si elle date de moins de 8 heures.
   Vous pouvez aussi l'ouvrir via Fichier > Ouvrir.""",
        "about_content": f"""{APP_NAME}

Copyright 2026 Hiroshi Kelner
Tous droits reserves

{APP_DISPLAY_NAME} est un createur visuel de fichiers batch.

Createur : Hiroshi Kelner
Twitter  : @hiroshiken71
Site web : https://nocodebat.weebly.com

Version      : {APP_VERSION}
Date         : 2026""",
        "terms_content": f"""CONDITIONS D'UTILISATION

{APP_NAME} - Contrat de licence utilisateur final
Copyright 2026 Hiroshi Kelner. Tous droits reserves.

OCTROI DE LICENCE
En utilisant {APP_DISPLAY_NAME}, vous recevez une licence non exclusive pour l'utiliser
sur tous les ordinateurs que vous possedez, pour des projets personnels, educatifs ou commerciaux.

RESPONSABILITE DE L'UTILISATEUR
VOUS ASSUMEZ L'ENTIERE RESPONSABILITE des fichiers batch que vous creez.

PROPRIETE INTELLECTUELLE
Vous ne pouvez PAS revendiquer {APP_DISPLAY_NAME} comme votre creation ni le redistribuer.

VOS FICHIERS VOUS APPARTIENNENT
Les fichiers batch que vous creez vous appartiennent entierement.

En utilisant {APP_DISPLAY_NAME}, vous acceptez ces conditions.

Merci d'utiliser {APP_DISPLAY_NAME} !
- Hiroshi Kelner""",
    }
}

ACTION_NAMES = {
    "en": {
        "Create folder":           "Create folder",
        "Delete file":             "Delete file",
        "Delete folder":           "Delete folder",
        "Move / Rename":           "Move / Rename",
        "Copy files":              "Copy files",
        "Launch program":          "Launch program",
        "Open folder":             "Open folder",
        "Open multiple websites":  "Open multiple websites",
        "Print text":              "Print text",
        "Add comment":             "Add comment",
        "Set window title":        "Set window title",
        "Wait for keypress":       "Wait for keypress",
        "Wait (seconds)":          "Wait (seconds)",
        "Create text file":        "Create text file",
        "Append text to file":     "Append text to file",
        "Run CMD command":         "Run CMD command",
        "Run PowerShell command":  "Run PowerShell command",
        "Kill process":            "Kill process",
        "Set variable (session)":  "Set variable (session)",
        "Set persistent variable": "Set persistent variable",
        "If file exists":          "If file exists",
        "If folder exists":        "If folder exists",
        "Loop files in folder":    "Loop files in folder",
        "Change directory":        "Change directory",
        "Run as administrator":    "Run as administrator",
        "Clear screen":            "Clear screen",
        "Define label":            "Define label",
        "Goto label":              "Goto label",
        "Exit script":             "Exit script",
        "Check errorlevel":        "Check errorlevel",
        "Log to file":             "Log to file",
        "Find in file":            "Find in file",
        "Type file":               "Type file",
        "Ping host":               "Ping host",
    },
    "fr": {
        "Create folder":           "Creer un dossier",
        "Delete file":             "Supprimer un fichier",
        "Delete folder":           "Supprimer un dossier",
        "Move / Rename":           "Deplacer / Renommer",
        "Copy files":              "Copier des fichiers",
        "Launch program":          "Lancer un programme",
        "Open folder":             "Ouvrir un dossier",
        "Open multiple websites":  "Ouvrir plusieurs sites web",
        "Print text":              "Afficher du texte",
        "Add comment":             "Ajouter un commentaire",
        "Set window title":        "Titre de la fenetre",
        "Wait for keypress":       "Attendre une touche",
        "Wait (seconds)":          "Attendre (secondes)",
        "Create text file":        "Creer un fichier texte",
        "Append text to file":     "Ajouter du texte",
        "Run CMD command":         "Commande CMD",
        "Run PowerShell command":  "Commande PowerShell",
        "Kill process":            "Tuer un processus",
        "Set variable (session)":  "Variable de session",
        "Set persistent variable": "Variable persistante",
        "If file exists":          "Si le fichier existe",
        "If folder exists":        "Si le dossier existe",
        "Loop files in folder":    "Boucler les fichiers",
        "Change directory":        "Changer de repertoire",
        "Run as administrator":    "Executer en admin",
        "Clear screen":            "Effacer l'ecran",
        "Define label":            "Definir une etiquette",
        "Goto label":              "Aller a l'etiquette",
        "Exit script":             "Quitter le script",
        "Check errorlevel":        "Verifier errorlevel",
        "Log to file":             "Ecrire dans un journal",
        "Find in file":            "Chercher dans un fichier",
        "Type file":               "Afficher un fichier",
        "Ping host":               "Ping",
    }
}

FIELD_LABELS = {
    "en": {
        "folder_name": "Folder name",
        "folder_path": "In folder (optional)",
        "prog_path":   "Program path",
        "prog_args":   "Arguments (optional)",
        "src":         "Source path",
        "dst":         "Destination path",
        "text":        "Text",
        "url":         "URL",
        "urls":        "URLs (one per line)",
        "ps_cmd":      "PowerShell command",
        "cmd":         "Command",
        "seconds":     "Seconds",
        "path":        "File path",
        "content":     "Content",
        "pname":       "Process name",
        "folder":      "Folder path",
        "var":         "Variable name",
        "value":       "Value",
        "if_true":     "Command if true",
        "if_false":    "Command if false",
        "loop_cmd":    "Command per file (use %%f)",
        "label":       "Label name",
        "exit_code":   "Exit code (0 = success)",
    },    "fr": {
        "folder_name": "Nom du dossier",
        "folder_path": "Dans le dossier (optionnel)",
        "prog_path":   "Chemin du programme",
        "prog_args":   "Arguments (optionnel)",
        "src":         "Chemin source",
        "dst":         "Chemin destination",
        "text":        "Texte",
        "url":         "URL",
        "urls":        "URLs (une par ligne)",
        "ps_cmd":      "Commande PowerShell",
        "cmd":         "Commande",
        "seconds":     "Secondes",
        "path":        "Chemin du fichier",
        "content":     "Contenu",
        "pname":       "Nom du processus",
        "folder":      "Chemin du dossier",
        "var":         "Nom de la variable",
        "value":       "Valeur",
        "if_true":     "Commande si vrai",
        "if_false":    "Commande si faux",
        "loop_cmd":    "Commande par fichier (utiliser %%f)",
        "label":       "Nom de l'etiquette",
        "exit_code":   "Code de sortie (0 = succes)",
    }
}

ACTION_TOOLTIPS = {
    "en": {
        "Create folder":           "Creates a directory with mkdir.",
        "Delete file":             "Permanently deletes a file (del /f /q). Cannot be undone.",
        "Delete folder":           "Recursively deletes a folder and all its contents (rmdir /s /q).",
        "Move / Rename":           "Moves or renames a file or folder using the move command.",
        "Copy files":              "Copies files from a source path to a destination path.",
        "Launch program":          "Starts an executable or script with optional arguments.",
        "Open folder":             "Opens a folder in Windows Explorer.",
        "Open multiple websites":  "Opens each URL (one per line) in the default browser.",
        "Print text":              "Prints a line of text to the console window (echo).",
        "Add comment":             "Inserts a REM comment line. Not executed, just documentation.",
        "Set window title":        "Sets the title text of the console window.",
        "Wait for keypress":       "Pauses the script until the user presses any key (pause).",
        "Wait (seconds)":          "Pauses execution for a set number of seconds (timeout).",
        "Create text file":        "Creates or overwrites a text file with the given content.",
        "Append text to file":     "Appends a line of text to an existing file.",
        "Run CMD command":         "Runs any raw batch command or statement.",
        "Run PowerShell command":  "Runs a command inside a PowerShell session.",
        "Kill process":            "Force-terminates a running process by its image name.",
        "Set variable (session)":  "Sets an env variable for this session only (set). Not permanent.",
        "Set persistent variable": "Permanently sets an env variable via setx. Takes effect on next session.",
        "If file exists":          "Branches based on whether a file exists. Provide commands for each branch.",
        "If folder exists":        "Branches based on whether a folder exists. Provide commands for each branch.",
        "Loop files in folder":    "Runs a command once for each file in a folder. Use %%f as the filename.",
        "Change directory":        "Changes the current working directory (cd /d).",
        "Run as administrator":    "Inserts a UAC self-elevation check at the top of the script.",
        "Clear screen":            "Clears the console window (cls).",
        "Define label":            "Defines a GOTO target label. Use with 'Goto label' to jump to it.",
        "Goto label":              "Jumps to a label defined elsewhere in the script (goto).",
        "Exit script":             "Exits the script immediately with an optional error code (exit /b).",
        "Check errorlevel":        "Branches based on %errorlevel% after a previous command. 0 = success.",
        "Log to file":             "Appends a timestamped message to a log file.",
        "Find in file":            "Searches for a text pattern in a file (findstr /i).",
        "Type file":               "Prints the full contents of a text file to the console (type).",
        "Ping host":               "Pings a hostname or IP address a given number of times.",
    },
    "fr": {
        "Create folder":           "Cree un repertoire avec mkdir.",
        "Delete file":             "Supprime definitivement un fichier (del /f /q). Irreversible.",
        "Delete folder":           "Supprime recursivement un dossier et tout son contenu (rmdir /s /q).",
        "Move / Rename":           "Deplace ou renomme un fichier ou dossier avec la commande move.",
        "Copy files":              "Copie des fichiers de la source vers la destination.",
        "Launch program":          "Lance un executable ou script avec des arguments optionnels.",
        "Open folder":             "Ouvre un dossier dans l'Explorateur Windows.",
        "Open multiple websites":  "Ouvre chaque URL (une par ligne) dans le navigateur par defaut.",
        "Print text":              "Affiche une ligne de texte dans la console (echo).",
        "Add comment":             "Insere une ligne REM. Non executee, sert de documentation.",
        "Set window title":        "Definit le titre de la fenetre de commandes.",
        "Wait for keypress":       "Met en pause jusqu'a ce que l'utilisateur appuie sur une touche.",
        "Wait (seconds)":          "Met en pause pour un nombre de secondes defini (timeout).",
        "Create text file":        "Cree ou ecrase un fichier texte avec le contenu indique.",
        "Append text to file":     "Ajoute une ligne de texte a un fichier existant.",
        "Run CMD command":         "Execute une commande batch brute.",
        "Run PowerShell command":  "Execute une commande dans une session PowerShell.",
        "Kill process":            "Termine de force un processus par son nom d'image.",
        "Set variable (session)":  "Definit une variable d'env pour cette session uniquement (set).",
        "Set persistent variable": "Definit une variable d'env de facon permanente via setx.",
        "If file exists":          "Branche selon qu'un fichier existe. Fournissez les commandes pour chaque branche.",
        "If folder exists":        "Branche selon qu'un dossier existe. Fournissez les commandes pour chaque branche.",
        "Loop files in folder":    "Execute une commande pour chaque fichier d'un dossier. Utilisez %%f.",
        "Change directory":        "Change le repertoire de travail courant (cd /d).",
        "Run as administrator":    "Insere une verification d'elevation UAC au debut du script.",
        "Clear screen":            "Efface la fenetre de la console (cls).",
        "Define label":            "Definit une etiquette cible GOTO. Utilisez avec 'Goto label'.",
        "Goto label":              "Saute vers une etiquette definie ailleurs dans le script (goto).",
        "Exit script":             "Quitte le script avec un code de sortie optionnel (exit /b).",
        "Check errorlevel":        "Branche selon %errorlevel% apres une commande. 0 = succes.",
        "Log to file":             "Ajoute un message horodate dans un fichier journal.",
        "Find in file":            "Recherche un motif dans un fichier (findstr /i).",
        "Type file":               "Affiche le contenu complet d'un fichier texte (type).",
        "Ping host":               "Envoie des requetes ping a un hote ou une adresse IP.",
    }
}


# ─── Generator functions ──────────────────────────────────────────────────────
def gen_create_folder(v):
    n, p = v.get("folder_name",""), v.get("folder_path","")
    return ([f'cd /d "{p}"'] if p else []) + [f'mkdir "{n}"']

def gen_delete_file(v):
    return [f'del /f /q "{v.get("path","")}"']

def gen_delete_folder(v):
    return [f'rmdir /s /q "{v.get("folder","")}"']

def gen_move_file(v):
    return [f'move "{v.get("src","")}" "{v.get("dst","")}"']

def gen_launch_program(v):
    p = v.get("prog_path","").strip().strip('"')
    a = v.get("prog_args","")
    return [f'start "" "{p}" {a}' if a else f'start "" "{p}"']

def gen_copy_files(v):
    return [f'copy "{v.get("src","")}" "{v.get("dst","")}"']

def gen_open_folder(v):
    return [f'start "" "{v.get("folder","")}"']

def gen_open_websites(v):
    # Split on newlines so URLs with query strings are handled correctly
    urls = [u.strip() for u in v.get("urls","").splitlines() if u.strip()]
    return [f'start "" "{u}"' for u in urls]

def gen_echo_text(v):
    t = v.get("text", "")
    return ["echo."] if not t.strip() else [f"echo {t}"]

def gen_comment(v):
    return [f'REM {v.get("text","")}']

def gen_set_title(v):
    return [f'title {v.get("text","")}']

def gen_pause(v):
    return ["pause"]

def gen_wait(v):
    return [f'timeout /t {v.get("seconds","1").strip() or "1"} /nobreak']

def gen_create_file(v):
    # Parenthesized echo handles special characters more safely than bare echo > path
    content = v.get("content","")
    path    = v.get("path","")
    return [f'(echo {content}) > "{path}"']

def gen_append(v):
    content = v.get("content","")
    path    = v.get("path","")
    return [f'(echo {content}) >> "{path}"']

def gen_cmd(v):
    return [v.get("cmd","")]

def gen_powershell(v):
    return [f'powershell -NoProfile -Command "{v.get("ps_cmd","")}"']

def gen_kill(v):
    return [f'taskkill /IM "{v.get("pname","")}" /F']

def gen_set_env(v):
    return [f'set {v.get("var","")}={v.get("value","")}']

def gen_set_persistent(v):
    return [f'setx {v.get("var","")} "{v.get("value","")}"']

def gen_if_exists(v):
    path     = v.get("path","")
    true_cmd = v.get("if_true","").strip()  or "echo File exists"
    false_cmd= v.get("if_false","").strip() or "echo File not found"
    return [f'if exist "{path}" (', f'  {true_cmd}', ') else (', f'  {false_cmd}', ')']

def gen_if_folder_exists(v):
    folder   = v.get("folder","").rstrip("\\")
    true_cmd = v.get("if_true","").strip()  or "echo Folder exists"
    false_cmd= v.get("if_false","").strip() or "echo Folder not found"
    return [f'if exist "{folder}\\" (', f'  {true_cmd}', ') else (', f'  {false_cmd}', ')']

def gen_loop(v):
    folder  = v.get("folder","")
    cmd     = v.get("loop_cmd","").strip() or "echo %%f"
    return [f'for %%f in ("{folder}\\*") do {cmd}']

def gen_cd(v):
    return [f'cd /d "{v.get("folder","")}"']

def gen_runas_admin(v):
    return [
        "NET SESSION >nul 2>&1",
        "IF %ERRORLEVEL% NEQ 0 (",
        "    PowerShell -Command \"Start-Process '%~f0' -Verb RunAs\"",
        "    EXIT",
        ")",
    ]

def gen_cls(v):
    return ["cls"]

def gen_define_label(v):
    name = v.get("label", "").strip().replace(" ", "_")
    return [f":{name}"]

def gen_goto(v):
    name = v.get("label", "").strip().replace(" ", "_")
    return [f"goto {name}"]

def gen_exit_script(v):
    code = v.get("value", "0").strip() or "0"
    return [f"exit /b {code}"]

def gen_check_errorlevel(v):
    code     = v.get("var",      "0").strip() or "0"
    true_cmd = v.get("if_true",  "").strip()  or "echo Error detected"
    false_cmd= v.get("if_false", "").strip()  or "echo OK"
    return [
        f"if %errorlevel% neq {code} (",
        f"  {true_cmd}",
        ") else (",
        f"  {false_cmd}",
        ")",
    ]

def gen_log_to_file(v):
    msg  = v.get("text",  "")
    path = v.get("path",  "log.txt")
    return [
        f'for /f "tokens=1-3 delims=/ " %%a in (\'date /t\') do set _d=%%a-%%b-%%c',
        f'for /f "tokens=1-2 delims=: " %%a in (\'time /t\') do set _t=%%a:%%b',
        f'(echo [%_d% %_t%] {msg}) >> "{path}"',
    ]

def gen_find_in_file(v):
    pattern = v.get("text",   "")
    path    = v.get("path",   "")
    return [f'findstr /i "{pattern}" "{path}"']

def gen_type_file(v):
    path = v.get("path", "")
    return [f'type "{path}"']

def gen_ping(v):
    host  = v.get("text",    "google.com")
    count = v.get("seconds", "4").strip() or "4"
    return [f"ping -n {count} {host}"]


# ─── Action definitions ───────────────────────────────────────────────────────
# Field tuples: (field_label_key, var_key)  or  (field_label_key, var_key, "textarea")
ACTION_DEFS = {
    "Create folder":           {"fields":[("folder_name","folder_name"),("folder_path","folder_path")],            "generator":gen_create_folder},
    "Delete file":             {"fields":[("path","path")],                                                        "generator":gen_delete_file},
    "Delete folder":           {"fields":[("folder","folder")],                                                    "generator":gen_delete_folder},
    "Move / Rename":           {"fields":[("src","src"),("dst","dst")],                                            "generator":gen_move_file},
    "Copy files":              {"fields":[("src","src"),("dst","dst")],                                            "generator":gen_copy_files},
    "Launch program":          {"fields":[("prog_path","prog_path"),("prog_args","prog_args")],                     "generator":gen_launch_program},
    "Open folder":             {"fields":[("folder","folder")],                                                    "generator":gen_open_folder},
    "Open multiple websites":  {"fields":[("urls","urls","textarea")],                                             "generator":gen_open_websites},
    "Print text":              {"fields":[("text","text")],                                                        "generator":gen_echo_text},
    "Add comment":             {"fields":[("text","text")],                                                        "generator":gen_comment},
    "Set window title":        {"fields":[("text","text")],                                                        "generator":gen_set_title},
    "Wait for keypress":       {"fields":[],                                                                       "generator":gen_pause},
    "Wait (seconds)":          {"fields":[("seconds","seconds")],                                                  "generator":gen_wait},
    "Create text file":        {"fields":[("path","path"),("content","content")],                                  "generator":gen_create_file},
    "Append text to file":     {"fields":[("path","path"),("content","content")],                                  "generator":gen_append},
    "Run CMD command":         {"fields":[("cmd","cmd")],                                                          "generator":gen_cmd},
    "Run PowerShell command":  {"fields":[("ps_cmd","ps_cmd")],                                                    "generator":gen_powershell},
    "Kill process":            {"fields":[("pname","pname")],                                                      "generator":gen_kill},
    "Set variable (session)":  {"fields":[("var","var"),("value","value")],                                        "generator":gen_set_env},
    "Set persistent variable": {"fields":[("var","var"),("value","value")],                                        "generator":gen_set_persistent},
    "If file exists":          {"fields":[("path","path"),("if_true","if_true"),("if_false","if_false")],          "generator":gen_if_exists},
    "If folder exists":        {"fields":[("folder","folder"),("if_true","if_true"),("if_false","if_false")],      "generator":gen_if_folder_exists},
    "Loop files in folder":    {"fields":[("folder","folder"),("loop_cmd","loop_cmd")],                            "generator":gen_loop},
    "Change directory":        {"fields":[("folder","folder")],                                                    "generator":gen_cd},
    "Run as administrator":    {"fields":[],                                                                       "generator":gen_runas_admin},
    "Clear screen":            {"fields":[],                                                                       "generator":gen_cls},
    "Define label":            {"fields":[("label","label")],                                                      "generator":gen_define_label},
    "Goto label":              {"fields":[("label","label")],                                                      "generator":gen_goto},
    "Exit script":             {"fields":[("exit_code","value")],                                                   "generator":gen_exit_script},
    "Check errorlevel":        {"fields":[("exit_code","var"),("if_true","if_true"),("if_false","if_false")],       "generator":gen_check_errorlevel},
    "Log to file":             {"fields":[("text","text"),("path","path")],                                        "generator":gen_log_to_file},
    "Find in file":            {"fields":[("text","text"),("path","path")],                                        "generator":gen_find_in_file},
    "Type file":               {"fields":[("path","path")],                                                        "generator":gen_type_file},
    "Ping host":               {"fields":[("text","text"),("seconds","seconds")],                                  "generator":gen_ping},
}

# Old project-file compat alias: "Set environment variable" maps to session setter
ACTION_DEFS["Set environment variable"] = ACTION_DEFS["Set variable (session)"]

_ALL_ACTION_KEYS = [k for k in ACTION_DEFS if k not in ("Set environment variable",)]

# ─── Syntax highlight keyword groups ─────────────────────────────────────────
_SH_DANGER_CMDS  = re.compile(
    r"^\s*(?:del|rmdir|rd|format)\b", re.I)
_SH_KEYWORD_CMDS = re.compile(
    r"^\s*(?:@echo\s+off|@echo|echo|set|setx|if|for|mkdir|md|move|copy|xcopy"
    r"|start|cd|title|pause|timeout|taskkill|powershell|net|exit|call|goto"
    r"|pushd|popd|cls|type|more|find|findstr|attrib|icacls|schtasks|reg|ping)\b", re.I)
_SH_COMMENT      = re.compile(r"^\s*rem\b", re.I)
_SH_HEADER       = re.compile(r"^\s*@echo\s+off\s*$", re.I)
_SH_STRING       = re.compile(r'"[^"]*"')
_SH_VARIABLE     = re.compile(r'%[^%\r\n]+%')

# ─── Action category icons ────────────────────────────────────────────────────
_ACTION_ICONS = {
    "Create folder":           "▣",
    "Delete file":             "✕",
    "Delete folder":           "✕",
    "Move / Rename":           "⇄",
    "Copy files":              "⧉",
    "Launch program":          "▶",
    "Open folder":             "▣",
    "Open multiple websites":  "⊕",
    "Print text":              "≡",
    "Add comment":             "//",
    "Set window title":        "◻",
    "Wait for keypress":       "⌨",
    "Wait (seconds)":          "◎",
    "Create text file":        "⊞",
    "Append text to file":     "⊟",
    "Run CMD command":         ">_",
    "Run PowerShell command":  "$",
    "Kill process":            "⊗",
    "Set variable (session)":  "=",
    "Set persistent variable": ":=",
    "If file exists":          "?",
    "If folder exists":        "?",
    "Loop files in folder":    "↻",
    "Change directory":        "cd",
    "Run as administrator":    "⚡",
    "Clear screen":            "✦",
    "Define label":            ":",
    "Goto label":              "→",
    "Exit script":             "⏹",
    "Check errorlevel":        "✔",
    "Log to file":             "📋",
    "Find in file":            "🔍",
    "Type file":               "📄",
    "Ping host":               "⇆",
}


# ─── BAT import parser ────────────────────────────────────────────────────────
def parse_bat_file(filepath):
    actions = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.lower() == '@echo off':
            i += 1; continue
        ll = line.lower()
        found = False
        if ll.startswith('rem ') or ll == 'rem':
            actions.append(("Add comment", {"text": line[4:]})); found = True
        elif ll.startswith('title '):
            actions.append(("Set window title", {"text": line[6:]})); found = True
        elif ll.startswith('mkdir'):
            m = re.search(r'mkdir\s+"?([^"]+)"?', line, re.I)
            if m: actions.append(("Create folder",{"folder_name":m.group(1),"folder_path":""})); found=True
        elif ll.startswith('rmdir'):
            m = re.search(r'rmdir\s+(?:/s\s+)?(?:/q\s+)?"?([^"]+)"?', line, re.I)
            if m: actions.append(("Delete folder",{"folder":m.group(1)})); found=True
        elif ll.startswith('del '):
            m = re.search(r'del\s+(?:/f\s+)?(?:/q\s+)?"?([^"]+)"?', line, re.I)
            if m: actions.append(("Delete file",{"path":m.group(1)})); found=True
        elif ll.startswith('move '):
            m = re.search(r'move\s+"?([^"]+)"?\s+"?([^"]+)"?', line, re.I)
            if m: actions.append(("Move / Rename",{"src":m.group(1),"dst":m.group(2)})); found=True
        elif ll.startswith('start'):
            m = re.search(r'start\s+""?\s+"?([^"]+)"?(?:\s+(.+))?', line, re.I)
            if m:
                p, a = m.group(1), m.group(2) or ""
                if p.startswith(('http://','https://')):
                    actions.append(("Open multiple websites",{"urls":p}))
                else:
                    actions.append(("Launch program",{"prog_path":p,"prog_args":a}))
                found = True
        elif ll.startswith('copy'):
            m = re.search(r'copy\s+"?([^"]+)"?\s+"?([^"]+)"?', line, re.I)
            if m: actions.append(("Copy files",{"src":m.group(1),"dst":m.group(2)})); found=True
        elif ll.startswith('echo') and '>' not in line:
            m = re.search(r'echo\s+(.+)', line, re.I)
            if m: actions.append(("Print text",{"text":m.group(1)})); found=True
        elif ll == 'pause':
            actions.append(("Wait for keypress",{})); found=True
        elif ll.startswith('timeout'):
            m = re.search(r'timeout\s+/t\s+(\d+)', line, re.I)
            if m: actions.append(("Wait (seconds)",{"seconds":m.group(1)})); found=True
        elif ll.startswith('taskkill'):
            m = re.search(r'taskkill\s+/IM\s+"?([^"]+)"?', line, re.I)
            if m: actions.append(("Kill process",{"pname":m.group(1)})); found=True
        elif ll.startswith('setx '):
            m = re.search(r'setx\s+(\w+)\s+"?([^"]*)"?', line, re.I)
            if m: actions.append(("Set persistent variable",{"var":m.group(1),"value":m.group(2)})); found=True
        elif ll.startswith('set '):
            m = re.search(r'set\s+(\w+)=(.+)', line, re.I)
            if m: actions.append(("Set variable (session)",{"var":m.group(1),"value":m.group(2)})); found=True
        elif ll.startswith('cd '):
            m = re.search(r'cd\s+(?:/d\s+)?"?([^"]+)"?', line, re.I)
            if m: actions.append(("Change directory",{"folder":m.group(1)})); found=True
        elif ll.startswith('powershell'):
            ps = [line]
            i += 1
            while i < len(lines) and lines[i].strip().endswith('^'):
                ps.append(lines[i].strip()); i += 1
            if i < len(lines): ps.append(lines[i].strip())
            actions.append(("Run PowerShell command",{"ps_cmd":' '.join(ps)})); found=True
        if not found:
            actions.append(("Run CMD command",{"cmd":line}))
        i += 1
    return actions


# ─── Default templates bundled with the app ───────────────────────────────────
DEFAULT_TEMPLATES = {

    "File Backup": {
        "version": APP_VERSION,
        "next_action_id": 11,
        "items": [
            {"type":"action","action":"Add comment","values":{"text":"File Backup Script — copies files to a dated backup folder"},"id":0},
            {"type":"action","action":"Run as administrator","values":{},"id":1},
            {"type":"action","action":"Set window title","values":{"text":"File Backup"},"id":2},
            {"type":"action","action":"Clear screen","values":{},"id":3},
            {"type":"action","action":"Print text","values":{"text":"Starting backup..."},"id":4},
            {"type":"action","action":"Set variable (session)","values":{"var":"TODAY","value":"%date:~-4%%date:~3,2%%date:~0,2%"},"id":5},
            {"type":"action","action":"Create folder","values":{"folder_name":"Backup_%TODAY%","folder_path":"C:\\Backups"},"id":6},
            {"type":"action","action":"Copy files","values":{"src":"C:\\MyFiles\\*","dst":"C:\\Backups\\Backup_%TODAY%\\"},"id":7},
            {"type":"action","action":"Check errorlevel","values":{"var":"0","if_true":"echo Backup completed successfully!","if_false":"echo WARNING: Backup may have failed."},"id":8},
            {"type":"action","action":"Log to file","values":{"text":"Backup run","path":"C:\\Backups\\backup_log.txt"},"id":9},
            {"type":"action","action":"Print text","values":{"text":""},"id":10},
            {"type":"action","action":"Print text","values":{"text":"All done. Press any key to close."},"id":11},
            {"type":"action","action":"Wait for keypress","values":{},"id":12},
        ]
    },

    "System Temp Cleanup": {
        "version": APP_VERSION,
        "next_action_id": 9,
        "items": [
            {"type":"action","action":"Add comment","values":{"text":"Deletes temporary files from common Windows temp folders"},"id":0},
            {"type":"action","action":"Run as administrator","values":{},"id":1},
            {"type":"action","action":"Set window title","values":{"text":"System Cleanup"},"id":2},
            {"type":"action","action":"Clear screen","values":{},"id":3},
            {"type":"action","action":"Print text","values":{"text":"Cleaning temporary files — please wait..."},"id":4},
            {"type":"action","action":"Print text","values":{"text":""},"id":5},
            {"type":"action","action":"Run CMD command","values":{"cmd":"del /f /q /s \"%TEMP%\\*\" >nul 2>&1"},"id":6},
            {"type":"action","action":"Run CMD command","values":{"cmd":"del /f /q /s \"C:\\Windows\\Temp\\*\" >nul 2>&1"},"id":7},
            {"type":"action","action":"Run CMD command","values":{"cmd":"rd /s /q \"%TEMP%\" >nul 2>&1 & mkdir \"%TEMP%\" >nul 2>&1"},"id":8},
            {"type":"action","action":"Print text","values":{"text":"Temp folders cleared."},"id":9},
            {"type":"action","action":"Print text","values":{"text":""},"id":10},
            {"type":"action","action":"Print text","values":{"text":"Cleanup complete. Press any key to exit."},"id":11},
            {"type":"action","action":"Wait for keypress","values":{},"id":12},
        ]
    },

    "Project Folder Setup": {
        "version": APP_VERSION,
        "next_action_id": 10,
        "items": [
            {"type":"action","action":"Add comment","values":{"text":"Creates a standard project folder structure in the current directory"},"id":0},
            {"type":"action","action":"Set window title","values":{"text":"Project Setup"},"id":1},
            {"type":"action","action":"Clear screen","values":{},"id":2},
            {"type":"action","action":"Print text","values":{"text":"Creating project folders..."},"id":3},
            {"type":"group","name":"Folders","items":[
                {"type":"action","action":"Create folder","values":{"folder_name":"src","folder_path":""},"id":4},
                {"type":"action","action":"Create folder","values":{"folder_name":"dist","folder_path":""},"id":5},
                {"type":"action","action":"Create folder","values":{"folder_name":"docs","folder_path":""},"id":6},
                {"type":"action","action":"Create folder","values":{"folder_name":"tests","folder_path":""},"id":7},
                {"type":"action","action":"Create folder","values":{"folder_name":"assets","folder_path":""},"id":8},
            ]},
            {"type":"action","action":"Create text file","values":{"path":"README.md","content":"# Project Name"},"id":9},
            {"type":"action","action":"Print text","values":{"text":""},"id":10},
            {"type":"action","action":"Print text","values":{"text":"Project structure created! Opening folder..."},"id":11},
            {"type":"action","action":"Open folder","values":{"folder":"."},"id":12},
        ]
    },

    "Network Diagnostics": {
        "version": APP_VERSION,
        "next_action_id": 12,
        "items": [
            {"type":"action","action":"Set window title","values":{"text":"Network Diagnostics"},"id":0},
            {"type":"action","action":"Clear screen","values":{},"id":1},
            {"type":"action","action":"Print text","values":{"text":"Running network diagnostics..."},"id":2},
            {"type":"action","action":"Print text","values":{"text":""},"id":3},
            {"type":"group","name":"Ping Tests","items":[
                {"type":"action","action":"Print text","values":{"text":"--- Google DNS (8.8.8.8) ---"},"id":4},
                {"type":"action","action":"Ping host","values":{"text":"8.8.8.8","seconds":"4"},"id":5},
                {"type":"action","action":"Print text","values":{"text":""},"id":6},
                {"type":"action","action":"Print text","values":{"text":"--- Cloudflare DNS (1.1.1.1) ---"},"id":7},
                {"type":"action","action":"Ping host","values":{"text":"1.1.1.1","seconds":"4"},"id":8},
                {"type":"action","action":"Print text","values":{"text":""},"id":9},
                {"type":"action","action":"Print text","values":{"text":"--- google.com ---"},"id":10},
                {"type":"action","action":"Ping host","values":{"text":"google.com","seconds":"4"},"id":11},
            ]},
            {"type":"action","action":"Print text","values":{"text":""},"id":12},
            {"type":"action","action":"Print text","values":{"text":"Diagnostics complete. Press any key to close."},"id":13},
            {"type":"action","action":"Wait for keypress","values":{},"id":14},
        ]
    },

    "Launch and Log": {
        "version": APP_VERSION,
        "next_action_id": 7,
        "items": [
            {"type":"action","action":"Add comment","values":{"text":"Launches a program and logs the outcome to a file"},"id":0},
            {"type":"action","action":"Set window title","values":{"text":"Launch and Log"},"id":1},
            {"type":"action","action":"Log to file","values":{"text":"Script started","path":"run_log.txt"},"id":2},
            {"type":"action","action":"Print text","values":{"text":"Launching program..."},"id":3},
            {"type":"action","action":"Launch program","values":{"prog_path":"C:\\path\\to\\program.exe","prog_args":""},"id":4},
            {"type":"action","action":"Check errorlevel","values":{"var":"0","if_true":"echo Program exited successfully.","if_false":"echo Program exited with an error."},"id":5},
            {"type":"action","action":"Log to file","values":{"text":"Script finished","path":"run_log.txt"},"id":6},
            {"type":"action","action":"Wait for keypress","values":{},"id":7},
        ]
    },

    "Open Daily Websites": {
        "version": APP_VERSION,
        "next_action_id": 5,
        "items": [
            {"type":"action","action":"Add comment","values":{"text":"Opens a set of websites in your default browser — edit the URLs to match your daily routine"},"id":0},
            {"type":"action","action":"Set window title","values":{"text":"Daily Browser Launch"},"id":1},
            {"type":"action","action":"Print text","values":{"text":"Opening your daily sites..."},"id":2},
            {"type":"action","action":"Open multiple websites","values":{"urls":"https://gmail.com\nhttps://github.com\nhttps://news.ycombinator.com"},"id":3},
            {"type":"action","action":"Print text","values":{"text":"Done!"},"id":4},
            {"type":"action","action":"Wait (seconds)","values":{"seconds":"2"},"id":5},
        ]
    },

    "App Installer Prep": {
        "version": APP_VERSION,
        "next_action_id": 9,
        "items": [
            {"type":"action","action":"Add comment","values":{"text":"Closes common apps, clears temp files, then launches an installer"},"id":0},
            {"type":"action","action":"Run as administrator","values":{},"id":1},
            {"type":"action","action":"Set window title","values":{"text":"Installer Prep"},"id":2},
            {"type":"action","action":"Clear screen","values":{},"id":3},
            {"type":"action","action":"Print text","values":{"text":"Preparing installation environment..."},"id":4},
            {"type":"group","name":"Close Running Apps","items":[
                {"type":"action","action":"Kill process","values":{"pname":"chrome.exe"},"id":5},
                {"type":"action","action":"Kill process","values":{"pname":"firefox.exe"},"id":6},
                {"type":"action","action":"Kill process","values":{"pname":"msedge.exe"},"id":7},
            ]},
            {"type":"action","action":"Run CMD command","values":{"cmd":"del /f /q \"%TEMP%\\*\" >nul 2>&1"},"id":8},
            {"type":"action","action":"Print text","values":{"text":"Environment ready. Launching installer..."},"id":9},
            {"type":"action","action":"Launch program","values":{"prog_path":"setup.exe","prog_args":""},"id":10},
            {"type":"action","action":"Wait for keypress","values":{},"id":11},
        ]
    },

    "Script Starter": {
        "version": APP_VERSION,
        "next_action_id": 4,
        "items": [
            {"type":"action","action":"Add comment","values":{"text":"A clean starting point — admin check, titled window, clear screen, welcome message"},"id":0},
            {"type":"action","action":"Run as administrator","values":{},"id":1},
            {"type":"action","action":"Set window title","values":{"text":"My Script"},"id":2},
            {"type":"action","action":"Clear screen","values":{},"id":3},
            {"type":"action","action":"Print text","values":{"text":"=============================="},"id":4},
            {"type":"action","action":"Print text","values":{"text":"  My Script"},"id":5},
            {"type":"action","action":"Print text","values":{"text":"=============================="},"id":6},
            {"type":"action","action":"Print text","values":{"text":""},"id":7},
        ]
    },

}

# ─── Main application ─────────────────────────────────────────────────────────
class BatBuilderApp:
    def __init__(self, root):
        self.root         = root
        self.current_lang = self._load_lang()
        self.current_project_path = None
        self.has_unsaved_changes  = False
        self.items          = []
        self.next_action_id = 0
        self._cached_lines  = None
        self._undo_stack    = []
        self._redo_stack    = []
        self._drag_idx      = None
        self._status_job    = None
        self._theme_name    = "dark"
        self.project_name   = "Untitled"

        self.root.title(self.t("app_title"))
        self.root.geometry("1200x780")
        self.root.minsize(920, 620)

        self._build_ui()
        self._bind_shortcuts()
        self.refresh_preview()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self._autosave_dir = os.path.join(os.path.expanduser("~"), ".ncbat", "autosave")
        os.makedirs(self._autosave_dir, exist_ok=True)
        self._schedule_autosave()
        self._start_update_check()
        self.check_first_run()

    # ── Translation helpers ──────────────────────────────────────────────────
    def t(self, k):  return TRANSLATIONS[self.current_lang].get(k, k)
    def ta(self, k): return ACTION_NAMES[self.current_lang].get(k, k)
    def tf(self, k): return FIELD_LABELS[self.current_lang].get(k, k)
    def T(self):     return THEMES[self._theme_name]

    # ── Keyboard shortcuts ───────────────────────────────────────────────────
    def _bind_shortcuts(self):
        r = self.root
        r.bind("<Control-s>", lambda e: self.save_project())
        r.bind("<Control-S>", lambda e: self.save_project())
        r.bind("<Control-n>", lambda e: self.new_project())
        r.bind("<Control-N>", lambda e: self.new_project())
        r.bind("<Control-z>", lambda e: self.undo())
        r.bind("<Control-Z>", lambda e: self.undo())
        r.bind("<Control-y>", lambda e: self.redo())
        r.bind("<Control-Y>", lambda e: self.redo())
        r.bind("<Control-d>", lambda e: self.duplicate_step())
        r.bind("<Control-D>", lambda e: self.duplicate_step())
        r.bind("<Delete>",    lambda e: self._del_if_steps_focused())
        r.bind("<Control-Up>",   lambda e: self.move_up())
        r.bind("<Control-Down>", lambda e: self.move_down())
        r.bind("<F2>",        lambda e: self._f2_edit())
        r.bind("<Control-e>", lambda e: self.save_bat())
        r.bind("<Control-E>", lambda e: self.save_bat())

    def _f2_edit(self):
        """Edit selected step if the steps list has focus or a step is selected."""
        if self.steps_lb.curselection():
            self.edit_step()

    def _del_if_steps_focused(self):
        focused = self.root.focus_get()
        if focused is self.steps_lb.lb:
            self.remove_step()

    def toggle_fullscreen(self):
        self._is_fullscreen = not self._is_fullscreen
        self.root.attributes("-fullscreen", self._is_fullscreen)
        self._fs_btn.config(text="✕  Exit Fullscreen" if self._is_fullscreen else "⛶  Fullscreen")

    def _exit_fullscreen(self):
        if self._is_fullscreen:
            self._is_fullscreen = False
            self.root.attributes("-fullscreen", False)
            self._fs_btn.config(text="⛶  Fullscreen")

    def _on_escape(self):
        """Escape: exit fullscreen first; otherwise clear the search bar."""
        if self._is_fullscreen:
            self._exit_fullscreen()
        else:
            self._clear_search()

    # ── Theme switching ──────────────────────────────────────────────────────
    def toggle_theme(self):
        old_t = THEMES[self._theme_name]
        self._theme_name = "light" if self._theme_name == "dark" else "dark"
        new_t = THEMES[self._theme_name]

        # Update all module-level color globals so new widgets use correct colors
        _apply_theme_globals(self._theme_name)

        # Update action-listbox hover state vars
        self._alb_hover_bg  = _ALB_HOVER_BG
        self._alb_norm_bg   = _LB_BG
        self._alb_alt_bg_h  = _ALB_ALT_ROW_BG

        # Build a normalised old->new color mapping
        color_map = {}
        for k in old_t:
            ov = old_t[k].lower()
            nv = new_t[k].lower()
            if ov not in color_map:
                color_map[ov] = nv

        # Walk every widget and swap colours
        self._recolor_widget_tree(self.root, color_map)

        # Redraw RoundedButton canvases (they cache colours internally)
        self._refresh_rounded_buttons(self.root)

        # Refresh lists so alt-row tints update
        self._fill_action_lb(self._action_keys)
        sel = self.action_lb.lb.curselection()
        if sel:
            self.action_lb.lb.selection_set(sel[0])
        self.rebuild_steps()
        self.refresh_preview()

        label = "☀  Light Mode" if self._theme_name == "dark" else "☾  Dark Mode"
        self._theme_toggle_btn.config(text=label)
        self._rebind_theme_btn()
        self._build_project_name_widget()
        self._status(f"Switched to {'light' if self._theme_name == 'light' else 'dark'} mode")

    def _recolor_widget_tree(self, widget, color_map):
        """Recursively re-color a widget and all its descendants."""
        OPTS = (
            "background", "foreground",
            "highlightbackground", "highlightcolor",
            "insertbackground", "selectbackground", "selectforeground",
            "activebackground", "activeforeground",
            "troughcolor", "disabledforeground",
        )
        try:
            cfg = widget.configure()
            updates = {}
            for opt in OPTS:
                if opt in cfg:
                    try:
                        val = widget.cget(opt)
                        mapped = color_map.get(val.lower() if val else "")
                        if mapped:
                            updates[opt] = mapped
                    except Exception:
                        pass
            if updates:
                widget.configure(**updates)
        except Exception:
            pass
        for child in widget.winfo_children():
            self._recolor_widget_tree(child, color_map)

    def _refresh_rounded_buttons(self, widget):
        """Find all RoundedButton instances and redraw them with current globals."""
        if isinstance(widget, RoundedButton):
            widget._update_color_pair()
            widget._draw()
        for child in widget.winfo_children():
            self._refresh_rounded_buttons(child)

    # ── Title bar ────────────────────────────────────────────────────────────
    def _update_title(self):
        """Reflect the project name and unsaved state in the window title."""
        base = f"{self.t('app_title')}  -  {self.project_name}"
        if self.has_unsaved_changes:
            base += "  *"
        self.root.title(base)

    def _build_project_name_widget(self):
        """Build the clickable project-name label inside _pn_frame."""
        for w in self._pn_frame.winfo_children():
            w.destroy()

        # Outer pill — always visible, reads as a button at a glance
        pill = tk.Frame(
            self._pn_frame,
            bg=_BTN_SEC_BG,
            highlightbackground=_BORDER,
            highlightcolor=_BORDER,
            highlightthickness=1,
            cursor="hand2",
        )
        pill.grid(row=0, column=0, sticky="", padx=16, pady=7)

        # Name text + pencil icon always shown side-by-side
        self._pn_lbl = tk.Label(
            pill,
            text=f"✎  {self.project_name}",
            font=("Segoe UI", 12),
            bg=_BTN_SEC_BG, fg=_BTN_SEC_FG,
            cursor="hand2", anchor="center",
            padx=12, pady=5,
        )
        self._pn_lbl.pack()

        def _enter(_e):
            pill.config(bg=_BTN_SEC_HOV, highlightbackground=_ENTRY_FOCUS)
            self._pn_lbl.config(bg=_BTN_SEC_HOV, fg=_TEXT)

        def _leave(_e):
            pill.config(bg=_BTN_SEC_BG, highlightbackground=_BORDER)
            self._pn_lbl.config(bg=_BTN_SEC_BG, fg=_BTN_SEC_FG)

        for w in (pill, self._pn_lbl):
            w.bind("<Enter>", _enter)
            w.bind("<Leave>", _leave)

        # Defer start_rename_project by one event-loop tick so the click
        # event (and any Tooltip/bubble events on the same widget) fully
        # finish before we destroy and rebuild the header contents.
        self._pn_lbl.bind("<ButtonRelease-1>",
                          lambda _e: self.root.after(1, self.start_rename_project))

        Tooltip(self._pn_lbl, "Click to rename this project  (File > Rename Project)")

    def start_rename_project(self):
        """Replace the project-name label with an inline entry field."""
        for w in self._pn_frame.winfo_children():
            w.destroy()

        container = tk.Frame(self._pn_frame, bg=_HEADER_BG, bd=0, highlightthickness=0)
        container.grid(row=0, column=0, sticky="nsew")
        container.columnconfigure(0, weight=1)

        var = tk.StringVar(value=self.project_name)
        ent_frame = tk.Frame(container,
                             bg=_ENTRY_BG,
                             highlightbackground=_ENTRY_FOCUS,
                             highlightcolor=_ENTRY_FOCUS,
                             highlightthickness=2)
        ent_frame.pack(side="left", padx=6, pady=5)
        ent = tk.Entry(ent_frame, textvariable=var, relief="flat", bd=0,
                       font=("Segoe UI", 13),
                       bg=_ENTRY_BG, fg=_TEXT,
                       insertbackground=_TEXT,
                       selectbackground=_LB_SEL,
                       selectforeground=_LB_SEL_FG,
                       width=24)
        ent.pack(padx=8, pady=4)
        ent.select_range(0, "end")
        ent.focus_set()

        def _commit(_e=None):
            name = var.get().strip()
            if not name:
                name = "Untitled"
            self.project_name = name
            self.has_unsaved_changes = True
            self._sync_unsaved_dot()
            self._build_project_name_widget()
            self._status(f"Project renamed to: {name}")

        def _cancel(_e=None):
            self._build_project_name_widget()

        ent.bind("<Return>",  _commit)
        ent.bind("<Escape>",  _cancel)

        # OK / Cancel buttons
        btn_row = tk.Frame(container, bg=_HEADER_BG, bd=0, highlightthickness=0)
        btn_row.pack(side="left", padx=(0, 6))
        self._btn(btn_row, "OK",     _commit,  "primary",   48, 28, 10).pack(side="left", padx=2)
        self._btn(btn_row, "Cancel", _cancel,  "ghost",     60, 28, 10).pack(side="left", padx=2)

    def rename_project(self):
        """Menu-triggered project rename — delegates to the inline widget."""
        self.start_rename_project()

    # ── UI construction ──────────────────────────────────────────────────────
    def _build_ui(self):
        self.root.configure(bg=_BG)
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        # HEADER
        self.hdr = tk.Frame(self.root, bg=_HEADER_BG, bd=0, highlightthickness=0)
        self.hdr.grid(row=0, column=0, sticky="ew")
        self.hdr.columnconfigure(0, weight=0)   # logo
        self.hdr.columnconfigure(1, weight=0)   # menu bar
        self.hdr.columnconfigure(2, weight=1)   # project name (expands)
        self.hdr.columnconfigure(3, weight=0)   # right controls

        logo_frame = tk.Frame(self.hdr, bg=_HEADER_BG, bd=0, highlightthickness=0)
        logo_frame.grid(row=0, column=0, sticky="w", padx=(12, 20), ipady=10)
        self.lbl_logo = tk.Label(logo_frame, text=f"  {APP_NAME}",
                                  font=("Segoe UI", 15, "bold"), anchor="w",
                                  bg=_HEADER_BG, fg=_TEXT)
        self.lbl_logo.pack(side="left")
        self._lbl_unsaved = tk.Label(logo_frame, text=" ●",
                                      font=("Segoe UI", 13), anchor="w",
                                      bg=_HEADER_BG, fg=_TEXT_MUTED)
        self._lbl_unsaved.pack(side="left")
        self._lbl_unsaved.pack_forget()

        self.menu_frame = tk.Frame(self.hdr, bg=_HEADER_BG, bd=0, highlightthickness=0)
        self.menu_frame.grid(row=0, column=1, sticky="w")
        self._build_menu_bar(self.menu_frame)

        # ── Project name (center, inline-editable) ───────────────────────────
        self._pn_frame = tk.Frame(self.hdr, bg=_HEADER_BG, bd=0, highlightthickness=0)
        self._pn_frame.grid(row=0, column=2, sticky="nsew")
        self._pn_frame.columnconfigure(0, weight=1)
        self._pn_frame.rowconfigure(0, weight=1)
        self._build_project_name_widget()

        right_hdr = tk.Frame(self.hdr, bg=_HEADER_BG, bd=0, highlightthickness=0)
        right_hdr.grid(row=0, column=3, sticky="e", padx=(0, 20))
        self.lbl_as = tk.Label(right_hdr, text="", font=("Segoe UI", 13), anchor="e",
                                bg=_HEADER_BG, fg=_TEXT_MUTED)
        self.lbl_as.pack(side="left")

        self._theme_toggle_btn = tk.Label(
            right_hdr, text="☀  Light Mode",
            font=("Segoe UI", 12), cursor="hand2",
            padx=10, pady=4,
            bg=_HEADER_BG, fg=_TEXT_MUTED)
        self._theme_toggle_btn.pack(side="left", padx=(8, 0))
        self._theme_toggle_btn.bind("<Button-1>", lambda _e: self.toggle_theme())
        self._theme_toggle_btn.bind("<Enter>",
            lambda _e: self._theme_toggle_btn.config(fg=_ACCENT))
        self._theme_toggle_btn.bind("<Leave>",
            lambda _e: self._theme_toggle_btn.config(fg=_TEXT_MUTED))

        self._is_fullscreen = False
        self._fs_btn = tk.Label(
            right_hdr, text="⛶  Fullscreen",
            font=("Segoe UI", 12), cursor="hand2",
            padx=10, pady=4,
            bg=_HEADER_BG, fg=_TEXT_MUTED)
        self._fs_btn.pack(side="left", padx=(8, 0))
        self._fs_btn.bind("<Button-1>", lambda _e: self.toggle_fullscreen())
        self._fs_btn.bind("<Enter>",  lambda _e: self._fs_btn.config(fg=_ACCENT))
        self._fs_btn.bind("<Leave>",  lambda _e: self._fs_btn.config(fg=_TEXT_MUTED))
        self.root.bind("<F11>",    lambda _e: self.toggle_fullscreen())
        self.root.bind("<Escape>", lambda _e: self._on_escape())
        # Store ref so toggle_theme can update hover bindings after theme swap
        def _rebind_theme_btn():
            self._theme_toggle_btn.bind("<Enter>",
                lambda _e: self._theme_toggle_btn.config(fg=_ACCENT))
            self._theme_toggle_btn.bind("<Leave>",
                lambda _e: self._theme_toggle_btn.config(fg=_TEXT_MUTED))
        self._rebind_theme_btn = _rebind_theme_btn

        tk.Frame(self.hdr, height=1, bg=_SEP, bd=0).grid(row=1, column=0, columnspan=4, sticky="ew")

        # MAIN AREA
        main = tk.Frame(self.root, bg=_BG, bd=0, highlightthickness=0)
        main.grid(row=1, column=0, sticky="nsew")
        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=0)
        main.columnconfigure(1, weight=0)
        main.columnconfigure(2, weight=1)

        # LEFT SIDEBAR (steps list)
        self.sb = tk.Frame(main, width=270, bg=_PANEL_BG, bd=0, highlightthickness=0)
        self.sb.grid(row=0, column=0, sticky="nsew")
        self.sb.grid_propagate(False)
        self.sb.rowconfigure(1, weight=1)
        self.sb.columnconfigure(0, weight=1)

        tk.Frame(main, width=1, bg=_BORDER, bd=0).grid(row=0, column=0, sticky="nse")

        # Sidebar header with step count badge
        sb_top = tk.Frame(self.sb, bg=_PANEL_BG, bd=0, highlightthickness=0)
        sb_top.grid(row=0, column=0, sticky="ew", padx=14, pady=(10, 2))
        self.lbl_steps_hdr = tk.Label(sb_top, text=self.t("steps").upper(),
                                       font=("Segoe UI", 13, "bold"),
                                       bg=_PANEL_BG, fg=_TEXT_MUTED)
        self.lbl_steps_hdr.pack(side="left")
        self.lbl_step_count = tk.Label(sb_top, text="",
                                        font=("Segoe UI", 12),
                                        bg=_PANEL_BG, fg=_TEXT_LIGHT)
        self.lbl_step_count.pack(side="left", padx=(6, 0))

        self.steps_lb = ThemedListbox(self.sb)
        self.steps_lb.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 8))

        # Empty-state overlay (shown when no steps exist)
        self._empty_lbl = tk.Label(self.sb,
            text="No steps yet.\nAdd one from the centre panel.",
            font=("Segoe UI", 12, "italic"),
            bg=_PANEL_BG, fg=_TEXT_LIGHT,
            justify="center", wraplength=220)
        self._empty_lbl.place(relx=0.5, rely=0.42, anchor="center")

        self._setup_dnd()

        # Sidebar buttons
        btn_grid = tk.Frame(self.sb, bg=_PANEL_BG, bd=0, highlightthickness=0)
        btn_grid.grid(row=2, column=0, sticky="ew", padx=9, pady=(0, 10))
        btn_grid.columnconfigure(0, weight=1)
        btn_grid.columnconfigure(1, weight=1)

        def mk_btn(text, cmd, style, row, col, colspan=1):
            b = RoundedButton(btn_grid, text, command=cmd, style=style, height=38, font_size=12)
            b.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)
            b.configure(bg=_PANEL_BG)
            b.apply_theme(None)
            return b

        self._btn_move_up   = mk_btn("▲  " + self.t("move_up"),    self.move_up,       "secondary", 0, 0)
        self._btn_move_down = mk_btn("▼  " + self.t("move_down"),  self.move_down,     "secondary", 0, 1)
        self._btn_edit      = mk_btn("✎  " + self.t("edit"),       self.edit_step,     "secondary", 1, 0)
        self._btn_remove    = mk_btn("✕  " + self.t("remove"),     self.remove_step,   "danger",    1, 1)
        self._btn_cgrp      = mk_btn("⊞  " + self.t("create_group"),self.create_group, "secondary", 2, 0)
        self._btn_ungroup   = mk_btn("⊟  " + self.t("ungroup"),    self.ungroup,       "secondary", 2, 1)
        self._btn_rename    = mk_btn("↔  " + self.t("rename_group"),self.rename_group, "secondary", 3, 0)
        self._btn_duplicate = mk_btn("⧉  " + self.t("duplicate"),  self.duplicate_step,"secondary", 3, 1)

        Tooltip(self._btn_move_up,   "Move selected step up  (Ctrl+↑)")
        Tooltip(self._btn_move_down, "Move selected step down  (Ctrl+↓)")
        Tooltip(self._btn_edit,      "Edit selected step")
        Tooltip(self._btn_remove,    "Remove selected step  (Del)")
        Tooltip(self._btn_cgrp,      "Group selected steps together")
        Tooltip(self._btn_ungroup,   "Ungroup selected group")
        Tooltip(self._btn_rename,    "Rename selected group")
        Tooltip(self._btn_duplicate, "Duplicate selected step  (Ctrl+D)")

        # CENTER PANEL (action picker)
        self.cp = tk.Frame(main, width=320, bg=_PANEL_BG, bd=0, highlightthickness=0)
        self.cp.grid(row=0, column=1, sticky="nsew")
        self.cp.grid_propagate(False)
        self.cp.rowconfigure(2, weight=1)
        self.cp.columnconfigure(0, weight=1)

        tk.Frame(main, width=1, bg=_BORDER, bd=0).grid(row=0, column=1, sticky="nse")

        self.lbl_add_step = tk.Label(self.cp, text=self.t("add_step_section").upper(),
                                      font=("Segoe UI", 13, "bold"),
                                      bg=_PANEL_BG, fg=_TEXT_MUTED)
        self.lbl_add_step.grid(row=0, column=0, sticky="w", padx=14, pady=(10, 2))

        self.search_var = tk.StringVar()
        self.search_ent = StyledEntry(self.cp, textvariable=self.search_var,
                                       placeholder=self.t("search"))
        self.search_ent.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 6))

        self.action_lb = ThemedListbox(self.cp, show_scrollbar=False)
        self.action_lb.grid(row=2, column=0, sticky="nsew", padx=14, pady=(0, 2))
        self.action_lb.lb.configure(height=14)
        self._action_keys = _ALL_ACTION_KEYS[:]
        self._fill_action_lb(self._action_keys)
        self.action_lb.lb.selection_set(0)
        self.action_lb.bind("<<ListboxSelect>>", self._on_action_sel)
        self.action_lb.lb.bind("<Return>", lambda _e: self.add_step())

        # Hover highlight for action listbox
        _ALB = self.action_lb.lb
        self._alb_hover_bg  = _ALB_HOVER_BG
        self._alb_norm_bg   = _LB_BG
        self._alb_alt_bg_h  = _ALB_ALT_ROW_BG
        self._action_hover_idx = None

        def _alb_enter(e):
            idx = _ALB.nearest(e.y)
            if idx == self._action_hover_idx:
                return
            if self._action_hover_idx is not None:
                old_idx = self._action_hover_idx
                _ALB.itemconfigure(old_idx, background=self._alb_alt_bg_h if old_idx % 2 == 1 else self._alb_norm_bg)
            self._action_hover_idx = idx
            sel = _ALB.curselection()
            if idx not in sel:
                _ALB.itemconfigure(idx, background=self._alb_hover_bg)

        def _alb_leave(e):
            if self._action_hover_idx is not None:
                old_idx = self._action_hover_idx
                sel = _ALB.curselection()
                if old_idx not in sel:
                    _ALB.itemconfigure(old_idx, background=self._alb_alt_bg_h if old_idx % 2 == 1 else self._alb_norm_bg)
                self._action_hover_idx = None

        _ALB.bind("<Motion>", _alb_enter)
        _ALB.bind("<Leave>",  _alb_leave)

        # Action description box
        tip_box = tk.Frame(self.cp, bg=_ENTRY_BG,
                           highlightbackground=_ENTRY_BORDER,
                           highlightcolor=_ENTRY_BORDER,
                           highlightthickness=1)
        tip_box.grid(row=3, column=0, sticky="ew", padx=14, pady=(4, 0))
        tip_box.columnconfigure(0, weight=1)
        self.lbl_action_tip = tk.Label(tip_box, text="",
                                        font=("Segoe UI", 11, "italic"),
                                        bg=_ENTRY_BG, fg=_TEXT_MUTED,
                                        wraplength=280, anchor="w", justify="left",
                                        padx=10, pady=8)
        self.lbl_action_tip.grid(row=0, column=0, sticky="ew")

        # Fixed-height container so changing fields never reflowing the panel
        self._f_container = tk.Frame(self.cp, bg=_PANEL_BG, bd=0,
                                     highlightthickness=0, height=215)
        self._f_container.grid(row=4, column=0, sticky="ew")
        self._f_container.grid_propagate(False)
        self._f_container.columnconfigure(0, weight=1)

        self.f_frame = tk.Frame(self._f_container, bg=_PANEL_BG, bd=0, highlightthickness=0)
        self.f_frame.place(x=14, y=4, relwidth=1, width=-28)

        self.field_vars = {}
        self._field_wgts = []
        self._cur_en_action = "Create folder"
        self.build_fields("Create folder")

        self.btn_add = RoundedButton(self.cp, f"+ {self.t('add_step')}", command=self.add_step,
                                      style="primary", height=46, font_size=14)
        self.btn_add.grid(row=5, column=0, sticky="ew", padx=14, pady=(12, 2))
        self.btn_add.configure(bg=_PANEL_BG)
        self.btn_add.apply_theme(None)

        # Keyboard hint strip
        self._hint_bar = tk.Label(self.cp,
            text="Enter  add     Ctrl+D  duplicate     F2  edit     Ctrl+E  export",
            font=("Segoe UI", 10), bg=_PANEL_BG, fg=_TEXT_LIGHT,
            anchor="center", pady=4)
        self._hint_bar.grid(row=6, column=0, sticky="ew", padx=14, pady=(0, 8))

        def _resize_add(e):
            new_w = max(e.width - 28, 60)
            self.btn_add.configure(width=new_w)
            self.btn_add.w = new_w
            self.btn_add._draw()
        self.cp.bind("<Configure>", _resize_add)

        # RIGHT PANEL (code preview + export)
        self.rp = tk.Frame(main, bg=_BG, bd=0, highlightthickness=0)
        self.rp.grid(row=0, column=2, sticky="nsew")
        self.rp.rowconfigure(1, weight=1)
        self.rp.columnconfigure(0, weight=1)

        # Code panel header row: label left, copy button right
        rp_hdr = tk.Frame(self.rp, bg=_BG, bd=0, highlightthickness=0)
        rp_hdr.grid(row=0, column=0, sticky="ew", padx=18, pady=(10, 4))
        rp_hdr.columnconfigure(0, weight=1)

        self.lbl_gen_code = tk.Label(rp_hdr, text=self.t("generated_code").upper(),
                                      font=("Segoe UI", 13, "bold"),
                                      bg=_BG, fg=_TEXT_MUTED)
        self.lbl_gen_code.grid(row=0, column=0, sticky="w")

        def _copy_code():
            self.root.clipboard_clear()
            self.root.clipboard_append(self.preview.get("1.0", "end-1c"))
            self._status("Code copied to clipboard")

        self._btn_copy = RoundedButton(rp_hdr, "⎘  Copy", command=_copy_code,
                                        style="ghost", width=84, height=28, font_size=11)
        self._btn_copy.grid(row=0, column=1, sticky="e")
        self._btn_copy.configure(bg=_BG)
        self._btn_copy.apply_theme(None)
        Tooltip(self._btn_copy, "Copy generated code to clipboard")

        # Header comment block toggle
        self._header_enabled = True
        self._hdr_toggle_lbl = tk.Label(
            rp_hdr, text="⊞  Header",
            font=("Segoe UI", 11), cursor="hand2",
            padx=8, pady=2,
            bg=_BG, fg=_ACCENT)
        self._hdr_toggle_lbl.grid(row=0, column=2, sticky="e", padx=(6, 0))
        Tooltip(self._hdr_toggle_lbl, "Toggle header comment block in exported file")

        def _toggle_header():
            self._header_enabled = not self._header_enabled
            self._hdr_toggle_lbl.config(
                fg=_ACCENT if self._header_enabled else _TEXT_MUTED,
                text="⊞  Header" if self._header_enabled else "⊟  Header")
            self.invalidate_cache()
            self._status("Header comment " + ("on" if self._header_enabled else "off"))

        self._hdr_toggle_lbl.bind("<Button-1>", lambda _e: _toggle_header())
        self._hdr_toggle_lbl.bind("<Enter>", lambda _e: self._hdr_toggle_lbl.config(fg=_ACCENT_HOVER))
        self._hdr_toggle_lbl.bind("<Leave>", lambda _e: self._hdr_toggle_lbl.config(
            fg=_ACCENT if self._header_enabled else _TEXT_MUTED))

        self.code_frame = tk.Frame(self.rp, bg=_CODE_BG, bd=0, highlightthickness=1,
                                    highlightbackground=_BORDER, highlightcolor=_BORDER)
        self.code_frame.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 4))
        self.code_frame.rowconfigure(0, weight=1)
        self.code_frame.columnconfigure(2, weight=1)

        # Subtle separator between line numbers and code
        tk.Frame(self.code_frame, width=1, bg=_BORDER).grid(row=0, column=1, sticky="ns")

        self.preview = tk.Text(self.code_frame, wrap="none", state="disabled",
                                relief="flat", bd=0, padx=6, pady=12,
                                font=("Consolas", 13),
                                bg=_CODE_BG, fg=_CODE_FG,
                                selectbackground=_LB_SEL)
        psy = tk.Scrollbar(self.code_frame, orient="vertical",
                            command=self.preview.yview, relief="flat", bd=0, width=8,
                            bg=_SCROLLBAR, troughcolor=_CODE_BG, activebackground=_ACCENT)
        psx = tk.Scrollbar(self.code_frame, orient="horizontal",
                            command=self.preview.xview, relief="flat", bd=0, width=8,
                            bg=_SCROLLBAR, troughcolor=_CODE_BG)
        self.preview.configure(yscrollcommand=psy.set, xscrollcommand=psx.set)
        psy.grid(row=0, column=3, sticky="ns")
        psx.grid(row=1, column=1, columnspan=2, sticky="ew")
        self.preview.grid(row=0, column=2, sticky="nsew")

        # Line numbers – must be created after preview so it can reference it
        self._ln = CodeLineNumbers(self.code_frame, self.preview)
        self._ln.grid(row=0, column=0, sticky="ns", padx=(2, 0), pady=(0, 0))

        def _on_scroll(*args):
            psy.set(*args)
            self._ln.redraw()
        self.preview.configure(yscrollcommand=_on_scroll)
        self.preview.bind("<Configure>", lambda e: self._ln.redraw())

        self.btn_export = RoundedButton(self.rp, self.t("save_bat"), command=self.save_bat,
                                         style="primary", height=48, font_size=14)
        self.btn_export.grid(row=2, column=0, sticky="ew", padx=18, pady=12)
        self.btn_export.configure(bg=_BG)
        self.btn_export.apply_theme(None)

        def _resize_export(e):
            new_w = max(e.width - 36, 60)
            self.btn_export.configure(width=new_w)
            self.btn_export.w = new_w
            self.btn_export._draw()
        self.rp.bind("<Configure>", _resize_export)

        # STATUS BAR
        tk.Frame(self.root, height=1, bg=_SEP, bd=0).grid(row=1, column=0, sticky="sew")
        self.stbar = tk.Frame(self.root, bg=_STATUS_BG, bd=0, highlightthickness=0)
        self.stbar.grid(row=2, column=0, sticky="ew")
        self.lbl_st = tk.Label(self.stbar, text=f"  {APP_NAME} ready",
                                font=("Segoe UI", 13), anchor="w",
                                bg=_STATUS_BG, fg=_TEXT_MUTED)
        self.lbl_st.pack(side="left", padx=10, pady=5)
        self.lbl_st_count = tk.Label(self.stbar, text="",
                                      font=("Segoe UI", 11), anchor="e",
                                      bg=_STATUS_BG, fg=_TEXT_LIGHT)
        self.lbl_st_count.pack(side="right", padx=14, pady=5)

        # Attach search trace now that all widgets exist
        self.search_var.trace_add("write", self.on_search_change)
        # Escape on the search entry clears it and restores the full action list
        self.search_ent._e.bind("<Escape>", self._clear_search)

        # Show initial tooltip
        self._update_action_tip()

    def _build_menu_bar(self, parent):
        menus = [
            (self.t("file"), [
                (self.t("new_project"),    self.new_project),
                (self.t("open_project"),   self.open_project),
                None,
                (self.t("save_project"),   self.save_project),
                (self.t("save_project_as"),self.save_project_as),
                None,
                (self.t("rename_project"), self.rename_project),
                None,
                (self.t("import_bat"),     self.import_bat),
                None,
                (self.t("exit"),           self.on_closing),
            ]),
            (self.t("edit_menu"), [
                (self.t("undo") + "  Ctrl+Z",   self.undo),
                (self.t("redo") + "  Ctrl+Y",   self.redo),
                None,
                (self.t("duplicate") + "  Ctrl+D", self.duplicate_step),
                None,
                ("Clear All Steps", self.clear_all_steps),
            ]),
            (self.t("templates"), [
                (self.t("save_as_template"), self.save_as_template),
                (self.t("load_template"),    self.load_template),
                (self.t("manage_templates"), self.manage_templates),
            ]),
            (self.t("extras"), [
                (self.t("about"),              self.show_about),
                (self.t("terms"),              self.show_terms),
                None,
                (self.t("open_config_folder"), self.open_config_folder),
                None,
                (self.t("twitter"),            self.open_twitter),
                (self.t("check_updates"),      self.check_for_updates),
                (self.t("support_project"),    self.open_support),
                (self.t("give_feedback"),      self.open_feedback),
            ]),
            (self.t("help"), [
                (self.t("instruction_manual"), self.show_help),
                (self.t("debug"),              self.show_debug),
            ]),
            (self.t("language"), [
                (self.t("english"), lambda: self.change_language("en")),
                (self.t("french"),  lambda: self.change_language("fr")),
            ]),
        ]

        for label, items in menus:
            b = tk.Label(parent, text=label, font=("Segoe UI", 13), cursor="hand2",
                          padx=12, pady=4, bg=_HEADER_BG, fg=_TEXT)
            b.pack(side="left", fill="y")

            def bind_popup(btn, its):
                def show(_e=None):
                    drop = tk.Toplevel(self.root)
                    drop.overrideredirect(True)
                    drop.configure(bg=_BORDER)
                    drop.attributes("-topmost", True)
                    inner = tk.Frame(drop, bg=_PANEL_BG, bd=0, highlightthickness=0)
                    inner.pack(padx=1, pady=1, fill="both", expand=True)

                    def close_drop(cmd=None):
                        drop.destroy()
                        if cmd: self.root.after(1, cmd)

                    drop.bind("<FocusOut>", lambda e: close_drop())

                    for it in its:
                        if it is None:
                            tk.Frame(inner, height=1, bg=_SEP).pack(fill="x", padx=0, pady=2)
                        else:
                            lbl_text, cmd = it
                            row = tk.Label(inner, text=lbl_text,
                                           font=("Segoe UI", 12),
                                           bg=_PANEL_BG, fg=_TEXT,
                                           anchor="w", padx=14, pady=6,
                                           cursor="hand2")
                            row.pack(fill="x")
                            row.bind("<Enter>",           lambda e, r=row: r.config(bg=_LB_SEL, fg=_TEXT))
                            row.bind("<Leave>",           lambda e, r=row: r.config(bg=_PANEL_BG, fg=_TEXT))
                            row.bind("<ButtonRelease-1>", lambda e, c=cmd: close_drop(c))

                    drop.update_idletasks()
                    x = btn.winfo_rootx()
                    y = btn.winfo_rooty() + btn.winfo_height()
                    drop.geometry(f"+{x}+{y}")
                    drop.focus_set()

                btn.bind("<Button-1>", show)
                btn.bind("<Enter>", lambda e, b=btn: b.config(fg=_ACCENT))
                btn.bind("<Leave>", lambda e, b=btn: b.config(fg=_TEXT))

            bind_popup(b, items)

    # ── Drag-and-drop reordering ─────────────────────────────────────────────
    def _setup_dnd(self):
        lb = self.steps_lb.lb

        def _dnd_press(e):
            self._drag_idx = lb.nearest(e.y)

        def _dnd_motion(e):
            if self._drag_idx is None:
                return
            target = lb.nearest(e.y)
            lb.configure(cursor="fleur")
            if target != self._drag_idx:
                lb.selection_clear(0, "end")
                lb.selection_set(target)

        def _dnd_release(e):
            lb.configure(cursor="")
            if self._drag_idx is None:
                return
            target = lb.nearest(e.y)
            if target != self._drag_idx:
                self._move_item_dnd(self._drag_idx, target)
            else:
                lb.selection_clear(0, "end")
                lb.selection_set(self._drag_idx)
            self._drag_idx = None

        lb.bind("<ButtonPress-1>",   _dnd_press)
        lb.bind("<B1-Motion>",       _dnd_motion)
        lb.bind("<ButtonRelease-1>", _dnd_release)
        lb.bind("<Double-Button-1>", lambda e: self.edit_step())
        lb.bind("<Button-3>",        self._show_step_context_menu)

    def _show_step_context_menu(self, event):
        """Right-click context menu for the steps list."""
        lb = self.steps_lb.lb
        idx = lb.nearest(event.y)
        if idx < 0 or idx >= lb.size():
            return
        lb.selection_clear(0, "end")
        lb.selection_set(idx)

        m = self._mapping()
        if idx >= len(m):
            return
        _, is_grp = m[idx]

        menu = tk.Menu(self.root, tearoff=0,
                       bg=_PANEL_BG, fg=_TEXT,
                       activebackground=_LB_SEL,
                       activeforeground=_LB_SEL_FG,
                       relief="flat", bd=1,
                       font=("Segoe UI", 12))
        menu.add_command(label="Edit            F2",      command=self.edit_step)
        menu.add_command(label="Duplicate   Ctrl+D", command=self.duplicate_step)
        menu.add_separator()
        menu.add_command(label="Move Up     Ctrl+\u2191", command=self.move_up)
        menu.add_command(label="Move Down  Ctrl+\u2193", command=self.move_down)
        menu.add_separator()
        menu.add_command(label="Remove       Del",        command=self.remove_step)
        if is_grp:
            menu.add_separator()
            menu.add_command(label="Ungroup",      command=self.ungroup)
            menu.add_command(label="Rename Group", command=self.rename_group)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def _move_item_dnd(self, from_flat, to_flat):
        m = self._mapping()
        if from_flat >= len(m) or to_flat >= len(m):
            return
        self._push_undo()
        from_path, _ = m[from_flat]
        to_path,   _ = m[to_flat]
        from_par, from_idx = self._by_path(from_path)
        to_par,   to_idx   = self._by_path(to_path)
        item = from_par.pop(from_idx)
        if from_par is to_par and to_idx > from_idx:
            to_idx -= 1
        to_par.insert(to_idx, item)
        self.has_unsaved_changes = True
        self.rebuild_steps()
        self.invalidate_cache()
        # Re-select the moved item
        new_m = self._mapping()
        for i, (path, _) in enumerate(new_m):
            p2, idx2 = self._by_path(path)
            if p2 is to_par and idx2 == to_idx:
                self.steps_lb.lb.selection_set(i)
                break

    # ── Undo / Redo ──────────────────────────────────────────────────────────
    def _push_undo(self):
        state = (copy.deepcopy(self.items), self.next_action_id)
        self._undo_stack.append(state)
        if len(self._undo_stack) > 60:
            self._undo_stack.pop(0)
        self._redo_stack.clear()

    def undo(self):
        if not self._undo_stack:
            self._status("Nothing to undo")
            return
        self._redo_stack.append((copy.deepcopy(self.items), self.next_action_id))
        self.items, self.next_action_id = self._undo_stack.pop()
        self.has_unsaved_changes = True
        self.rebuild_steps()
        self.invalidate_cache()
        self._status(self.t("undo"))

    def redo(self):
        if not self._redo_stack:
            self._status("Nothing to redo")
            return
        self._undo_stack.append((copy.deepcopy(self.items), self.next_action_id))
        self.items, self.next_action_id = self._redo_stack.pop()
        self.has_unsaved_changes = True
        self.rebuild_steps()
        self.invalidate_cache()
        self._status(self.t("redo"))

    # ── Action list helpers ──────────────────────────────────────────────────
    def _fill_action_lb(self, keys):
        self.action_lb.delete(0, "end")
        self._action_keys = keys
        if hasattr(self, "_action_hover_idx"):
            self._action_hover_idx = None
        lb = self.action_lb.lb
        ta = self.ta
        for i, k in enumerate(keys):
            icon = _ACTION_ICONS.get(k, " ")
            lb.insert("end", f"  {icon}  {ta(k)}")
            if i % 2 == 1:
                lb.itemconfigure(i, background=_ALT_ROW_BG)

    def _on_action_sel(self, _e=None):
        sel = self.action_lb.curselection()
        if not sel:
            return
        self._cur_en_action = self._action_keys[sel[0]]
        self.build_fields(self._cur_en_action)
        self._update_action_tip()

    def _update_action_tip(self):
        tips = ACTION_TOOLTIPS.get(self.current_lang, ACTION_TOOLTIPS["en"])
        tip  = tips.get(self._cur_en_action, "")
        self.lbl_action_tip.config(text=tip)

    def on_search_change(self, *_args):
        q = self.search_var.get().strip().lower()
        if not q or q == self.search_ent._ph.lower():
            self._fill_action_lb(_ALL_ACTION_KEYS)
            self.action_lb.lb.selection_set(0)
            return
        ta = self.ta
        filtered = [k for k in ACTION_DEFS if k != "Set environment variable"
                    and (q in ta(k).lower() or q in k.lower())]
        if not filtered:
            filtered = _ALL_ACTION_KEYS
        self._fill_action_lb(filtered)
        self.action_lb.lb.selection_set(0)
        self._on_action_sel()

    def _clear_search(self, _e=None):
        """Clear the search bar and restore the full action list."""
        self.search_var.set("")
        self.search_ent.set("")
        self._fill_action_lb(_ALL_ACTION_KEYS)
        self.action_lb.lb.selection_set(0)
        self._on_action_sel()

    def build_fields(self, en_action):
        for w in self.f_frame.winfo_children():
            w.destroy()
        self.field_vars  = {}
        self._field_wgts = []

        fields = ACTION_DEFS[en_action]["fields"]
        if not fields:
            lbl = tk.Label(self.f_frame, text=self.t("no_options"),
                            font=("Segoe UI", 13, "italic"), bg=_PANEL_BG, fg=_TEXT_MUTED)
            lbl.pack(anchor="w", pady=10, padx=4)
            self._field_wgts.append(lbl)
            return

        tf = self.tf
        for field_def in fields:
            fk  = field_def[0]
            vk  = field_def[1]
            ftype = field_def[2] if len(field_def) > 2 else "entry"
            lbl = tk.Label(self.f_frame, text=tf(fk),
                            font=("Segoe UI", 13), bg=_PANEL_BG, fg=_TEXT_MUTED, anchor="w")
            lbl.pack(anchor="w", pady=(8, 2), padx=4)
            if ftype == "textarea":
                ta_widget = StyledTextArea(self.f_frame, height=4)
                ta_widget.pack(fill="x", padx=4, pady=(0, 4))
                self.field_vars[vk] = ta_widget.var
                self._field_wgts += [lbl, ta_widget]
            else:
                var = tk.StringVar()
                ent = StyledEntry(self.f_frame, textvariable=var)
                ent.pack(fill="x", padx=4, pady=(0, 4))
                ent._e.bind("<Return>", lambda _e: self.add_step())
                self.field_vars[vk] = var
                self._field_wgts += [lbl, ent]

    # ── Step management ──────────────────────────────────────────────────────
    # Required fields per action that must be non-empty before adding
    _REQUIRED_FIELDS = {
        "Create folder":           ["folder_name"],
        "Delete file":             ["path"],
        "Delete folder":           ["folder"],
        "Move / Rename":           ["src", "dst"],
        "Copy files":              ["src", "dst"],
        "Launch program":          ["prog_path"],
        "Open folder":             ["folder"],
        "Open multiple websites":  ["urls"],
        "Run CMD command":         ["cmd"],
        "Run PowerShell command":  ["ps_cmd"],
        "Kill process":            ["pname"],
        "Set variable (session)":  ["var"],
        "Set persistent variable": ["var"],
        "If file exists":          ["path"],
        "If folder exists":        ["folder"],
        "Loop files in folder":    ["folder"],
        "Change directory":        ["folder"],
        "Define label":            ["label"],
        "Goto label":              ["label"],
        "Find in file":            ["path"],
        "Type file":               ["path"],
        "Ping host":               ["text"],
    }

    def add_step(self):
        ea   = self._cur_en_action
        vals = {k: v.get() for k, v in self.field_vars.items()}
        # Validate required fields
        required = self._REQUIRED_FIELDS.get(ea, [])
        missing  = [self.tf(f) for f in required if not vals.get(f, "").strip()]
        if missing:
            messagebox.showwarning(
                "Missing field",
                f"Please fill in: {', '.join(missing)}"
            )
            return
        self._push_undo()
        ea   = self._cur_en_action
        vals = {k: v.get() for k, v in self.field_vars.items()}
        self.items.append(("action", ea, vals, self.next_action_id))
        self.next_action_id += 1
        self.has_unsaved_changes = True
        self.rebuild_steps()
        self.invalidate_cache()
        # Auto-select the new step so the user sees it highlighted
        new_idx = self.steps_lb.lb.size() - 1
        if new_idx >= 0:
            self.steps_lb.lb.selection_clear(0, "end")
            self.steps_lb.lb.selection_set(new_idx)
            self.steps_lb.lb.see(new_idx)
        self._status(f"Added: {self.ta(ea)}")

    def duplicate_step(self):
        sel = self.steps_lb.curselection()
        if not sel:
            return
        self._push_undo()
        path, is_grp = self._mapping()[sel[0]]
        par, idx = self._by_path(path)
        item = copy.deepcopy(par[idx])
        if item[0] == "action":
            item = ("action", item[1], dict(item[2]), self.next_action_id)
            self.next_action_id += 1
        par.insert(idx + 1, item)
        self.has_unsaved_changes = True
        self.rebuild_steps()
        self.invalidate_cache()
        self.steps_lb.lb.selection_clear(0, "end")
        self.steps_lb.lb.selection_set(sel[0] + 1)
        label = self.ta(item[1]) if item[0] == "action" else item[1]
        self._status(f"Duplicated: {label}")

    def rebuild_steps(self):
        lb = self.steps_lb.lb
        lb.delete(0, "end")
        labels = []
        self._collect_labels(self.items, 0, labels)
        for i, (lbl, is_grp) in enumerate(labels):
            lb.insert("end", lbl)
            if not is_grp and i % 2 == 1:
                lb.itemconfigure(i, background=_ALT_ROW_BG)
        # Update step count badge
        total = sum(1 for _ in self._flatten(self.items))
        self.lbl_step_count.config(text=f"({total})" if total else "")
        # Toggle empty-state overlay
        if total == 0:
            self._empty_lbl.lift()
            self._empty_lbl.place(relx=0.5, rely=0.42, anchor="center")
        else:
            self._empty_lbl.place_forget()
        # Update status-bar step count
        if total:
            self.lbl_st_count.config(text=f"{total} step{'s' if total != 1 else ''}")
        else:
            self.lbl_st_count.config(text="")
        # Update unsaved dot
        self._sync_unsaved_dot()

    def _collect_labels(self, items, depth, out):
        pad = "  " * depth
        ta  = self.ta
        for it in items:
            if it[0] == "action":
                icon    = _ACTION_ICONS.get(it[1], " ")
                summary = self._step_summary(it[1], it[2])
                label   = f"{pad}  {icon}  {ta(it[1])}"
                if summary:
                    label = f"{label}:  {summary}"
                out.append((label, False))
            else:
                out.append((f"{pad}▸  {it[1]}", True))
                self._collect_labels(it[2], depth + 1, out)

    # Key fields to extract for each action's one-line summary shown in the step list
    _SUMMARY_FIELD = {
        "Create folder":           "folder_name",
        "Delete file":             "path",
        "Delete folder":           "folder",
        "Move / Rename":           "src",
        "Copy files":              "src",
        "Launch program":          "prog_path",
        "Open folder":             "folder",
        "Open multiple websites":  "urls",
        "Print text":              "text",
        "Add comment":             "text",
        "Set window title":        "text",
        "Wait (seconds)":          "seconds",
        "Create text file":        "path",
        "Append text to file":     "path",
        "Run CMD command":         "cmd",
        "Run PowerShell command":  "ps_cmd",
        "Kill process":            "pname",
        "Set variable (session)":  "var",
        "Set persistent variable": "var",
        "If file exists":          "path",
        "If folder exists":        "folder",
        "Loop files in folder":    "folder",
        "Change directory":        "folder",
        "Define label":            "label",
        "Goto label":              "label",
        "Exit script":             "value",
        "Check errorlevel":        "var",
        "Log to file":             "text",
        "Find in file":            "text",
        "Type file":               "path",
        "Ping host":               "text",
    }

    def _step_summary(self, action, vals):
        """Return a short display string for the most important field of a step."""
        field = self._SUMMARY_FIELD.get(action)
        if not field:
            return ""
        raw = vals.get(field, "").strip()
        if not raw:
            return ""
        # Truncate long values so the listbox stays readable
        if len(raw) > 38:
            raw = raw[:36] + "…"
        # For URLs (one per line) show only the first one
        first_line = raw.splitlines()[0]
        return first_line

    # ── Mapping (flat index → path) ──────────────────────────────────────────
    def _mapping(self):
        result = []
        def walk(items, path):
            for i, it in enumerate(items):
                cp = path + [i]
                result.append((cp, it[0] == "group"))
                if it[0] == "group":
                    walk(it[2], cp + ["items"])
        walk(self.items, [])
        return result

    def _by_path(self, path):
        cur = self.items
        for p in path[:-1]:
            if p == "items":
                continue
            cur = cur[p]
            if cur[0] == "group":
                cur = cur[2]
        return cur, path[-1]

    def move_up(self):
        sel = self.steps_lb.curselection()
        if not sel or sel[0] == 0:
            return
        self._push_undo()
        m = self._mapping()
        path, _ = m[sel[0]]
        par, idx = self._by_path(path)
        if idx > 0:
            par[idx - 1], par[idx] = par[idx], par[idx - 1]
            self.has_unsaved_changes = True
            self.rebuild_steps()
            self.steps_lb.selection_set(sel[0] - 1)
            self.invalidate_cache()

    def move_down(self):
        sel = self.steps_lb.curselection()
        if not sel:
            return
        m = self._mapping()
        if sel[0] >= len(m) - 1:
            return
        self._push_undo()
        path, _ = m[sel[0]]
        par, idx = self._by_path(path)
        if idx < len(par) - 1:
            par[idx + 1], par[idx] = par[idx], par[idx + 1]
            self.has_unsaved_changes = True
            self.rebuild_steps()
            self.steps_lb.selection_set(sel[0] + 1)
            self.invalidate_cache()

    def remove_step(self):
        sel = self.steps_lb.curselection()
        if not sel:
            return
        self._push_undo()
        path, _ = self._mapping()[sel[0]]
        par, idx = self._by_path(path)
        del par[idx]
        self.has_unsaved_changes = True
        self.rebuild_steps()
        self.invalidate_cache()
        # Re-select nearest remaining item
        remaining = self.steps_lb.lb.size()
        if remaining > 0:
            new_idx = min(sel[0], remaining - 1)
            self.steps_lb.lb.selection_set(new_idx)
            self.steps_lb.lb.see(new_idx)

    def edit_step(self):
        sel = self.steps_lb.curselection()
        if not sel:
            return
        path, is_grp = self._mapping()[sel[0]]
        par, idx = self._by_path(path)
        it = par[idx]
        if is_grp:
            self.edit_group(par, idx, it)
        else:
            self.edit_action(par, idx, it)

    def edit_action(self, par, idx, it):
        fields = ACTION_DEFS[it[1]]["fields"]
        dlg_h  = max(300, 180 + len(fields) * 85)
        dlg = self._dialog(self.t("edit_step"), 440, dlg_h)
        dlg.configure(bg=_PANEL_BG)
        tk.Label(dlg, text=self.ta(it[1]), font=("Segoe UI", 14, "bold"),
                  bg=_PANEL_BG, fg=_TEXT).pack(pady=(16, 6), padx=18, anchor="w")
        tk.Frame(dlg, height=1, bg=_SEP).pack(fill="x", padx=18, pady=4)

        ff = tk.Frame(dlg, bg=_PANEL_BG)
        ff.pack(fill="both", expand=True, padx=18, pady=4)
        ff.columnconfigure(0, weight=1)
        fvars = {}

        for field_def in fields:
            fk    = field_def[0]
            vk    = field_def[1]
            ftype = field_def[2] if len(field_def) > 2 else "entry"
            init  = it[2].get(vk, "")
            tk.Label(ff, text=self.tf(fk), font=("Segoe UI", 13),
                      bg=_PANEL_BG, fg=_TEXT_MUTED).pack(anchor="w", pady=(6, 2))
            if ftype == "textarea":
                ta_widget = StyledTextArea(ff, height=3)
                ta_widget.pack(fill="x")
                ta_widget.var.set(init)
                fvars[vk] = ta_widget.var
            else:
                var = tk.StringVar(value=init)
                ent = StyledEntry(ff, textvariable=var)
                ent.pack(fill="x")
                fvars[vk] = var

        br = tk.Frame(dlg, bg=_PANEL_BG)
        br.pack(fill="x", padx=18, pady=10)

        def do_save():
            self._push_undo()
            nv = {k: v.get() for k, v in fvars.items()}
            par[idx] = ("action", it[1], nv, it[3])
            self.has_unsaved_changes = True
            self.rebuild_steps()
            self.invalidate_cache()
            dlg.destroy()

        self._btn(br, self.t("update_step"), do_save,     "primary", 130, 30).pack(side="left")
        self._btn(br, self.t("cancel"),      dlg.destroy, "ghost",    80, 30).pack(side="left", padx=8)

    def edit_group(self, par, idx, grp):
        dlg = self._dialog(f"Edit - {grp[1]}", 600, 500)
        dlg.configure(bg=_PANEL_BG)
        tk.Label(dlg, text=f"> {grp[1]}", font=("Segoe UI", 14, "bold"),
                  bg=_PANEL_BG, fg=_TEXT).pack(pady=(16, 6), padx=18, anchor="w")

        mf = tk.Frame(dlg, bg=_PANEL_BG)
        mf.pack(fill="both", expand=True, padx=18, pady=4)
        mf.columnconfigure(0, weight=1)
        mf.columnconfigure(2, weight=1)
        mf.rowconfigure(0, weight=1)

        def mkbox(label, col):
            lf = tk.LabelFrame(mf, text=label, font=("Segoe UI", 13),
                                 bg=_PANEL_BG, fg=_TEXT_MUTED, bd=1, relief="solid")
            lf.grid(row=0, column=col, sticky="nsew", padx=(0,4) if col==0 else (4,0))
            lb = ThemedListbox(lf, selectmode="multiple")
            lb.pack(fill="both", expand=True, padx=4, pady=4)
            return lb

        in_lb  = mkbox(self.t("items_in_group"),     0)
        out_lb = mkbox(self.t("items_outside_group"), 2)

        grp_items = list(grp[2])
        ta = self.ta

        def _item_label(it):
            return f"  {ta(it[1]) if it[0]=='action' else it[1]}"

        for it in grp_items:
            in_lb.insert("end", _item_label(it))

        out_items = []
        def collect_out(items):
            for i, it in enumerate(items):
                if items is par and i == idx:
                    continue
                out_items.append(it)
                if it[0] == "group":
                    collect_out(it[2])
        collect_out(self.items)
        for it in out_items:
            out_lb.insert("end", _item_label(it))

        midf = tk.Frame(mf, bg=_PANEL_BG)
        midf.grid(row=0, column=1, padx=4)

        def rem():
            for si in reversed(in_lb.curselection()):
                rm = grp_items.pop(si)
                in_lb.delete(si)
                out_items.append(rm)
                out_lb.insert("end", _item_label(rm))

        def add():
            for si in reversed(out_lb.curselection()):
                it = out_items.pop(si)
                out_lb.delete(si)
                grp_items.append(it)
                in_lb.insert("end", _item_label(it))

        self._btn(midf, "Remove >", rem, "ghost", 90, 28).pack(pady=6)
        self._btn(midf, "< Add",    add, "ghost", 90, 28).pack(pady=6)

        br = tk.Frame(dlg, bg=_PANEL_BG)
        br.pack(fill="x", padx=18, pady=10)

        def do_save():
            self._push_undo()
            def item_key(it):
                return ("a", it[3]) if it[0]=="action" else ("g", id(it))
            new_keys = {item_key(it) for it in grp_items}
            def remove_absorbed(items):
                to_del = []
                for i, it in enumerate(items):
                    if items is par and i == idx:
                        continue
                    if item_key(it) in new_keys:
                        to_del.append(i)
                    elif it[0] == "group":
                        remove_absorbed(it[2])
                for i in reversed(to_del):
                    items.pop(i)
            remove_absorbed(self.items)
            par[idx] = ("group", grp[1], grp_items)
            self.has_unsaved_changes = True
            self.rebuild_steps()
            self.invalidate_cache()
            dlg.destroy()

        self._btn(br, self.t("update_step"), do_save,     "primary", 130, 30).pack(side="left")
        self._btn(br, self.t("cancel"),      dlg.destroy, "ghost",    80, 30).pack(side="left", padx=8)

    def create_group(self):
        sel = self.steps_lb.curselection()
        if not sel:
            messagebox.showinfo(self.t("create_group"), self.t("select_steps_to_group"))
            return
        m    = self._mapping()
        name = self._ask(self.t("group_name"), self.t("enter_group_name"))
        if not name:
            return
        self._push_undo()
        to_grp, to_rm = [], []
        for i in sel:
            path, _ = m[i]
            par, pidx = self._by_path(path)
            to_grp.append(par[pidx])
            to_rm.append((par, pidx))
        for par, pidx in sorted(to_rm, key=lambda x: x[1], reverse=True):
            del par[pidx]
        fp, _ = m[list(sel)[0]]
        par, ins = self._by_path(fp)
        par.insert(ins, ("group", name, to_grp))
        self.has_unsaved_changes = True
        self.rebuild_steps()
        self.invalidate_cache()

    def ungroup(self):
        sel = self.steps_lb.curselection()
        if not sel:
            return
        path, is_grp = self._mapping()[sel[0]]
        if not is_grp:
            messagebox.showinfo(self.t("ungroup"), self.t("select_group_to_ungroup"))
            return
        self._push_undo()
        par, idx = self._by_path(path)
        grp = par[idx]
        par[idx:idx + 1] = grp[2]
        self.has_unsaved_changes = True
        self.rebuild_steps()
        self.invalidate_cache()

    def rename_group(self):
        sel = self.steps_lb.curselection()
        if not sel:
            return
        path, is_grp = self._mapping()[sel[0]]
        if not is_grp:
            messagebox.showinfo(self.t("rename_group"), self.t("select_group_to_rename"))
            return
        par, idx = self._by_path(path)
        grp = par[idx]
        nn = self._ask(self.t("rename_group"), self.t("enter_group_name"), grp[1])
        if nn:
            self._push_undo()
            par[idx] = ("group", nn, grp[2])
            self.has_unsaved_changes = True
            self.rebuild_steps()

    # ── Code generation ──────────────────────────────────────────────────────
    def _flatten(self, items):
        result = []
        stack  = list(reversed(items))
        while stack:
            it = stack.pop()
            if it[0] == "action":
                result.append((it[1], it[2]))
            else:
                stack.extend(reversed(it[2]))
        return result

    def generate_bat_lines(self):
        if self._cached_lines is not None:
            return self._cached_lines
        lines = ["@echo off"]
        # Optional header comment block
        if getattr(self, "_header_enabled", True):
            ts   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            name = (os.path.basename(self.current_project_path)
                    if self.current_project_path else "Untitled")
            lines += [
                f"REM -----------------------------------------------",
                f"REM  Created: {ts}",
                f"REM  Tool   : {APP_NAME}",
                f"REM -----------------------------------------------",
            ]
        for action, vals in self._flatten(self.items):
            gen = ACTION_DEFS.get(action, {}).get("generator")
            if gen:
                lines.extend(gen(vals))
        self._cached_lines = lines
        return lines

    def refresh_preview(self):
        lines = self.generate_bat_lines()
        pv    = self.preview
        pv.configure(state="normal")
        pv.delete("1.0", "end")
        pv.insert("1.0", "\n".join(lines))
        self._apply_syntax_highlight()
        pv.configure(state="disabled")
        self.root.after_idle(self._ln.redraw)

    def _apply_syntax_highlight(self):
        pv = self.preview
        # Configure tags (idempotent)
        pv.tag_configure("sh_header",   foreground=_TEXT_MUTED,   font=("Consolas", 13))
        pv.tag_configure("sh_comment",  foreground=_TEXT_MUTED,   font=("Consolas", 13, "italic"))
        pv.tag_configure("sh_keyword",  foreground=_ACCENT,       font=("Consolas", 13, "bold"))
        pv.tag_configure("sh_danger",   foreground=_DANGER,       font=("Consolas", 13, "bold"))
        pv.tag_configure("sh_string",   foreground=_BTN_SEC_FG,   font=("Consolas", 13))
        pv.tag_configure("sh_variable", foreground=_TEXT_MUTED,   font=("Consolas", 13, "italic"))

        content = pv.get("1.0", "end-1c")
        for lineno, line in enumerate(content.split("\n"), 1):
            ls = f"{lineno}.0"
            le = f"{lineno}.end"
            if _SH_HEADER.match(line):
                pv.tag_add("sh_header", ls, le)
            elif _SH_COMMENT.match(line):
                pv.tag_add("sh_comment", ls, le)
            elif _SH_DANGER_CMDS.match(line):
                m = re.match(r"^(\s*\S+)", line)
                if m:
                    pv.tag_add("sh_danger", ls, f"{lineno}.{m.end()}")
            elif _SH_KEYWORD_CMDS.match(line):
                m = re.match(r"^(\s*@?\S+)", line)
                if m:
                    pv.tag_add("sh_keyword", ls, f"{lineno}.{m.end()}")
            # Quoted strings (applied after keyword so they can overlap)
            for sm in _SH_STRING.finditer(line):
                pv.tag_add("sh_string", f"{lineno}.{sm.start()}", f"{lineno}.{sm.end()}")
            # %variables%
            for vm in _SH_VARIABLE.finditer(line):
                pv.tag_add("sh_variable", f"{lineno}.{vm.start()}", f"{lineno}.{vm.end()}")

    def invalidate_cache(self):
        self._cached_lines = None
        self.refresh_preview()

    # ── Language / config ────────────────────────────────────────────────────
    def _lang_config_path(self):
        return os.path.join(os.path.expanduser("~"), ".ncbat", "language.txt")

    def _load_lang(self):
        try:
            p = self._lang_config_path()
            if os.path.exists(p):
                with open(p, "r") as f:
                    lang = f.read().strip()
                if lang in TRANSLATIONS:
                    return lang
        except Exception:
            pass
        return "en"

    def _save_lang(self, lang):
        try:
            os.makedirs(os.path.dirname(self._lang_config_path()), exist_ok=True)
            with open(self._lang_config_path(), "w") as f:
                f.write(lang)
        except Exception:
            pass

    def change_language(self, lang):
        self.current_lang = lang
        self._save_lang(lang)
        for w in self.menu_frame.winfo_children():
            w.destroy()
        self._build_menu_bar(self.menu_frame)
        self._refresh_ui_labels()
        self._build_project_name_widget()
        self.root.title(self.t("app_title"))
        self._update_title()
        self._status(f"{self.t('app_title')} - Language updated")

    def _refresh_ui_labels(self):
        self.lbl_steps_hdr.config(text=self.t("steps").upper())
        self.lbl_add_step.config(text=self.t("add_step_section").upper())
        self.lbl_gen_code.config(text=self.t("generated_code").upper())
        btn_texts = [
            (self._btn_move_up,   "▲  " + self.t("move_up")),
            (self._btn_move_down, "▼  " + self.t("move_down")),
            (self._btn_edit,      "✎  " + self.t("edit")),
            (self._btn_remove,    "✕  " + self.t("remove")),
            (self._btn_cgrp,      "⊞  " + self.t("create_group")),
            (self._btn_ungroup,   "⊟  " + self.t("ungroup")),
            (self._btn_rename,    "↔  " + self.t("rename_group")),
            (self._btn_duplicate, "⧉  " + self.t("duplicate")),
        ]
        for btn, txt in btn_texts:
            btn.text = txt
            btn._draw()
        self.btn_add.text = f"+ {self.t('add_step')}"
        self.btn_add._draw()
        self.btn_export.text = self.t("save_bat")
        self.btn_export._draw()
        self.search_ent._ph = self.t("search")
        if self.search_ent._is_ph:
            self.search_ent._set_ph()
        self._fill_action_lb(self._action_keys)
        self.build_fields(self._cur_en_action)
        self._update_action_tip()
        self.rebuild_steps()

    # ── Project file ops ─────────────────────────────────────────────────────
    def clear_all_steps(self):
        if not self.items:
            return
        if not messagebox.askyesno("Clear All Steps", "Remove all steps from the current project?"):
            return
        self._push_undo()
        self.items = []
        self.has_unsaved_changes = True
        self.rebuild_steps()
        self.invalidate_cache()
        self._status("All steps cleared")

    def new_project(self):
        if self.has_unsaved_changes:
            r = messagebox.askyesnocancel(self.t("unsaved_changes"), self.t("save_before_exit"))
            if r is None: return
            elif r: self.save_project()
        self.items = []
        self.next_action_id = 0
        self.current_project_path = None
        self.has_unsaved_changes  = False
        self.project_name = "Untitled"
        self._undo_stack.clear()
        self._redo_stack.clear()
        self.rebuild_steps()
        self.invalidate_cache()
        self._build_project_name_widget()
        self._status("New project")
        self._sync_unsaved_dot()

    def save_project(self):
        if self.current_project_path:
            self._save_to(self.current_project_path)
        else:
            self.save_project_as()

    def save_project_as(self):
        d = os.path.join(os.path.expanduser("~"), ".ncbat", "my projects")
        os.makedirs(d, exist_ok=True)
        # Suggest the project name as the filename
        initial = re.sub(r'[\\/:*?"<>|]', '_', self.project_name)
        p = filedialog.asksaveasfilename(
            initialdir=d,
            initialfile=initial,
            defaultextension=".ncbat",
            filetypes=[("NC Bat Project","*.ncbat"),("All","*.*")])
        if p:
            self._save_to(p)
            self.current_project_path = p

    def _save_to(self, path):
        data = {"version": APP_VERSION,
                "project_name": self.project_name,
                "items": self._ser(self.items),
                "next_action_id": self.next_action_id}
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        self.has_unsaved_changes = False
        self._status(f"Saved: {os.path.basename(path)}")
        self._sync_unsaved_dot()
        messagebox.showinfo(self.t("saved"), self.t("project_saved"))

    def _ser(self, items):
        r = []
        for it in items:
            if it[0] == "action":
                r.append({"type":"action","action":it[1],"values":it[2],"id":it[3]})
            elif it[0] == "group":
                r.append({"type":"group","name":it[1],"items":self._ser(it[2])})
        return r

    def _des(self, data):
        r = []
        for it in data:
            if it["type"] == "action":
                r.append(("action", it["action"], it["values"], it["id"]))
            elif it["type"] == "group":
                r.append(("group", it["name"], self._des(it["items"])))
        return r

    def open_project(self):
        if self.has_unsaved_changes:
            r = messagebox.askyesnocancel(self.t("unsaved_changes"), self.t("save_before_exit"))
            if r is None: return
            elif r: self.save_project()
        d = os.path.join(os.path.expanduser("~"), ".ncbat", "my projects")
        os.makedirs(d, exist_ok=True)
        p = filedialog.askopenfilename(initialdir=d,
                                        filetypes=[("NC Bat Project","*.ncbat"),("All","*.*")])
        if not p:
            return
        try:
            with open(p, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.items = self._des(data["items"])
            self.next_action_id = data.get("next_action_id", 0)
            # Load project name: saved name takes priority, fall back to filename
            self.project_name = data.get(
                "project_name",
                os.path.splitext(os.path.basename(p))[0]
            )
            self.current_project_path = p
            self.has_unsaved_changes  = False
            self._undo_stack.clear()
            self._redo_stack.clear()
            self.rebuild_steps()
            self.invalidate_cache()
            self._build_project_name_widget()
            self._sync_unsaved_dot()
            messagebox.showinfo(self.t("saved"), self.t("project_loaded"))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {e}")

    # ── Templates ────────────────────────────────────────────────────────────
    def _tdir(self):
        d = os.path.join(os.path.expanduser("~"), ".ncbat", "templates")
        os.makedirs(d, exist_ok=True)
        return d

    def _install_default_templates(self):
        """Write bundled default templates to the user's template folder if not present."""
        td = self._tdir()
        for name, data in DEFAULT_TEMPLATES.items():
            dest = os.path.join(td, f"{name}.ncbat")
            if not os.path.exists(dest):
                try:
                    with open(dest, "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                except Exception:
                    pass

    def save_as_template(self):
        if not self.items:
            messagebox.showwarning(self.t("nothing_to_save"), self.t("add_one_step"))
            return
        name = self._ask(self.t("templates"), self.t("enter_group_name"))
        if not name:
            return
        p = os.path.join(self._tdir(), f"{name}.ncbat")
        data = {"version": APP_VERSION, "items": self._ser(self.items),
                "next_action_id": self.next_action_id}
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        messagebox.showinfo(self.t("saved"), self.t("template_saved"))

    def load_template(self):
        td = self._tdir()
        tmpls = [f for f in os.listdir(td) if f.endswith('.ncbat')]
        if not tmpls:
            messagebox.showinfo(self.t("templates"), self.t("no_templates"))
            return
        dlg = self._dialog(self.t("templates"), 320, 260)
        dlg.configure(bg=_PANEL_BG)
        tk.Label(dlg, text=self.t("select_template"), font=("Segoe UI", 13),
                  bg=_PANEL_BG, fg=_TEXT).pack(pady=10, padx=14, anchor="w")
        lb = ThemedListbox(dlg)
        lb.pack(fill="both", expand=True, padx=14, pady=4)
        for t in tmpls:
            lb.insert("end", t[:-6])
        br = tk.Frame(dlg, bg=_PANEL_BG)
        br.pack(fill="x", padx=14, pady=10)

        def load():
            sel = lb.curselection()
            if not sel: return
            try:
                with open(os.path.join(td, tmpls[sel[0]]), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self._push_undo()
                self.items = self._des(data["items"])
                self.next_action_id = data.get("next_action_id", 0)
                self.has_unsaved_changes = True
                self.rebuild_steps()
                self.invalidate_cache()
                self._sync_unsaved_dot()
                dlg.destroy()
                messagebox.showinfo(self.t("saved"), self.t("template_loaded"))
            except Exception as e:
                messagebox.showerror("Error", f"Failed: {e}")

        self._btn(br, self.t("load_button"), load,        "primary", 90, 30).pack(side="left")
        self._btn(br, self.t("close"),       dlg.destroy, "ghost",   75, 30).pack(side="left", padx=8)

    def manage_templates(self):
        td = self._tdir()
        tmpls = [f for f in os.listdir(td) if f.endswith('.ncbat')]
        dlg = self._dialog(self.t("manage_templates_title"), 340, 300)
        dlg.configure(bg=_PANEL_BG)
        tk.Label(dlg, text=self.t("manage_templates_title"), font=("Segoe UI", 14, "bold"),
                  bg=_PANEL_BG, fg=_TEXT).pack(pady=12, padx=14, anchor="w")
        lb = ThemedListbox(dlg)
        lb.pack(fill="both", expand=True, padx=14, pady=4)
        for t in tmpls:
            lb.insert("end", t[:-6])
        br = tk.Frame(dlg, bg=_PANEL_BG)
        br.pack(fill="x", padx=14, pady=10)

        def delete():
            sel = lb.curselection()
            if not sel: return
            if messagebox.askyesno(self.t("confirm_delete"), self.t("confirm_delete")):
                os.remove(os.path.join(td, tmpls[sel[0]]))
                lb.delete(sel[0])
                tmpls.pop(sel[0])

        self._btn(br, self.t("delete_selected"), delete,      "danger", 120, 30).pack(side="left")
        self._btn(br, self.t("close"),           dlg.destroy, "ghost",   75, 30).pack(side="left", padx=8)

    def import_bat(self):
        p = filedialog.askopenfilename(filetypes=[("Batch files","*.bat"),("All","*.*")])
        if not p: return
        try:
            actions = parse_bat_file(p)
            if not actions:
                messagebox.showinfo(self.t("import_bat"), self.t("no_actions_found"))
                return
            self._push_undo()
            gn = self.t("imported_bat") + f" - {os.path.basename(p)}"
            gi = []
            for act, vals in actions:
                gi.append(("action", act, vals, self.next_action_id))
                self.next_action_id += 1
            self.items.append(("group", gn, gi))
            self.has_unsaved_changes = True
            self.rebuild_steps()
            self.invalidate_cache()
            messagebox.showinfo(self.t("import_bat"),
                                self.t("imported_actions").format(count=len(actions), name=gn))
        except Exception as e:
            messagebox.showerror("Error", f"Failed: {e}")

    # ── Misc actions ─────────────────────────────────────────────────────────
    def open_twitter(self):  webbrowser.open("https://twitter.com/hiroshiken71")
    def open_support(self):  webbrowser.open(SUPPORT_URL)
    def open_feedback(self): webbrowser.open(FEEDBACK_URL)

    def _fetch_latest_version(self):
        """Fetch version from the GitHub Gist API (not CDN-cached), with raw URL fallback."""
        import ssl, json as _json

        def _make_ctx(verify=True):
            ctx = ssl.create_default_context()
            if not verify:
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
            return ctx

        # --- Primary: Gist API (always fresh, never CDN-cached) ---
        for verify in (True, False):
            try:
                req = urllib.request.Request(
                    GIST_API_URL,
                    headers={
                        "User-Agent": f"{APP_NAME}",
                        "Accept": "application/vnd.github+json",
                    }
                )
                with urllib.request.urlopen(req, timeout=10, context=_make_ctx(verify)) as resp:
                    data = _json.loads(resp.read().decode("utf-8"))
                    # files is a dict keyed by filename; grab the first file's content
                    content = next(iter(data["files"].values()))["content"]
                    return content.strip().lstrip("vV")
            except Exception:
                if verify:
                    continue
                break  # both SSL modes failed, fall through to raw fallback

        # --- Fallback: raw URL (may be cached, but better than nothing) ---
        for verify in (True, False):
            try:
                req = urllib.request.Request(
                    VERSION_FILE_URL,
                    headers={"User-Agent": f"{APP_NAME}", "Cache-Control": "no-cache"},
                )
                with urllib.request.urlopen(req, timeout=10, context=_make_ctx(verify)) as resp:
                    return resp.read().decode("utf-8").strip().lstrip("vV")
            except Exception:
                if verify:
                    continue
                raise

    def _is_newer(self, latest, current):
        try:
            return tuple(int(x) for x in latest.split(".")) > \
                   tuple(int(x) for x in current.split("."))
        except Exception:
            return False

    def _show_update_popup(self, latest):
        answer = messagebox.askyesno(
            "Update Available",
            f"A new version of {APP_DISPLAY_NAME} is available: v{latest}\n\n"
            f"You are running v{APP_VERSION}.\n\n"
            "Go to the download page now?"
        )
        if answer:
            webbrowser.open(UPDATE_URL)

    def _start_update_check(self):
        def check():
            try:
                latest = self._fetch_latest_version()
                if self._is_newer(latest, APP_VERSION):
                    self.root.after(0, lambda v=latest: self._show_update_popup(v))
            except Exception as e:
                import sys
                print(f"[NC Bat] Background update check failed: {e}", file=sys.stderr)
        threading.Thread(target=check, daemon=True).start()

    def check_for_updates(self):
        """Manual check from menu — runs in a thread, shows result when done."""
        self._status("Checking for updates...")
        def check():
            try:
                latest = self._fetch_latest_version()
                if self._is_newer(latest, APP_VERSION):
                    self.root.after(0, lambda v=latest: self._show_update_popup(v))
                else:
                    def _show_ok():
                        self._status("You are up to date.")
                        messagebox.showinfo(
                            self.t("check_updates"),
                            f"You are up to date.\n\nRunning: v{APP_VERSION}"
                        )
                    self.root.after(0, _show_ok)
            except Exception as e:
                def _show_err(err=e):
                    self._status("Update check failed.")
                    messagebox.showwarning(
                        self.t("check_updates"),
                        f"Could not reach the update server.\n\n{err}"
                    )
                self.root.after(0, _show_err)
        threading.Thread(target=check, daemon=True).start()

    def open_config_folder(self):
        d = os.path.join(os.path.expanduser("~"), ".ncbat")
        os.makedirs(d, exist_ok=True)
        try:
            if os.name == "nt":
                os.startfile(d)
            elif sys.platform == "darwin":
                import subprocess
                subprocess.Popen(["open", d])
            else:
                import subprocess
                subprocess.Popen(["xdg-open", d])
        except Exception as exc:
            messagebox.showerror("Open Config Folder", f"Could not open the config folder.\n\n{exc}")

    def _text_win(self, title, content):
        dlg = self._dialog(title, 640, 500)
        dlg.configure(bg=_PANEL_BG)
        tk.Label(dlg, text=title, font=("Segoe UI", 14, "bold"),
                  bg=_PANEL_BG, fg=_TEXT).pack(pady=(16, 4), padx=18, anchor="w")
        tk.Frame(dlg, height=1, bg=_SEP).pack(fill="x", padx=18, pady=4)
        txt = tk.Text(dlg, wrap="word", relief="flat", bd=0, padx=10, pady=8,
                       font=("Segoe UI", 13), bg=_ENTRY_BG, fg=_TEXT)
        sb = tk.Scrollbar(dlg, command=txt.yview, relief="flat", bd=0, width=8,
                          bg=_SCROLLBAR, troughcolor=_ENTRY_BG, activebackground=_ACCENT)
        txt.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y", padx=(0, 8), pady=4)
        txt.pack(fill="both", expand=True, padx=18, pady=4)
        txt.insert("1.0", content)
        txt.config(state="disabled")
        self._btn(dlg, self.t("close"), dlg.destroy, "ghost", 90, 30).pack(pady=10)

    def show_help(self):  self._text_win(self.t("instruction_manual"), self.t("help_content"))
    def show_debug(self): self._text_win(self.t("debug"),              self.t("debug_content"))
    def show_about(self): self._text_win(self.t("about"),              self.t("about_content"))
    def show_terms(self): self._text_win(self.t("terms"),              self.t("terms_content"))

    # ── First-run / terms ────────────────────────────────────────────────────
    def check_first_run(self):
        tf = os.path.join(os.path.expanduser("~"), ".ncbat", "terms_accepted")
        if not os.path.exists(tf):
            self._lang_sel(tf)
        else:
            self._install_default_templates()
            # Offer to recover the most recent autosave if it is fresh enough
            self.root.after(500, self._offer_autosave_recovery)

    def _offer_autosave_recovery(self):
        """If a recent autosave exists and the project is empty, offer to restore it."""
        if self.items:
            return
        try:
            files = sorted(
                [f for f in os.listdir(self._autosave_dir)
                 if f.startswith("autosave_") and f.endswith(".ncbat")],
                reverse=True
            )
            if not files:
                return
            latest = os.path.join(self._autosave_dir, files[0])
            age = datetime.datetime.now() - datetime.datetime.fromtimestamp(
                os.path.getmtime(latest))
            if age > datetime.timedelta(hours=12):
                return
            ts = datetime.datetime.fromtimestamp(
                os.path.getmtime(latest)).strftime("%H:%M on %d %b")
            answer = messagebox.askyesno(
                "Recover Autosave",
                f"NC Bat found an autosaved session from {ts}.\n\n"
                "Would you like to recover it?"
            )
            if answer:
                with open(latest, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.items = self._des(data["items"])
                self.next_action_id = data.get("next_action_id", 0)
                self.project_name = data.get("project_name", "Untitled")
                self.has_unsaved_changes = True
                self.rebuild_steps()
                self.invalidate_cache()
                self._build_project_name_widget()
                self._sync_unsaved_dot()
                self._status("Autosave recovered")
        except Exception:
            pass

    def _lang_sel(self, tfile):
        dlg = tk.Toplevel(self.root)
        dlg.title("Language / Langue")
        dlg.geometry("440x260")
        dlg.transient(self.root)
        dlg.grab_set()
        dlg.protocol("WM_DELETE_WINDOW", lambda: None)
        dlg.configure(bg=_PANEL_BG)
        dlg.update_idletasks()
        dlg.geometry(f"440x260+{dlg.winfo_screenwidth()//2-220}+{dlg.winfo_screenheight()//2-130}")
        tk.Label(dlg, text=f"  {APP_NAME}", font=("Segoe UI", 15, "bold"),
                  bg=_PANEL_BG, fg=_TEXT).pack(pady=(26, 4))
        tk.Label(dlg, text="Select Language / Selectionner la langue",
                  font=("Segoe UI", 13), bg=_PANEL_BG, fg=_TEXT).pack(pady=6)
        tk.Label(dlg, text="Please choose your language\nVeuillez choisir votre langue",
                  font=("Segoe UI", 13), justify="center", bg=_PANEL_BG, fg=_TEXT_MUTED).pack(pady=4)
        br = tk.Frame(dlg, bg=_PANEL_BG)
        br.pack(pady=20)

        def sel(lang):
            self.current_lang = lang
            self._save_lang(lang)
            dlg.destroy()
            self._terms_dlg(tfile)

        self._btn(br, "English",  lambda: sel("en"), "primary",   125, 36, 10).pack(side="left", padx=8)
        self._btn(br, "Francais", lambda: sel("fr"), "secondary", 125, 36, 10).pack(side="left", padx=8)

    def _terms_dlg(self, tfile):
        dlg = tk.Toplevel(self.root)
        dlg.title(self.t("terms_agreement"))
        dlg.geometry("720x600")
        dlg.minsize(600, 500)
        dlg.transient(self.root)
        dlg.grab_set()
        dlg.protocol("WM_DELETE_WINDOW", lambda: None)
        dlg.configure(bg=_PANEL_BG)
        dlg.update_idletasks()
        sw, sh = dlg.winfo_screenwidth(), dlg.winfo_screenheight()
        w = 720; h = min(600, sh - 100)
        dlg.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        tk.Label(dlg, text=f"  {APP_NAME} - {self.t('terms')}",
                  font=("Segoe UI", 14, "bold"), bg=_PANEL_BG, fg=_TEXT).pack(
            pady=(18, 4), padx=20, anchor="w")
        tk.Frame(dlg, height=1, bg=_SEP).pack(fill="x", padx=20, pady=4)
        txt = tk.Text(dlg, wrap="word", relief="flat", bd=0, padx=10, pady=8,
                       font=("Segoe UI", 13), bg=_ENTRY_BG, fg=_TEXT)
        sb = tk.Scrollbar(dlg, command=txt.yview, relief="flat", bd=0, width=8,
                          bg=_SCROLLBAR, troughcolor=_ENTRY_BG, activebackground=_ACCENT)
        txt.configure(yscrollcommand=sb.set)
        br = tk.Frame(dlg, bg=_PANEL_BG)
        br.pack(side="bottom", fill="x", padx=20, pady=12)
        sb.pack(side="right", fill="y", padx=(0, 8), pady=4)
        txt.pack(fill="both", expand=True, padx=20, pady=4)
        txt.insert("1.0", self.t("terms_content"))
        txt.config(state="disabled")

        def accept():
            os.makedirs(os.path.dirname(tfile), exist_ok=True)
            with open(tfile, 'w') as f:
                f.write("accepted")
            dlg.destroy()
            self._install_default_templates()
            self._refresh_ui_labels()
            self._update_title()
            self.root.after(500, self._offer_autosave_recovery)

        def decline():
            messagebox.showwarning(self.t("terms_agreement"), self.t("must_accept_terms"))
            self.root.destroy()

        self._btn(br, self.t("accept_terms"),  accept,  "primary", 150, 36, 10).pack(side="right")
        self._btn(br, self.t("decline_terms"), decline, "ghost",   110, 36, 10).pack(side="right", padx=8)

    # ── Lifecycle ────────────────────────────────────────────────────────────
    def on_closing(self):
        if self.has_unsaved_changes:
            r = messagebox.askyesnocancel(self.t("unsaved_changes"), self.t("save_before_exit"))
            if r is None: return
            elif r: self.save_project()
        self.root.destroy()

    def _schedule_autosave(self):
        self.root.after(AUTO_SAVE_INTERVAL, self._do_autosave)

    def _do_autosave(self):
        if self.items:
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            p  = os.path.join(self._autosave_dir, f"autosave_{ts}.ncbat")
            data = {"version": APP_VERSION,
                    "project_name": self.project_name,
                    "items": self._ser(self.items),
                    "next_action_id": self.next_action_id}
            try:
                with open(p, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                self.lbl_as.config(text=f"Autosaved {datetime.datetime.now().strftime('%H:%M')}")
            except Exception:
                pass
            # Prune autosaves older than 24h (only runs when there are items to save)
            cutoff = datetime.datetime.now() - datetime.timedelta(hours=24)
            try:
                for fn in os.listdir(self._autosave_dir):
                    if fn.startswith("autosave_") and fn.endswith(".ncbat"):
                        fp = os.path.join(self._autosave_dir, fn)
                        try:
                            if datetime.datetime.fromtimestamp(os.path.getmtime(fp)) < cutoff:
                                os.remove(fp)
                        except Exception:
                            pass
            except Exception:
                pass
        self._schedule_autosave()

    # ── Verification ─────────────────────────────────────────────────────────
    def _verify(self, lines):
        DANGER = [
            (r'\bformat\b',                         "Contains 'format' - can erase an entire drive."),
            (r'del\s+/[fsq\s]*[fsq]\s+["\']?[A-Za-z]:\\', "Recursive delete from drive root - destructive."),
            (r'r[md]dir\s+/s\s+/q\s+["\']?[A-Za-z]:\\',   "Removes directory tree from drive root - destructive."),
        ]
        WARN = [
            (r'reg\s+(delete|add)',                   "Modifies the Windows Registry."),
            (r'\bshutdown\b',                         "Contains 'shutdown' - will restart/shut off the computer."),
            (r'taskkill.*?(svchost|lsass|winlogon|csrss|smss|wininit)', "Kills a critical Windows process."),
            (r'del\s+/[fsq\s]*[fsq]',                 "Force/recursive delete - check the target path."),
            (r'r[md]dir\s+/s',                        "Recursive directory remove - check the target path."),
        ]
        INFO = [
            (r'powershell',                           "Runs PowerShell - verify the command."),
            (r'set\s+(PATH|PATHEXT|COMSPEC|SYSTEMROOT|WINDIR)\s*=', "Overwrites a critical env variable."),
        ]
        combined = "\n".join(lines)
        issues   = []
        for p, m in DANGER:
            if re.search(p, combined, re.I): issues.append({"level":"danger",  "message":m})
        for p, m in WARN:
            if re.search(p, combined, re.I): issues.append({"level":"warning", "message":m})
        for p, m in INFO:
            if re.search(p, combined, re.I): issues.append({"level":"info",    "message":m})
        seen = set()
        return [i for i in issues if not (i["message"] in seen or seen.add(i["message"]))]

    def _verify_dlg(self, issues, on_export):
        has_danger = any(i["level"] == "danger" for i in issues)
        dlg = self._dialog("Verification Report", 520, 340)
        dlg.configure(bg=_PANEL_BG)
        dlg.resizable(False, False)
        tk.Label(dlg, text="Verification Report", font=("Segoe UI", 14, "bold"),
                  bg=_PANEL_BG, fg=_TEXT).pack(pady=(16, 2), padx=18, anchor="w")
        tk.Label(dlg, text=f"{len(issues)} issue(s) found in your script:",
                  font=("Segoe UI", 13), bg=_PANEL_BG, fg=_TEXT_MUTED).pack(padx=18, anchor="w")
        tk.Frame(dlg, height=1, bg=_SEP).pack(fill="x", padx=18, pady=6)

        br = tk.Frame(dlg, bg=_PANEL_BG)
        br.pack(side="bottom", fill="x", padx=18, pady=12)
        self._btn(br, "Go Back & Fix", dlg.destroy, "secondary", 150, 36).pack(side="left")
        exp_label = "Export Anyway (Risk!)" if has_danger else "Export Anyway"

        def do_exp():
            dlg.destroy()
            on_export()

        self._btn(br, exp_label, do_exp, "danger" if has_danger else "primary", 170, 36).pack(side="right")

        tf = tk.Frame(dlg, bg=_PANEL_BG)
        tf.pack(fill="both", expand=True, padx=18)
        tf.columnconfigure(0, weight=1)
        tf.rowconfigure(0, weight=1)
        txt = tk.Text(tf, wrap="word", relief="flat", bd=0, padx=12, pady=10,
                       font=("Segoe UI", 13), bg=_ENTRY_BG, fg=_TEXT)
        txt.grid(row=0, column=0, sticky="nsew")
        txt.tag_configure("danger",  foreground=_DANGER,    font=("Segoe UI", 13, "bold"))
        txt.tag_configure("warning", foreground="#D97706",   font=("Segoe UI", 13, "bold"))
        txt.tag_configure("info",    foreground=_TEXT_MUTED, font=("Segoe UI", 13, "bold"))
        txt.tag_configure("body",    foreground=_TEXT,       font=("Segoe UI", 12))
        icons = {"danger": "✕  DANGER", "warning": "⚠  WARNING", "info": "ℹ  NOTE"}
        for iss in issues:
            txt.insert("end", f"{icons.get(iss['level'], iss['level'])}  ", iss["level"])
            txt.insert("end", iss["message"] + "\n\n", "body")
        txt.config(state="disabled")

    def save_bat(self):
        if not self.items:
            messagebox.showwarning(self.t("nothing_to_save"), self.t("add_one_step"))
            return
        lines  = self.generate_bat_lines()
        issues = self._verify(lines)

        def do_save():
            p = filedialog.asksaveasfilename(defaultextension=".bat",
                                              filetypes=[("Batch files","*.bat")])
            if not p: return
            with open(p, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            self._status(f"Exported: {os.path.basename(p)}")

        if issues:
            self._verify_dlg(issues, do_save)
        else:
            do_save()

    # ── Helpers ──────────────────────────────────────────────────────────────
    def _status(self, msg, duration=4000):
        self.lbl_st.config(text=f"  {msg}", fg=_TEXT_MUTED)
        if hasattr(self, "_status_job") and self._status_job:
            self.root.after_cancel(self._status_job)
        def _fade():
            self.lbl_st.config(text=f"  {APP_NAME} ready", fg=_TEXT_LIGHT)
            self._status_job = None
        self._status_job = self.root.after(duration, _fade)

    def _sync_unsaved_dot(self):
        """Show/hide the ● unsaved-changes indicator in the header."""
        try:
            if self.has_unsaved_changes:
                self._lbl_unsaved.pack(side="left")
            else:
                self._lbl_unsaved.pack_forget()
        except Exception:
            pass
        self._update_title()

    def _dialog(self, title, w, h):
        d = tk.Toplevel(self.root)
        d.title(title)
        d.geometry(f"{w}x{h}")
        d.transient(self.root)
        d.grab_set()
        d.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width()  - w) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - h) // 2
        d.geometry(f"{w}x{h}+{max(0,x)}+{max(0,y)}")
        return d

    def _btn(self, parent, text, cmd, style, w=100, h=36, fs=11):
        b = RoundedButton(parent, text, command=cmd, style=style, width=w, height=h, font_size=fs)
        b.configure(bg=_PANEL_BG)
        b.apply_theme(None)
        return b

    def _ask(self, title, prompt, initial=""):
        dlg = self._dialog(title, 360, 172)
        dlg.configure(bg=_PANEL_BG)
        tk.Label(dlg, text=prompt, font=("Segoe UI", 13),
                  bg=_PANEL_BG, fg=_TEXT).pack(pady=(18, 6), padx=18, anchor="w")
        var = tk.StringVar(value=initial)
        ent = StyledEntry(dlg, textvariable=var)
        ent.pack(fill="x", padx=18, pady=4)
        if initial:
            ent.set(initial)
        result = [None]

        def ok(_e=None):
            result[0] = var.get().strip()
            dlg.destroy()

        br = tk.Frame(dlg, bg=_PANEL_BG)
        br.pack(fill="x", padx=18, pady=10)
        self._btn(br, "OK",             ok,          "primary", 72, 28).pack(side="left")
        self._btn(br, self.t("cancel"), dlg.destroy, "ghost",   72, 28).pack(side="left", padx=8)
        ent._e.bind("<Return>", ok)
        ent._e.focus_set()
        dlg.wait_window()
        return result[0]


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)
    try:
        root.tk.call('tk', 'scaling', 1.0)
    except Exception:
        pass

    # Set window icons (ico and png)
    try:
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        ico_path = os.path.join(base_dir, "Assets", "icon.ico")
        png_path = os.path.join(base_dir, "Assets", "icon.png")
        
        # Copy NC Bat Blue.png to icon.png if it does not exist
        if not os.path.exists(png_path):
            blue_png = os.path.join(base_dir, "Assets", "NC Bat Blue.png")
            if os.path.exists(blue_png):
                import shutil
                shutil.copy2(blue_png, png_path)

        if os.path.exists(ico_path):
            root.iconbitmap(ico_path)
        if os.path.exists(png_path):
            img = tk.PhotoImage(file=png_path)
            root.iconphoto(True, img)
    except Exception:
        pass

    app = BatBuilderApp(root)
    root.mainloop()
