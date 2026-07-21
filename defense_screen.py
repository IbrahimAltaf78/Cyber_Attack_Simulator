"""
defense_screen.py - Window 2: Defense Terminal  v3
Dynamic widgets per attack type, combo display, streak feedback.
"""
import tkinter as tk
import random
import theme as T


class DefenseScreen(tk.Frame):
    def __init__(self, master, attack_data, game_controller, on_submit, on_next_round):
        super().__init__(master, bg=T.BG_DARK)
        self.atk           = attack_data
        self.gc            = game_controller
        self.on_submit     = on_submit
        self.on_next_round = on_next_round
        self._answered     = False
        self._ddos_decisions   = {}
        self._ddos_entry_vars  = {}
        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)
        atype = self.atk["attack_type"]
        cfg   = T.ATTACK_COLORS.get(atype, {"fg": T.TEXT})

        # ── Header ──────────────────────────────────────────────────────────
        top = tk.Frame(self, bg=T.BG_PANEL,
                       highlightthickness=1, highlightbackground=T.BORDER_AMBER)
        top.pack(fill="x", padx=12, pady=(12,0))
        tk.Label(top, text="// DEFENSE TERMINAL",
                 bg=T.BG_PANEL, fg=T.AMBER,
                 font=("Courier New",12,"bold")).pack(side="left",padx=12,pady=8)

        title = self.atk.get("title", T.ATTACK_LABELS.get(atype, atype))
        tk.Label(top, text=title, bg=T.BG_PANEL, fg=cfg["fg"],
                 font=("Courier New",10,"bold")).pack(side="right",padx=12)

        # ── Combo + streak HUD ───────────────────────────────────────────────
        hud = tk.Frame(self, bg=T.BG_DARK)
        hud.pack(fill="x", padx=14, pady=(4,0))

        streak = self.gc.score_mgr.current_streak
        from score_manager import COMBO_MULTIPLIERS
        mult   = COMBO_MULTIPLIERS.get(min(streak+1, 5), 2.0)
        sc_col = T.GREEN if streak == 0 else (T.AMBER if streak < 3 else T.RED)

        tk.Label(hud, text=f"Current Streak: {streak}",
                 bg=T.BG_DARK, fg=sc_col,
                 font=("Courier New",9,"bold")).pack(side="left")
        tk.Label(hud, text=f"   Next answer multiplier: x{mult:.1f}",
                 bg=T.BG_DARK, fg=T.PURPLE,
                 font=("Courier New",9)).pack(side="left")

        hints     = self.gc.score_mgr.hints_remaining
        hint_cost = self.gc.score_mgr.settings["hint_cost"]
        self.hint_count_var = tk.StringVar(value=f"Hints: {hints}")
        tk.Label(hud, textvariable=self.hint_count_var,
                 bg=T.BG_DARK, fg=T.MUTED,
                 font=("Courier New",9)).pack(side="right", padx=4)

        self.hint_btn = T.styled_button(
            hud, f"HINT (-{hint_cost}pts)",
            self._use_hint, color=T.AMBER,
            font=("Courier New",9,"bold"), padx=8, pady=3)
        if self.gc.difficulty in ("expert",) or hints == 0:
            self.hint_btn.config(state="disabled", fg=T.MUTED)
        self.hint_btn.pack(side="right")

        # ── Description ──────────────────────────────────────────────────────
        tk.Label(self, text=self.atk.get("description",""),
                 bg=T.BG_DARK, fg=T.TEXT,
                 font=("Courier New",10),
                 wraplength=640, justify="center").pack(pady=(6,0))

        # ── Hint reveal box ──────────────────────────────────────────────────
        self.hint_frame = tk.Frame(self, bg="#1a150a",
                                   highlightthickness=1,
                                   highlightbackground=T.BORDER_AMBER)
        self.hint_label = tk.Label(self.hint_frame, text="",
                                   bg="#1a150a", fg=T.AMBER,
                                   font=("Courier New",10),
                                   wraplength=620, justify="left")
        self.hint_label.pack(padx=12, pady=8)

        # ── Widget area ──────────────────────────────────────────────────────
        self.widget_frame = tk.Frame(self, bg=T.BG_PANEL,
                                     highlightthickness=1,
                                     highlightbackground=T.BORDER_PANEL)
        self.widget_frame.pack(fill="x", padx=12, pady=(6,0), ipadx=10, ipady=10)

        {
            "phishing":   self._render_phishing,
            "bruteforce": self._render_bruteforce,
            "ddos":       self._render_ddos,
            "sqli":       self._render_sqli,
        }.get(atype, lambda: None)()

        # ── Feedback ─────────────────────────────────────────────────────────
        self.feedback_var   = tk.StringVar()
        self.feedback_frame = tk.Frame(self, bg=T.BG_PANEL,
                                       highlightthickness=1,
                                       highlightbackground=T.BORDER_GREEN)
        self.feedback_label = tk.Label(self.feedback_frame,
                                       textvariable=self.feedback_var,
                                       bg=T.BG_PANEL, fg=T.GREEN,
                                       font=("Courier New",10),
                                       wraplength=640, justify="left")
        self.feedback_label.pack(padx=14, pady=10)

    # ── Hint ──────────────────────────────────────────────────────────────────

    def _use_hint(self):
        if self.gc.use_hint():
            self.hint_count_var.set(f"Hints: {self.gc.score_mgr.hints_remaining}")
            self.hint_label.config(text="[?] HINT: " + self.atk.get("hint","No hint."))
            self.hint_frame.pack(fill="x", padx=12, pady=(4,0))
            self.hint_btn.config(state="disabled", fg=T.MUTED)

    # ── Feedback ──────────────────────────────────────────────────────────────

    def _show_feedback(self, result):
        self._answered = True
        correct = result["correct"]
        streak  = result.get("streak", 0)
        color   = T.GREEN if correct else T.RED
        border  = T.BORDER_GREEN if correct else T.BORDER_RED
        msg     = result["message"]

        # Extra streak message
        if correct and streak >= 2:
            from score_manager import COMBO_MULTIPLIERS
            mult = COMBO_MULTIPLIERS.get(min(streak, 5), 2.0)
            msg += f"\n   COMBO x{mult:.1f} — streak {streak}!"

        self.feedback_var.set(msg)
        self.feedback_frame.config(highlightbackground=border)
        self.feedback_label.config(fg=color)
        self.feedback_frame.pack(fill="x", padx=12, pady=(8,0))
        self.on_submit(result)
        self.after(2800, self.on_next_round)

    # ══════════════════════════════════════════════════════════════════════════
    # WIDGET 1 — PHISHING
    # ══════════════════════════════════════════════════════════════════════════

    def _render_phishing(self):
        p = self.widget_frame
        tk.Label(p, text="Click the MOST DANGEROUS element in the email below.",
                 bg=T.BG_PANEL, fg=T.MUTED,
                 font=("Courier New",9)).pack(anchor="w", padx=6, pady=(0,6))

        email_bg = tk.Frame(p, bg="#060a12",
                            highlightthickness=1, highlightbackground=T.BORDER_GREEN)
        email_bg.pack(fill="x", padx=4, ipady=4)

        hdr = tk.Frame(email_bg, bg="#060a12")
        hdr.pack(fill="x", padx=12, pady=(8,0))
        for lbl, val, col in [
            ("From:    ", self.atk.get("from_addr","?"), T.RED),
            ("To:      ", self.atk.get("to_addr","?"),   T.TEXT),
            ("Subject: ", self.atk.get("subject","?"),   T.AMBER),
        ]:
            row = tk.Frame(hdr, bg="#060a12")
            row.pack(anchor="w")
            tk.Label(row, text=lbl, bg="#060a12", fg=T.MUTED,
                     font=("Courier New",9)).pack(side="left")
            tk.Label(row, text=val, bg="#060a12", fg=col,
                     font=("Courier New",9)).pack(side="left")

        tk.Frame(email_bg, bg=T.BORDER_PANEL, height=1).pack(fill="x", padx=12, pady=5)
        body = tk.Frame(email_bg, bg="#060a12")
        body.pack(fill="x", padx=12, pady=(0,10))

        for entry in self.atk.get("body_lines", []):
            kind = entry[0]; text = entry[1] if len(entry)>1 else ""
            target = entry[2] if len(entry)>2 else kind

            if kind == "text":
                tk.Label(body, text=text, bg="#060a12", fg=T.TEXT,
                         font=("Courier New",10), justify="left", anchor="w").pack(anchor="w")
            elif kind == "link":
                l = tk.Label(body, text=text, bg="#060a12", fg=T.CYAN,
                             font=("Courier New",10,"underline"), cursor="hand2")
                l.pack(anchor="w")
                l.bind("<Button-1>", lambda _, t=target: self._phishing_click(t))
                l.bind("<Enter>", lambda e,w=l: w.config(bg=T.BORDER_BLUE))
                l.bind("<Leave>", lambda e,w=l: w.config(bg="#060a12"))
            elif kind == "urgent":
                l = tk.Label(body, text=text, bg="#060a12", fg=T.AMBER,
                             font=("Courier New",10,"underline"), cursor="hand2")
                l.pack(anchor="w")
                l.bind("<Button-1>", lambda _, t=target: self._phishing_click(t))
                l.bind("<Enter>", lambda e,w=l: w.config(bg=T.BORDER_AMBER))
                l.bind("<Leave>", lambda e,w=l: w.config(bg="#060a12"))
            elif kind == "sender":
                l = tk.Label(body, text=text, bg="#060a12", fg=T.TEXT,
                             font=("Courier New",10,"underline"), cursor="hand2")
                l.pack(anchor="w")
                l.bind("<Button-1>", lambda _, t=target: self._phishing_click(t))
                l.bind("<Enter>", lambda e,w=l: w.config(bg=T.BORDER_PANEL))
                l.bind("<Leave>", lambda e,w=l: w.config(bg="#060a12"))

        tk.Label(p, text="All underlined elements are clickable.",
                 bg=T.BG_PANEL, fg=T.MUTED, font=("Courier New",8)).pack(pady=(4,0))

    def _phishing_click(self, target):
        if self._answered: return
        self._show_feedback(self.gc.submit_answer(target))

    # ══════════════════════════════════════════════════════════════════════════
    # WIDGET 2 — BRUTE FORCE
    # ══════════════════════════════════════════════════════════════════════════

    def _render_bruteforce(self):
        p = self.widget_frame
        tk.Label(p, text="Review the auth log. Type the attacking IP and press ENTER or click BLOCK.",
                 bg=T.BG_PANEL, fg=T.MUTED,
                 font=("Courier New",9)).pack(anchor="w", padx=6, pady=(0,8))

        log_f = tk.Frame(p, bg="#060a12",
                         highlightthickness=1, highlightbackground=T.BORDER_PANEL)
        log_f.pack(fill="x", padx=4, pady=(0,10))

        for ip, attempts, suspicious in self.atk.get("entries", []):
            col = T.RED if suspicious else T.GREEN
            row = tk.Frame(log_f, bg="#060a12")
            row.pack(fill="x", padx=10, pady=3)
            tk.Label(row, text=ip, bg="#060a12", fg=col,
                     font=("Courier New",10), width=20, anchor="w").pack(side="left")
            bg2 = "#1a0a0a" if suspicious else "#060a12"
            tk.Label(row, text=attempts, bg=bg2, fg=col,
                     font=("Courier New",10)).pack(side="left", padx=8)

        inp = tk.Frame(p, bg=T.BG_PANEL)
        inp.pack(fill="x", padx=4)
        tk.Label(inp, text="Block IP:", bg=T.BG_PANEL, fg=T.MUTED,
                 font=("Courier New",10)).pack(side="left", padx=6)
        self.bf_var = tk.StringVar()
        entry = T.styled_entry(inp, textvariable=self.bf_var, width=22)
        entry.pack(side="left", padx=6)
        entry.bind("<Return>", lambda _: self._submit_bf())
        entry.focus_set()
        T.styled_button(inp, "BLOCK IP", self._submit_bf,
                        color=T.RED, padx=12, pady=4).pack(side="left", padx=4)

    def _submit_bf(self):
        if self._answered: return
        self._show_feedback(self.gc.submit_answer(self.bf_var.get().strip()))

    # ══════════════════════════════════════════════════════════════════════════
    # WIDGET 3 — DDoS
    # ══════════════════════════════════════════════════════════════════════════

    def _render_ddos(self):
        p = self.widget_frame
        tk.Label(p, text="Classify every source: ALLOW legitimate traffic, BLOCK flood IPs. Then SUBMIT.",
                 bg=T.BG_PANEL, fg=T.MUTED,
                 font=("Courier New",9)).pack(anchor="w", padx=6, pady=(0,8))

        raw = list(self.atk.get("traffic", []))
        random.shuffle(raw)

        for ip, pkt_display, is_flood in raw:
            # Slight variance in displayed pkt rate
            try:
                base = int(pkt_display.split(" ")[0].replace(",","").split("(")[0])
                v    = random.randint(-200,200) if is_flood else random.randint(-2,2)
                display = f"{max(1,base+v):,} {pkt_display.split(' ',1)[1]}" if " " in pkt_display else f"{max(1,base+v):,} pkt/s"
            except Exception:
                display = pkt_display

            row = tk.Frame(p, bg="#060a12",
                           highlightthickness=1, highlightbackground=T.BORDER_PANEL)
            row.pack(fill="x", padx=4, pady=3)

            tk.Label(row, text=ip, bg="#060a12",
                     fg=T.RED if is_flood else T.BLUE,
                     font=("Courier New",10), width=22, anchor="w").pack(side="left",padx=8,pady=5)
            tk.Label(row, text=display, bg="#060a12", fg=T.MUTED,
                     font=("Courier New",9)).pack(side="left", expand=True)

            var = tk.StringVar(value="")
            self._ddos_entry_vars[ip] = var

            bf = tk.Frame(row, bg="#060a12")
            bf.pack(side="right", padx=8)
            tk.Button(bf, text="ALLOW",
                      command=lambda i=ip,v=var,r=row: self._ddos_decide(i,"allow",v,r),
                      bg="#060a12", fg=T.GREEN, relief="flat", bd=0,
                      activebackground=T.BG_HOVER, activeforeground=T.GREEN,
                      cursor="hand2", font=("Courier New",9,"bold"),
                      highlightthickness=1, highlightbackground=T.BORDER_GREEN,
                      padx=8, pady=3).pack(side="left", padx=3)
            tk.Button(bf, text="BLOCK",
                      command=lambda i=ip,v=var,r=row: self._ddos_decide(i,"block",v,r),
                      bg="#060a12", fg=T.RED, relief="flat", bd=0,
                      activebackground=T.BG_HOVER, activeforeground=T.RED,
                      cursor="hand2", font=("Courier New",9,"bold"),
                      highlightthickness=1, highlightbackground=T.BORDER_RED,
                      padx=8, pady=3).pack(side="left", padx=3)

        self.ddos_submit_btn = T.styled_button(
            p, "SUBMIT ALL DECISIONS", self._submit_ddos,
            color=T.CYAN, font=("Courier New",11,"bold"), padx=16, pady=8)
        self.ddos_submit_btn.pack(fill="x", padx=4, pady=(10,0))
        self.ddos_submit_btn.config(state="disabled", fg=T.MUTED)

        total = len(raw)
        self.ddos_count_var = tk.StringVar(value=f"0 / {total} classified")
        tk.Label(p, textvariable=self.ddos_count_var,
                 bg=T.BG_PANEL, fg=T.MUTED,
                 font=("Courier New",9)).pack(pady=(3,0))

    def _ddos_decide(self, ip, action, var, row):
        if var.get(): return
        var.set(action)
        self._ddos_decisions[ip] = action
        row.config(bg="#0a1a0a" if action=="allow" else "#1a0a0a")
        for ch in row.winfo_children():
            try: ch.config(bg=row.cget("bg"))
            except: pass
        done  = len(self._ddos_decisions)
        total = len(self._ddos_entry_vars)
        self.ddos_count_var.set(f"{done} / {total} classified")
        if done == total:
            self.ddos_submit_btn.config(state="normal", fg=T.CYAN)

    def _submit_ddos(self):
        if self._answered: return
        self._show_feedback(self.gc.submit_answer(self._ddos_decisions))

    # ══════════════════════════════════════════════════════════════════════════
    # WIDGET 4 — SQL INJECTION
    # ══════════════════════════════════════════════════════════════════════════

    def _render_sqli(self):
        p = self.widget_frame
        qf = tk.Frame(p, bg="#060a12",
                      highlightthickness=1, highlightbackground=T.BORDER_PANEL)
        qf.pack(fill="x", padx=4, pady=(0,10))
        query = self.atk.get("query","SELECT * FROM users WHERE id='' OR 1=1--")
        tk.Label(qf, text=query, bg="#060a12", fg=T.RED,
                 font=("Courier New",10,"bold"),
                 wraplength=580, justify="left").pack(padx=12, pady=(8,2))
        note = self.atk.get("query_note","This is a malicious SQL query.")
        tk.Label(qf, text="  "+note, bg="#060a12", fg=T.MUTED,
                 font=("Courier New",9),
                 wraplength=580, justify="left").pack(padx=12, pady=(0,8))

        tk.Label(p, text="Select the BEST fix for this SQL injection attack:",
                 bg=T.BG_PANEL, fg=T.TEXT,
                 font=("Courier New",10)).pack(anchor="w", padx=6, pady=(0,6))

        self.sqli_var = tk.StringVar(value="")
        options = list(self.atk.get("options",[]))
        random.shuffle(options)

        for val, text in options:
            rb = tk.Radiobutton(
                p, text=text, variable=self.sqli_var, value=val,
                bg=T.BG_PANEL, fg=T.TEXT,
                activebackground=T.BG_HOVER, activeforeground=T.PURPLE,
                selectcolor=T.BG_INPUT,
                font=("Courier New",10), cursor="hand2", anchor="w")
            rb.pack(fill="x", padx=14, pady=2)

        T.styled_button(p, "APPLY FIX", self._submit_sqli,
                        color=T.PURPLE, padx=14, pady=8).pack(fill="x", padx=4, pady=(10,0))

    def _submit_sqli(self):
        if self._answered: return
        val = self.sqli_var.get()
        if not val: return
        self._show_feedback(self.gc.submit_answer(val))
