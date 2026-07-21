"""
theme.py - Dark hacker theme constants used across all windows.
Cyber-Attack Simulator & Defense Lab
"""

# ── Palette ────────────────────────────────────────────────────────────────────
BG_DARK   = "#0a0e1a"    # main background
BG_PANEL  = "#111827"    # panel/card background
BG_INPUT  = "#1c2333"    # entry fields and terminal bg
BG_HOVER  = "#1a2235"    # hover state

GREEN     = "#00ff88"    # success, score, primary accent
RED       = "#ff4444"    # danger, attack
AMBER     = "#ffaa00"    # warning, brute force
BLUE      = "#4a9eff"    # info, DDoS
CYAN      = "#00ccff"    # headers, defense terminal
PURPLE    = "#a855f7"    # SQL injection
MUTED     = "#64748b"    # secondary text
TEXT      = "#e2e8f0"    # primary text
WHITE     = "#ffffff"

BORDER_GREEN  = "#1a4a30"
BORDER_RED    = "#4a1a1a"
BORDER_AMBER  = "#4a3800"
BORDER_BLUE   = "#1a2f4a"
BORDER_PANEL  = "#1e2535"

# ── Fonts ──────────────────────────────────────────────────────────────────────
FONT_MONO_LG  = ("Courier New", 14, "bold")
FONT_MONO_MD  = ("Courier New", 12)
FONT_MONO_SM  = ("Courier New", 10)
FONT_MONO_XS  = ("Courier New", 9)

FONT_TITLE    = ("Courier New", 20, "bold")
FONT_SUBTITLE = ("Courier New", 13, "bold")
FONT_LABEL    = ("Courier New", 10)
FONT_BODY     = ("Courier New", 11)
FONT_BTN      = ("Courier New", 11, "bold")

# ── Attack label colors ────────────────────────────────────────────────────────
ATTACK_COLORS = {
    "phishing":   {"fg": RED,    "bg": BORDER_RED},
    "bruteforce": {"fg": AMBER,  "bg": BORDER_AMBER},
    "ddos":       {"fg": BLUE,   "bg": BORDER_BLUE},
    "sqli":       {"fg": PURPLE, "bg": "#2a1a4a"},
}

ATTACK_LABELS = {
    "phishing":   "[~] PHISHING EMAIL",
    "bruteforce": "[K] BRUTE FORCE ATTACK",
    "ddos":       "[~] DDoS FLOOD",
    "sqli":       "[!] SQL INJECTION",
}

# ── Widget style helper ────────────────────────────────────────────────────────
def styled_entry(parent, **kwargs):
    """Return a pre-styled dark Entry widget."""
    import tkinter as tk
    defaults = dict(
        bg=BG_INPUT, fg=TEXT,
        insertbackground=GREEN,
        relief="flat", bd=0,
        font=FONT_MONO_MD,
        highlightthickness=1,
        highlightcolor=GREEN,
        highlightbackground=BORDER_PANEL,
    )
    defaults.update(kwargs)
    return tk.Entry(parent, **defaults)


def styled_button(parent, text, command, color=GREEN, **kwargs):
    """Return a pre-styled flat button."""
    import tkinter as tk
    defaults = dict(
        text=text,
        command=command,
        bg=BG_PANEL,
        fg=color,
        activebackground=BG_HOVER,
        activeforeground=color,
        relief="flat", bd=0,
        cursor="hand2",
        font=FONT_BTN,
        highlightthickness=1,
        highlightcolor=color,
        highlightbackground=color,
        padx=14, pady=7,
    )
    defaults.update(kwargs)
    return tk.Button(parent, **defaults)


def styled_label(parent, text="", color=TEXT, font=None, **kwargs):
    import tkinter as tk
    defaults = dict(
        text=text,
        bg=BG_DARK,
        fg=color,
        font=font or FONT_BODY,
    )
    defaults.update(kwargs)
    return tk.Label(parent, **defaults)


def section_header(parent, text):
    """A small muted section heading label."""
    import tkinter as tk
    return tk.Label(
        parent, text=text,
        bg=BG_DARK, fg=MUTED,
        font=("Courier New", 9, "bold"),
        anchor="w"
    )
