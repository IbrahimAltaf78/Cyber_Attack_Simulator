"""
login_screen.py - Login and Register screens (Window 0)
Cyber-Attack Simulator & Defense Lab
"""

import tkinter as tk
from tkinter import messagebox
import theme as T
import auth


class LoginScreen(tk.Frame):
    def __init__(self, master, on_login_success):
        super().__init__(master, bg=T.BG_DARK)
        self.master = master
        self.on_login_success = on_login_success
        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)

        # ── ASCII logo ──────────────────────────────────────────────────────
        logo = (
            " ██████╗██╗   ██╗██████╗ ███████╗██████╗ \n"
            "██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗\n"
            "██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝\n"
            "██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗\n"
            "╚██████╗   ██║   ██████╔╝███████╗██║  ██║\n"
            " ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝"
        )
        tk.Label(
            self, text=logo,
            bg=T.BG_DARK, fg=T.GREEN,
            font=("Courier New", 9, "bold"),
            justify="center"
        ).pack(pady=(30, 4))

        tk.Label(
            self, text="A T T A C K   S I M U L A T O R   &   D E F E N S E   L A B",
            bg=T.BG_DARK, fg=T.MUTED,
            font=("Courier New", 9)
        ).pack(pady=(0, 24))

        # ── Card frame ──────────────────────────────────────────────────────
        card = tk.Frame(self, bg=T.BG_PANEL,
                        highlightthickness=1, highlightbackground=T.BORDER_GREEN)
        card.pack(padx=60, pady=0, ipadx=30, ipady=20)

        # Tabs
        tab_row = tk.Frame(card, bg=T.BG_PANEL)
        tab_row.pack(fill="x", padx=0, pady=(0, 20))

        self.mode = tk.StringVar(value="login")

        self.tab_login = tk.Button(
            tab_row, text="LOGIN",
            command=lambda: self._switch_tab("login"),
            bg=T.BG_PANEL, fg=T.GREEN,
            activebackground=T.BG_HOVER, activeforeground=T.GREEN,
            relief="flat", bd=0, cursor="hand2",
            font=("Courier New", 11, "bold"),
            padx=20, pady=8,
            highlightthickness=0
        )
        self.tab_login.pack(side="left")

        self.tab_reg = tk.Button(
            tab_row, text="REGISTER",
            command=lambda: self._switch_tab("register"),
            bg=T.BG_PANEL, fg=T.MUTED,
            activebackground=T.BG_HOVER, activeforeground=T.GREEN,
            relief="flat", bd=0, cursor="hand2",
            font=("Courier New", 11, "bold"),
            padx=20, pady=8,
            highlightthickness=0
        )
        self.tab_reg.pack(side="left")

        # Divider
        tk.Frame(card, bg=T.BORDER_PANEL, height=1).pack(fill="x", pady=(0, 16))

        # ── Login form ──────────────────────────────────────────────────────
        self.login_frame = tk.Frame(card, bg=T.BG_PANEL)
        self.login_frame.pack(fill="x", padx=10)
        self._build_login(self.login_frame)

        # ── Register form ───────────────────────────────────────────────────
        self.reg_frame = tk.Frame(card, bg=T.BG_PANEL)
        self._build_register(self.reg_frame)
        # reg_frame hidden by default

        # Status
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            card, textvariable=self.status_var,
            bg=T.BG_PANEL, fg=T.RED,
            font=("Courier New", 10),
            wraplength=300
        )
        self.status_label.pack(pady=(10, 4))

        tk.Label(
            self, text="© 2026  OSSD Final Term — CLO 4",
            bg=T.BG_DARK, fg=T.MUTED,
            font=("Courier New", 8)
        ).pack(side="bottom", pady=10)

    def _build_login(self, parent):
        self._lbl(parent, "USERNAME")
        self.login_user_var = tk.StringVar()
        e1 = T.styled_entry(parent, textvariable=self.login_user_var, width=28)
        e1.pack(fill="x", pady=(2, 12))

        self._lbl(parent, "PASSWORD")
        self.login_pass_var = tk.StringVar()
        e2 = T.styled_entry(parent, textvariable=self.login_pass_var, show="●", width=28)
        e2.pack(fill="x", pady=(2, 18))
        e2.bind("<Return>", lambda _: self._do_login())

        T.styled_button(parent, "[ ENTER SYSTEM ]", self._do_login, color=T.GREEN).pack(fill="x")

    def _build_register(self, parent):
        self._lbl(parent, "USERNAME (min 3 chars, letters/numbers/_)")
        self.reg_user_var = tk.StringVar()
        T.styled_entry(parent, textvariable=self.reg_user_var, width=28).pack(fill="x", pady=(2, 12))

        self._lbl(parent, "PASSWORD (min 6 chars)")
        self.reg_pass_var = tk.StringVar()
        T.styled_entry(parent, textvariable=self.reg_pass_var, show="●", width=28).pack(fill="x", pady=(2, 12))

        self._lbl(parent, "CONFIRM PASSWORD")
        self.reg_pass2_var = tk.StringVar()
        e = T.styled_entry(parent, textvariable=self.reg_pass2_var, show="●", width=28)
        e.pack(fill="x", pady=(2, 18))
        e.bind("<Return>", lambda _: self._do_register())

        T.styled_button(parent, "[ CREATE ACCOUNT ]", self._do_register, color=T.CYAN).pack(fill="x")

    def _lbl(self, parent, text):
        tk.Label(parent, text=text, bg=T.BG_PANEL, fg=T.MUTED,
                 font=("Courier New", 9)).pack(anchor="w")

    def _switch_tab(self, tab):
        self.mode.set(tab)
        if tab == "login":
            self.tab_login.config(fg=T.GREEN)
            self.tab_reg.config(fg=T.MUTED)
            self.reg_frame.pack_forget()
            self.login_frame.pack(fill="x", padx=10)
        else:
            self.tab_reg.config(fg=T.GREEN)
            self.tab_login.config(fg=T.MUTED)
            self.login_frame.pack_forget()
            self.reg_frame.pack(fill="x", padx=10)
        self.status_var.set("")

    def _do_login(self):
        result = auth.login_user(
            self.login_user_var.get().strip(),
            self.login_pass_var.get()
        )
        if result["success"]:
            self.status_var.set("")
            self.on_login_success(result["user"])
        else:
            self.status_var.set("[!!] " + result["message"])
            self.status_label.config(fg=T.RED)

    def _do_register(self):
        if self.reg_pass_var.get() != self.reg_pass2_var.get():
            self.status_var.set("[!!] Passwords do not match.")
            self.status_label.config(fg=T.RED)
            return
        result = auth.register_user(
            self.reg_user_var.get().strip(),
            self.reg_pass_var.get()
        )
        if result["success"]:
            self.status_var.set("[OK] " + result["message"])
            self.status_label.config(fg=T.GREEN)
            self._switch_tab("login")
        else:
            self.status_var.set("[!!] " + result["message"])
            self.status_label.config(fg=T.RED)
