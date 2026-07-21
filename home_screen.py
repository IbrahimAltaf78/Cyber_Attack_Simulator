"""
home_screen.py - Main menu with difficulty, daily challenge, stats preview, achievements
Cyber-Attack Simulator & Defense Lab  v3
"""
import tkinter as tk
import datetime
import database as db
import theme as T


class HomeScreen(tk.Frame):
    def __init__(self, master, user, on_start_game, on_view_dashboard, on_logout):
        super().__init__(master, bg=T.BG_DARK)
        self.user = user
        self.on_start_game      = on_start_game
        self.on_view_dashboard  = on_view_dashboard
        self.on_logout          = on_logout
        self.selected_diff      = tk.StringVar(value="beginner")
        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)

        # ── Top bar ─────────────────────────────────────────────────────────
        top = tk.Frame(self, bg=T.BG_PANEL,
                       highlightthickness=1, highlightbackground=T.BORDER_PANEL)
        top.pack(fill="x", padx=12, pady=(12,0))

        tk.Label(top, text="[*] CYBER-ATTACK SIMULATOR & DEFENSE LAB",
                 bg=T.BG_PANEL, fg=T.GREEN,
                 font=("Courier New",12,"bold")).pack(side="left",padx=12,pady=8)

        for txt, cmd, col in [
            ("LOGOUT",    self.on_logout,          T.MUTED),
            ("DASHBOARD", self.on_view_dashboard,  T.CYAN),
        ]:
            tk.Button(top, text=txt, command=cmd,
                      bg=T.BG_PANEL, fg=col,
                      activebackground=T.BG_HOVER, activeforeground=col,
                      relief="flat", bd=0, cursor="hand2",
                      font=("Courier New",9,"bold"), padx=12, pady=6,
                      highlightthickness=0).pack(side="right", padx=4)

        # ── User info strip ──────────────────────────────────────────────────
        info = tk.Frame(self, bg=T.BG_DARK)
        info.pack(fill="x", padx=14, pady=(6,0))

        user_row = db.get_user_by_id(self.user["id"]) or self.user
        level  = user_row.get("level","Rookie")
        score  = user_row.get("total_score",0)
        streak = user_row.get("best_streak",0)
        sessions = user_row.get("sessions_played",0)

        for txt, col in [
            (f"Officer: {self.user['username']}", T.GREEN),
            (f"  |  Rank: {level}",               T.CYAN),
            (f"  |  Score: {score}",               T.AMBER),
            (f"  |  Best Streak: {streak}",        T.PURPLE),
            (f"  |  Sessions: {sessions}",         T.MUTED),
        ]:
            tk.Label(info, text=txt, bg=T.BG_DARK, fg=col,
                     font=("Courier New",9)).pack(side="left")

        # ── Main body: two columns ───────────────────────────────────────────
        body = tk.Frame(self, bg=T.BG_DARK)
        body.pack(fill="both", expand=True, padx=12, pady=8)
        body.columnconfigure(0, weight=3)
        body.columnconfigure(1, weight=2)

        left  = tk.Frame(body, bg=T.BG_DARK)
        left.grid(row=0, column=0, sticky="nsew", padx=(0,6))
        right = tk.Frame(body, bg=T.BG_DARK)
        right.grid(row=0, column=1, sticky="nsew")

        # ── LEFT: difficulty ─────────────────────────────────────────────────
        T.section_header(left, "  SELECT DIFFICULTY").pack(anchor="w", pady=(0,6))

        self.diff_frames = {}
        diffs = [
            ("beginner",    "BEGINNER",     T.GREEN,  "30s/round  |  3 hints\nFull score: +100  Wrong: -10\nCombo multiplier active"),
            ("intermediate","INTERMEDIATE", T.AMBER,  "20s/round  |  3 hints\nFull score: +100  Wrong: -25\nCombo multiplier active"),
            ("expert",      "EXPERT",       T.RED,    "12s/round  |  No hints\nFull score: +100  Wrong: -50\n2x combo starts at streak 2"),
        ]
        for val, label, col, desc in diffs:
            f = tk.Frame(left, bg=T.BG_PANEL,
                         highlightthickness=1, highlightbackground=T.BORDER_PANEL,
                         cursor="hand2")
            f.pack(fill="x", pady=3, ipadx=10, ipady=6)
            f.bind("<Button-1>", lambda e,v=val: self._select_diff(v))
            tk.Label(f, text=label, bg=T.BG_PANEL, fg=col,
                     font=("Courier New",11,"bold")).pack(anchor="w", padx=8)
            tk.Label(f, text=desc, bg=T.BG_PANEL, fg=T.MUTED,
                     font=("Courier New",8), justify="left").pack(anchor="w", padx=8)
            self.diff_frames[val] = f
        self._select_diff("beginner")

        # ── LEFT: Attack type overview ────────────────────────────────────────
        tk.Frame(left, bg=T.BORDER_PANEL, height=1).pack(fill="x", pady=8)
        T.section_header(left, "  4 ATTACK TYPES — SHUFFLED EACH SESSION").pack(anchor="w", pady=(0,6))

        atk_row = tk.Frame(left, bg=T.BG_DARK)
        atk_row.pack(fill="x")
        for icon, label, col in [
            ("[~]","Phishing",    T.RED),
            ("[K]","Brute Force", T.AMBER),
            ("[W]","DDoS Flood",  T.BLUE),
            ("[D]","SQL Inject",  T.PURPLE),
        ]:
            b = tk.Frame(atk_row, bg=T.BG_PANEL,
                         highlightthickness=1, highlightbackground=T.BORDER_PANEL)
            b.pack(side="left", expand=True, fill="x", padx=3, ipadx=6, ipady=6)
            tk.Label(b, text=icon, bg=T.BG_PANEL, fg=col,
                     font=("Courier New",14)).pack()
            tk.Label(b, text=label, bg=T.BG_PANEL, fg=col,
                     font=("Courier New",8,"bold")).pack()

        # ── LEFT: Combo system info ───────────────────────────────────────────
        tk.Frame(left, bg=T.BORDER_PANEL, height=1).pack(fill="x", pady=8)
        combo_f = tk.Frame(left, bg="#0a1a0a",
                           highlightthickness=1, highlightbackground=T.BORDER_GREEN)
        combo_f.pack(fill="x", ipadx=10, ipady=6)
        tk.Label(combo_f, text="[*] COMBO MULTIPLIER SYSTEM",
                 bg="#0a1a0a", fg=T.GREEN,
                 font=("Courier New",9,"bold")).pack(anchor="w", padx=8, pady=(4,2))
        combos = "Streak 1: x1.0  |  Streak 2: x1.2  |  Streak 3: x1.5  |  Streak 4: x1.8  |  Streak 5+: x2.0"
        tk.Label(combo_f, text=combos, bg="#0a1a0a", fg=T.MUTED,
                 font=("Courier New",8)).pack(anchor="w", padx=8, pady=(0,4))

        # ── RIGHT: Daily challenge ────────────────────────────────────────────
        T.section_header(right, "  DAILY CHALLENGE").pack(anchor="w", pady=(0,6))
        self._build_daily(right)

        # ── RIGHT: Recent achievements ────────────────────────────────────────
        tk.Frame(right, bg=T.BORDER_PANEL, height=1).pack(fill="x", pady=8)
        T.section_header(right, "  YOUR ACHIEVEMENTS").pack(anchor="w", pady=(0,6))
        self._build_achievements(right)

        # ── RIGHT: Quick stats ────────────────────────────────────────────────
        tk.Frame(right, bg=T.BORDER_PANEL, height=1).pack(fill="x", pady=8)
        T.section_header(right, "  QUICK STATS").pack(anchor="w", pady=(0,6))
        self._build_quick_stats(right)

        # ── Bottom: Launch button ─────────────────────────────────────────────
        tk.Frame(self, bg=T.BORDER_PANEL, height=1).pack(fill="x", padx=12, pady=(4,0))
        T.styled_button(
            self, "[ LAUNCH ATTACK SIMULATOR ]",
            self._launch, color=T.GREEN,
            font=("Courier New",13,"bold"), padx=30, pady=12
        ).pack(fill="x", padx=60, pady=10)

    def _build_daily(self, parent):
        today = datetime.date.today()
        dc    = db.get_daily_challenge(self.user["id"], today.isoformat())
        done  = dc and dc.get("completed")
        score = dc.get("score",0) if dc else 0

        df = tk.Frame(parent, bg=T.BG_PANEL,
                      highlightthickness=1,
                      highlightbackground=T.GREEN if done else T.BORDER_AMBER)
        df.pack(fill="x", ipadx=8, ipady=8)

        tk.Label(df, text=f"Date: {today.strftime('%d %b %Y')}",
                 bg=T.BG_PANEL, fg=T.MUTED,
                 font=("Courier New",8)).pack(anchor="w", padx=8, pady=(4,0))

        if done:
            tk.Label(df, text="[OK] COMPLETED",
                     bg=T.BG_PANEL, fg=T.GREEN,
                     font=("Courier New",11,"bold")).pack(anchor="w", padx=8)
            tk.Label(df, text=f"Score: {score}",
                     bg=T.BG_PANEL, fg=T.GREEN,
                     font=("Courier New",10)).pack(anchor="w", padx=8, pady=(0,4))
        else:
            tk.Label(df, text="Intermediate | 4 rounds | 2 hints",
                     bg=T.BG_PANEL, fg=T.TEXT,
                     font=("Courier New",9)).pack(anchor="w", padx=8)
            tk.Label(df, text="Bonus: +50 pts on completion",
                     bg=T.BG_PANEL, fg=T.AMBER,
                     font=("Courier New",8)).pack(anchor="w", padx=8)
            T.styled_button(
                df, "[ PLAY DAILY CHALLENGE ]",
                lambda: self.on_start_game("daily"),
                color=T.AMBER,
                font=("Courier New",9,"bold"), padx=8, pady=4,
            ).pack(fill="x", padx=8, pady=(6,4))

    def _build_achievements(self, parent):
        from achievements import ACHIEVEMENTS
        unlocked = set(db.get_user_achievements(self.user["id"]))
        total    = len(ACHIEVEMENTS)
        done_cnt = len(unlocked)

        tk.Label(parent, text=f"{done_cnt}/{total} unlocked",
                 bg=T.BG_DARK, fg=T.MUTED,
                 font=("Courier New",8)).pack(anchor="w")

        # Progress bar
        bar_outer = tk.Frame(parent, bg=T.BORDER_PANEL, height=6)
        bar_outer.pack(fill="x", pady=(2,6))
        pct = done_cnt/total if total else 0
        bar_inner = tk.Frame(bar_outer, bg=T.PURPLE, height=6)
        bar_inner.place(relwidth=pct, height=6)

        # Show up to 6 badges
        badge_frame = tk.Frame(parent, bg=T.BG_DARK)
        badge_frame.pack(fill="x")
        shown = 0
        for key, data in ACHIEVEMENTS.items():
            if shown >= 6: break
            is_done = key in unlocked
            b = tk.Frame(badge_frame, bg=T.BG_PANEL if is_done else T.BG_INPUT,
                         highlightthickness=1,
                         highlightbackground=T.PURPLE if is_done else T.BORDER_PANEL)
            b.pack(side="left", padx=2, ipadx=4, ipady=4)
            col = T.PURPLE if is_done else T.MUTED
            tk.Label(b, text=data["icon"], bg=b.cget("bg"), fg=col,
                     font=("Courier New",10)).pack()
            tk.Label(b, text=data["title"][:8], bg=b.cget("bg"), fg=col,
                     font=("Courier New",7)).pack()
            shown += 1

    def _build_quick_stats(self, parent):
        stats = db.get_user_stats(self.user["id"])
        user  = db.get_user_by_id(self.user["id"]) or self.user

        items = [
            ("Sessions",     str(stats.get("total",0)),        T.CYAN),
            ("Win Rate",     f"{stats.get('win_rate',0)}%",     T.GREEN),
            ("Best Streak",  str(user.get("best_streak",0)),   T.AMBER),
            ("Breaches",     str(stats.get("breaches",0)),     T.RED),
        ]
        row = tk.Frame(parent, bg=T.BG_DARK)
        row.pack(fill="x")
        for label, val, col in items:
            c = tk.Frame(row, bg=T.BG_PANEL,
                         highlightthickness=1, highlightbackground=T.BORDER_PANEL)
            c.pack(side="left", expand=True, fill="x", padx=2, ipadx=4, ipady=4)
            tk.Label(c, text=label, bg=T.BG_PANEL, fg=T.MUTED,
                     font=("Courier New",7)).pack()
            tk.Label(c, text=val, bg=T.BG_PANEL, fg=col,
                     font=("Courier New",13,"bold")).pack()

    def _select_diff(self, val):
        self.selected_diff.set(val)
        colors = {"beginner":T.GREEN,"intermediate":T.AMBER,"expert":T.RED}
        for v, f in self.diff_frames.items():
            f.config(highlightbackground=colors[v] if v==val else T.BORDER_PANEL)

    def _launch(self):
        self.on_start_game(self.selected_diff.get())
