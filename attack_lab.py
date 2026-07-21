"""
attack_lab.py - Window 1: Attack Lab with live terminal, timer bar, threat brief, streak HUD
Cyber-Attack Simulator & Defense Lab  v3
"""
import tkinter as tk
import theme as T


class AttackLabWindow(tk.Frame):
    def __init__(self, master, attack_data, round_num, total_rounds,
                 difficulty_settings, on_open_defense, on_breach,
                 current_streak=0, session_score=0):
        super().__init__(master, bg=T.BG_DARK)
        self.atk          = attack_data
        self.round_num    = round_num
        self.total_rounds = total_rounds
        self.diff         = difficulty_settings
        self.on_open_defense = on_open_defense
        self.on_breach    = on_breach
        self.streak       = current_streak
        self.session_score= session_score

        self.time_left   = difficulty_settings["time"]
        self._timer_job  = None
        self._log_job    = None
        self._log_lines  = self.atk.get("logs","").split("|")
        self._log_idx    = 0
        self._breached   = False
        self._build()
        self._start_log()
        self._tick()

    def _build(self):
        self.pack(fill="both", expand=True)

        # ── Header strip ────────────────────────────────────────────────────
        top = tk.Frame(self, bg=T.BG_PANEL,
                       highlightthickness=1, highlightbackground=T.BORDER_PANEL)
        top.pack(fill="x", padx=12, pady=(12,0))

        atype = self.atk["attack_type"]
        cfg   = T.ATTACK_COLORS.get(atype, {"fg":T.TEXT})
        lbl   = T.ATTACK_LABELS.get(atype, atype.upper())
        title = self.atk.get("title","")
        full_lbl = f"{lbl}  —  {title}" if title else lbl

        tk.Label(top, text=full_lbl, bg=T.BG_PANEL, fg=cfg["fg"],
                 font=("Courier New",12,"bold")).pack(side="left",padx=12,pady=8)

        # Round indicator
        dots = ""
        for i in range(self.total_rounds):
            dots += ("[*] " if i < self.round_num else "[ ] ")
        tk.Label(top, text=dots.strip(), bg=T.BG_PANEL, fg=T.MUTED,
                 font=("Courier New",9)).pack(side="right",padx=12)

        # ── HUD row: timer + streak + score ─────────────────────────────────
        hud = tk.Frame(self, bg=T.BG_DARK)
        hud.pack(fill="x", padx=12, pady=(4,0))

        # Timer label
        self.timer_lbl = tk.Label(hud, text=f"[T] {self.time_left}s",
                                  bg=T.BG_DARK, fg=T.GREEN,
                                  font=("Courier New",11,"bold"))
        self.timer_lbl.pack(side="left")

        # Streak
        streak_col = T.GREEN if self.streak == 0 else (
            T.AMBER if self.streak < 3 else T.RED)
        streak_txt = f"  STREAK: {self.streak}" + (
            f"  (x{min(self.streak+1,5)*0.2+0.8:.1f})" if self.streak >= 1 else "")
        tk.Label(hud, text=streak_txt, bg=T.BG_DARK, fg=streak_col,
                 font=("Courier New",10,"bold")).pack(side="left", padx=16)

        # Session score
        tk.Label(hud, text=f"  SESSION: {self.session_score} pts",
                 bg=T.BG_DARK, fg=T.CYAN,
                 font=("Courier New",10)).pack(side="right")

        # Timer progress bar
        bar_bg = tk.Frame(self, bg=T.BORDER_PANEL, height=5)
        bar_bg.pack(fill="x", padx=12, pady=(3,0))
        self.timer_fill = tk.Frame(bar_bg, bg=T.GREEN, height=5)
        self.timer_fill.place(x=0, y=0, relwidth=1.0, height=5)

        # ── Terminal box ─────────────────────────────────────────────────────
        T.section_header(self, "  LIVE THREAT FEED").pack(anchor="w", padx=14, pady=(8,3))
        term_wrap = tk.Frame(self, bg="#060a12",
                             highlightthickness=1, highlightbackground=T.BORDER_GREEN)
        term_wrap.pack(fill="x", padx=12, ipady=4)

        self.terminal = tk.Text(term_wrap, bg="#060a12", fg=T.GREEN,
                                font=("Courier New",10), height=8,
                                state="disabled", relief="flat", bd=0,
                                wrap="word", insertbackground=T.GREEN)
        scroll = tk.Scrollbar(term_wrap, command=self.terminal.yview,
                              bg=T.BG_DARK, troughcolor=T.BG_DARK)
        self.terminal.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.terminal.pack(fill="x", padx=8, pady=6)

        for tag, col in [("green",T.GREEN),("red",T.RED),("amber",T.AMBER),
                          ("cyan",T.CYAN),("muted",T.MUTED),("blue",T.BLUE)]:
            self.terminal.tag_config(tag, foreground=col)

        # ── Threat brief ─────────────────────────────────────────────────────
        brief = tk.Frame(self, bg=T.BG_PANEL,
                         highlightthickness=1, highlightbackground=T.BORDER_RED)
        brief.pack(fill="x", padx=12, pady=(8,0), ipadx=10, ipady=8)
        tk.Label(brief, text="[!] THREAT BRIEF",
                 bg=T.BG_PANEL, fg=T.RED,
                 font=("Courier New",10,"bold")).pack(anchor="w", padx=10, pady=(4,2))
        tk.Label(brief, text=self.atk.get("description",""),
                 bg=T.BG_PANEL, fg=T.TEXT,
                 font=("Courier New",10),
                 wraplength=620, justify="left").pack(anchor="w", padx=10, pady=(0,4))

        # ── Launch button ─────────────────────────────────────────────────────
        tk.Frame(self, bg=T.BORDER_PANEL, height=1).pack(fill="x", padx=12, pady=8)
        self.defend_btn = T.styled_button(
            self, "[ OPEN DEFENSE TERMINAL ]",
            self._open_defense, color=T.RED,
            font=("Courier New",12,"bold"), padx=20, pady=10)
        self.defend_btn.pack(fill="x", padx=60)

    # ── Timer ──────────────────────────────────────────────────────────────────

    def _tick(self):
        if self._breached: return
        ratio = self.time_left / self.diff["time"]
        self.timer_lbl.config(text=f"[T] {self.time_left}s")
        self.timer_fill.place(relwidth=max(0.0, ratio))
        col = T.GREEN if ratio > 0.5 else (T.AMBER if ratio > 0.25 else T.RED)
        self.timer_fill.config(bg=col)
        self.timer_lbl.config(fg=col)

        if self.time_left <= 0:
            self._do_breach(); return
        self.time_left -= 1
        self._timer_job = self.after(1000, self._tick)

    def stop_timer(self):
        if self._timer_job:  self.after_cancel(self._timer_job);  self._timer_job = None
        if self._log_job:    self.after_cancel(self._log_job);    self._log_job   = None

    def _do_breach(self):
        self._breached = True
        self.stop_timer()
        self._log_append("TIME EXPIRED — BREACH RECORDED", "red")
        self.defend_btn.config(state="disabled",
                               text="[ TIME EXPIRED — BREACH RECORDED ]",
                               fg=T.MUTED)
        self.after(1400, self.on_breach)

    # ── Log animation ──────────────────────────────────────────────────────────

    def _start_log(self):
        self.after(200, self._next_log)

    def _next_log(self):
        if self._log_idx >= len(self._log_lines): return
        line = self._log_lines[self._log_idx]; self._log_idx += 1
        parts = line.split("|") if "|" in line else ["LOG", line]
        prefix, body = parts[0], parts[-1] if len(parts) > 1 else line

        if "ALERT" in prefix:   tag = "red";   pfx = "[ALERT] "
        elif "SYSTEM" in prefix: tag = "cyan";  pfx = "[SYS]   "
        elif "AUTH" in prefix:  tag = "green"; pfx = "[AUTH]  "
        elif "NET" in prefix:   tag = "blue";  pfx = "[NET]   "
        elif "DB" in prefix:    tag = "amber"; pfx = "[DB]    "
        elif "MAIL" in prefix:  tag = "green"; pfx = "[MAIL]  "
        else:                   tag = "muted"; pfx = "[LOG]   "

        self._log_append(pfx + body, tag)
        if self._log_idx < len(self._log_lines):
            self._log_job = self.after(380, self._next_log)

    def _log_append(self, text, tag="green"):
        self.terminal.config(state="normal")
        self.terminal.insert("end", text + "\n", tag)
        self.terminal.see("end")
        self.terminal.config(state="disabled")

    def _open_defense(self):
        self.stop_timer()
        self.on_open_defense()
