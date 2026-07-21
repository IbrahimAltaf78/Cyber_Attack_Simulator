"""
dashboard.py - Window 3: Dashboard  v3
Stats, leaderboard, history, achievements, bar chart, weakness report.
"""
import tkinter as tk
import database as db
import theme as T
import datetime


class DashboardWindow(tk.Frame):
    def __init__(self, master, user, session_summary, on_play_again, on_logout):
        super().__init__(master, bg=T.BG_DARK)
        self.user     = db.get_user_by_id(user["id"]) or user
        self.summary  = session_summary
        self.on_play_again = on_play_again
        self.on_logout     = on_logout
        self._build()

    def _build(self):
        self.pack(fill="both", expand=True)

        # ── Top bar ──────────────────────────────────────────────────────────
        top = tk.Frame(self, bg=T.BG_PANEL,
                       highlightthickness=1, highlightbackground=T.BORDER_PANEL)
        top.pack(fill="x", padx=12, pady=(12,0))
        tk.Label(top, text="[=] SOC DASHBOARD",
                 bg=T.BG_PANEL, fg=T.CYAN,
                 font=("Courier New",12,"bold")).pack(side="left",padx=12,pady=8)
        for txt,cmd,col in [("LOGOUT",self.on_logout,T.MUTED),
                             ("PLAY AGAIN",self.on_play_again,T.GREEN)]:
            tk.Button(top, text=f"[ {txt} ]", command=cmd,
                      bg=T.BG_PANEL, fg=col,
                      activebackground=T.BG_HOVER, activeforeground=col,
                      relief="flat", bd=0, cursor="hand2",
                      font=("Courier New",9,"bold"),
                      highlightthickness=0, padx=10).pack(side="right",padx=4)

        # ── Tab bar ──────────────────────────────────────────────────────────
        tab_row = tk.Frame(self, bg=T.BG_DARK)
        tab_row.pack(fill="x", padx=12, pady=(8,0))
        self.tab_btns   = {}
        self.tab_frames = {}
        for tid, label in [("stats","STATS"),("leaderboard","LEADERBOARD"),
                           ("history","LOG"),("achievements","BADGES")]:
            btn = tk.Button(tab_row, text=label,
                            command=lambda t=tid: self._switch_tab(t),
                            bg=T.BG_DARK, fg=T.MUTED,
                            activebackground=T.BG_HOVER, activeforeground=T.CYAN,
                            relief="flat", bd=0, cursor="hand2",
                            font=("Courier New",10,"bold"),
                            padx=14, pady=5,
                            highlightthickness=1, highlightbackground=T.BORDER_PANEL)
            btn.pack(side="left", padx=(0,6))
            self.tab_btns[tid] = btn

        # ── Content area ─────────────────────────────────────────────────────
        self.content = tk.Frame(self, bg=T.BG_DARK)
        self.content.pack(fill="both", expand=True, padx=12, pady=6)

        for tid in ("stats","leaderboard","history","achievements"):
            f = tk.Frame(self.content, bg=T.BG_DARK)
            self.tab_frames[tid] = f

        self._build_stats(self.tab_frames["stats"])
        self._build_leaderboard(self.tab_frames["leaderboard"])
        self._build_history(self.tab_frames["history"])
        self._build_achievements(self.tab_frames["achievements"])

        self._switch_tab("stats")

    # ── Tab switching ─────────────────────────────────────────────────────────

    def _switch_tab(self, tid):
        for t, btn in self.tab_btns.items():
            active = (t == tid)
            btn.config(fg=T.CYAN if active else T.MUTED,
                       highlightbackground=T.CYAN if active else T.BORDER_PANEL)
        for t, frame in self.tab_frames.items():
            if t == tid: frame.pack(fill="both", expand=True)
            else:        frame.pack_forget()

    # ══════════════════════════════════════════════════════════════════════════
    # STATS TAB
    # ══════════════════════════════════════════════════════════════════════════

    def _build_stats(self, parent):
        s      = self.summary
        db_st  = db.get_user_stats(self.user["id"])
        user   = self.user

        # Session result banner
        final  = s.get("final_score",0)
        passes = s.get("passes",0)
        rounds = s.get("rounds",0)
        streak = s.get("max_streak",0)

        if rounds > 0:
            perfect = passes == rounds
            col     = T.GREEN if perfect else (T.AMBER if passes > 0 else T.RED)
            banner  = "[OK] PERFECT SESSION!" if perfect else f"[!] {passes}/{rounds} DEFENDED"
        else:
            col, banner = T.MUTED, "NO SESSION DATA"

        ban_f = tk.Frame(parent, bg=T.BG_PANEL,
                         highlightthickness=1, highlightbackground=col)
        ban_f.pack(fill="x", pady=(0,8))
        tk.Label(ban_f, text=banner, bg=T.BG_PANEL, fg=col,
                 font=("Courier New",12,"bold")).pack(side="left",padx=14,pady=8)
        if rounds > 0:
            tk.Label(ban_f, text=f"Session Score: +{final}  |  Best Streak: {streak}",
                     bg=T.BG_PANEL, fg=T.GREEN,
                     font=("Courier New",10)).pack(side="right",padx=14)

        # ── Stat cards ────────────────────────────────────────────────────────
        cards_row = tk.Frame(parent, bg=T.BG_DARK)
        cards_row.pack(fill="x", pady=(0,8))
        cards = [
            ("SESSION",         str(final),                          T.GREEN),
            ("WIN RATE",        f"{s.get('win_rate',0)}%",           T.CYAN),
            ("LIFETIME",        str(user.get("total_score",0)),      T.PURPLE),
            ("RANK",            user.get("level","Rookie"),          T.AMBER),
            ("BEST STREAK",     str(user.get("best_streak",0)),      T.RED),
            ("SESSIONS",        str(db_st.get("total",0)),           T.BLUE),
        ]
        for label, val, col in cards:
            c = tk.Frame(cards_row, bg=T.BG_PANEL,
                         highlightthickness=1, highlightbackground=T.BORDER_PANEL)
            c.pack(side="left", expand=True, fill="both",
                   padx=3, ipadx=6, ipady=6)
            tk.Label(c, text=label, bg=T.BG_PANEL, fg=T.MUTED,
                     font=("Courier New",7)).pack()
            tk.Label(c, text=val, bg=T.BG_PANEL, fg=col,
                     font=("Courier New",14,"bold")).pack()

        # ── Bar chart ─────────────────────────────────────────────────────────
        T.section_header(parent,"  SESSION SCORE BY ATTACK TYPE").pack(anchor="w",pady=(0,4))
        chart_f = tk.Frame(parent, bg=T.BG_PANEL,
                           highlightthickness=1, highlightbackground=T.BORDER_PANEL)
        chart_f.pack(fill="x", pady=(0,8), ipady=4)
        canvas = tk.Canvas(chart_f, bg=T.BG_PANEL, height=100,
                           highlightthickness=0)
        canvas.pack(fill="x", padx=12, pady=6)
        canvas.bind("<Configure>", lambda e: self._draw_chart(canvas, s.get("round_log",[])))
        self.after(100, lambda: self._draw_chart(canvas, s.get("round_log",[])))

        # ── Weakness ──────────────────────────────────────────────────────────
        worst = db_st.get("weakness")
        if worst:
            labels = {"phishing":"Phishing","bruteforce":"Brute Force",
                      "ddos":"DDoS","sqli":"SQL Injection"}
            wf = tk.Frame(parent, bg="#1a0a0a",
                          highlightthickness=1, highlightbackground=T.BORDER_RED)
            wf.pack(fill="x", pady=(0,4))
            tk.Label(wf,
                     text=f"[!] Weakness: {labels.get(worst,worst)} — you fail this attack type most. Focus on it next session.",
                     bg="#1a0a0a", fg=T.RED,
                     font=("Courier New",9),
                     wraplength=600, justify="left").pack(padx=12, pady=8)

        # ── Daily challenge status ─────────────────────────────────────────────
        today = datetime.date.today().isoformat()
        dc    = db.get_daily_challenge(self.user["id"], today)
        dcf   = tk.Frame(parent, bg=T.BG_PANEL,
                         highlightthickness=1,
                         highlightbackground=T.GREEN if (dc and dc.get("completed")) else T.BORDER_AMBER)
        dcf.pack(fill="x")
        dc_txt = (f"[OK] Daily Challenge COMPLETE — Score: {dc['score']}"
                  if (dc and dc.get("completed"))
                  else "[!] Daily Challenge not completed today — Play to earn bonus +50 pts!")
        dc_col = T.GREEN if (dc and dc.get("completed")) else T.AMBER
        tk.Label(dcf, text=dc_txt, bg=T.BG_PANEL, fg=dc_col,
                 font=("Courier New",9)).pack(padx=12, pady=8)

    def _draw_chart(self, canvas, round_log):
        canvas.delete("all")
        canvas.update_idletasks()
        w = canvas.winfo_width() or 580
        types  = ["phishing","bruteforce","ddos","sqli"]
        labels = {"phishing":"Phishing","bruteforce":"Brute Force",
                  "ddos":"DDoS","sqli":"SQL Inj."}
        colors = {"phishing":T.RED,"bruteforce":T.AMBER,"ddos":T.BLUE,"sqli":T.PURPLE}
        scores = {t:0 for t in types}
        for r in round_log:
            t = r.get("attack_type","")
            if t in scores: scores[t] = max(0, scores[t]+r.get("score",0))
        mx = max(scores.values(), default=1) or 1
        bw = (w-40)//len(types)-10
        for i,t in enumerate(types):
            x   = 20 + i*((w-40)//len(types))
            bh  = int((scores[t]/mx)*70)
            ytop= 90-bh
            canvas.create_rectangle(x,ytop,x+bw,90, fill=colors[t], outline="")
            canvas.create_text(x+bw//2, ytop-8, text=str(scores[t]),
                               fill=colors[t], font=("Courier New",9,"bold"))
            canvas.create_text(x+bw//2, 98, text=labels[t],
                               fill=T.MUTED, font=("Courier New",8))

    # ══════════════════════════════════════════════════════════════════════════
    # LEADERBOARD TAB
    # ══════════════════════════════════════════════════════════════════════════

    def _build_leaderboard(self, parent):
        T.section_header(parent,"  TOP 10 — ALL-TIME LEADERBOARD").pack(anchor="w",pady=(0,6))
        f = tk.Frame(parent, bg=T.BG_PANEL,
                     highlightthickness=1, highlightbackground=T.BORDER_PANEL)
        f.pack(fill="both", expand=True)

        hdr = tk.Frame(f, bg=T.BG_INPUT)
        hdr.pack(fill="x")
        for col,w in [("#",4),("USERNAME",18),("RANK",12),
                      ("STREAK",8),("SESSIONS",8),("SCORE",8)]:
            tk.Label(hdr, text=col, bg=T.BG_INPUT, fg=T.MUTED,
                     font=("Courier New",9,"bold"), width=w,
                     anchor="w").pack(side="left",padx=6,pady=5)
        tk.Frame(f, bg=T.BORDER_PANEL, height=1).pack(fill="x")

        rows   = db.get_leaderboard(10)
        medals = {0:"(1)",1:"(2)",2:"(3)"}
        mcolors= {0:T.AMBER,1:"#c0c0c0",2:"#cd7f32"}

        for i, row in enumerate(rows):
            is_me = row["username"] == self.user["username"]
            bg    = "#0a1a0a" if is_me else T.BG_PANEL
            r     = tk.Frame(f, bg=bg)
            r.pack(fill="x")

            tk.Label(r, text=medals.get(i,str(i+1)), bg=bg,
                     fg=mcolors.get(i, T.MUTED),
                     font=("Courier New",10), width=4, anchor="w").pack(side="left",padx=6,pady=4)
            tk.Label(r, text=row["username"]+(" <YOU>" if is_me else ""),
                     bg=bg, fg=T.GREEN if is_me else T.TEXT,
                     font=("Courier New",10,"bold" if is_me else "normal"),
                     width=18, anchor="w").pack(side="left",padx=6)
            tk.Label(r, text=row.get("level","—"), bg=bg, fg=T.CYAN,
                     font=("Courier New",10), width=12, anchor="w").pack(side="left",padx=6)
            tk.Label(r, text=str(row.get("best_streak",0)), bg=bg, fg=T.AMBER,
                     font=("Courier New",10), width=8, anchor="w").pack(side="left",padx=6)
            tk.Label(r, text=str(row.get("sessions_played",0)), bg=bg, fg=T.MUTED,
                     font=("Courier New",10), width=8, anchor="w").pack(side="left",padx=6)
            tk.Label(r, text=str(row.get("total_score",0)), bg=bg, fg=T.GREEN,
                     font=("Courier New",10,"bold"), width=8, anchor="w").pack(side="left",padx=6)
            tk.Frame(f, bg=T.BORDER_PANEL, height=1).pack(fill="x")

    # ══════════════════════════════════════════════════════════════════════════
    # HISTORY TAB
    # ══════════════════════════════════════════════════════════════════════════

    def _build_history(self, parent):
        T.section_header(parent,"  ATTACK LOG — LAST 30 ROUNDS").pack(anchor="w",pady=(0,6))
        outer = tk.Frame(parent, bg=T.BG_PANEL,
                         highlightthickness=1, highlightbackground=T.BORDER_PANEL)
        outer.pack(fill="both", expand=True)

        hdr = tk.Frame(outer, bg=T.BG_INPUT)
        hdr.pack(fill="x")
        for col,w in [("#",4),("ATTACK",14),("DIFF",12),
                      ("RESULT",12),("SCORE",8),("TIME",7)]:
            tk.Label(hdr, text=col, bg=T.BG_INPUT, fg=T.MUTED,
                     font=("Courier New",9,"bold"), width=w,
                     anchor="w").pack(side="left",padx=6,pady=5)
        tk.Frame(outer, bg=T.BORDER_PANEL, height=1).pack(fill="x")

        sc   = tk.Canvas(outer, bg=T.BG_PANEL, highlightthickness=0)
        sb   = tk.Scrollbar(outer, orient="vertical", command=sc.yview,
                            bg=T.BG_DARK, troughcolor=T.BG_DARK)
        sc.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        sc.pack(fill="both", expand=True)
        inner = tk.Frame(sc, bg=T.BG_PANEL)
        sc.create_window((0,0), window=inner, anchor="nw")
        inner.bind("<Configure>", lambda e: sc.configure(scrollregion=sc.bbox("all")))

        type_labels  = {"phishing":"Phishing","bruteforce":"Brute Force",
                        "ddos":"DDoS","sqli":"SQL Inject."}
        res_colors   = {"pass":T.GREEN,"fail":T.RED,"breach":T.AMBER}
        res_symbols  = {"pass":"[OK] DEFENDED","fail":"[!!] FAILED","breach":"[X] BREACH"}

        sessions = db.get_user_sessions(self.user["id"], limit=30)
        if not sessions:
            tk.Label(inner, text="No rounds recorded yet.",
                     bg=T.BG_PANEL, fg=T.MUTED,
                     font=("Courier New",10)).pack(padx=20,pady=20)
            return

        for i,sess in enumerate(sessions):
            result = sess.get("result","—")
            r = tk.Frame(inner, bg=T.BG_PANEL)
            r.pack(fill="x")
            pts   = sess.get("score",0)
            for val,w,col in [
                (str(i+1),                                4,  T.MUTED),
                (type_labels.get(sess.get("attack_type",""),"?"), 14, T.TEXT),
                (sess.get("difficulty","?").capitalize(), 12, T.MUTED),
                (res_symbols.get(result,result),          12, res_colors.get(result,T.TEXT)),
                ((f"+{pts}" if pts>0 else str(pts)),      8,  T.GREEN if pts>0 else T.RED),
                (f"{sess.get('time_taken',0):.1f}s",      7,  T.MUTED),
            ]:
                tk.Label(r, text=val, bg=T.BG_PANEL, fg=col,
                         font=("Courier New",10,"bold" if w==12 and col!=T.MUTED else "normal"),
                         width=w, anchor="w").pack(side="left",padx=6,pady=3)
            tk.Frame(inner, bg=T.BORDER_PANEL, height=1).pack(fill="x")

    # ══════════════════════════════════════════════════════════════════════════
    # ACHIEVEMENTS TAB
    # ══════════════════════════════════════════════════════════════════════════

    def _build_achievements(self, parent):
        from achievements import ACHIEVEMENTS
        unlocked = set(db.get_user_achievements(self.user["id"]))
        done_cnt = len(unlocked)
        total    = len(ACHIEVEMENTS)

        # Progress
        T.section_header(parent, f"  ACHIEVEMENTS  {done_cnt}/{total} UNLOCKED").pack(
            anchor="w", pady=(0,4))
        bar_bg = tk.Frame(parent, bg=T.BORDER_PANEL, height=8)
        bar_bg.pack(fill="x", pady=(0,8))
        pct = done_cnt/total if total else 0
        tk.Frame(bar_bg, bg=T.PURPLE, height=8).place(relwidth=pct, height=8)

        # Grid of badges
        grid = tk.Frame(parent, bg=T.BG_DARK)
        grid.pack(fill="both", expand=True)
        col_count = 3
        for idx, (key, data) in enumerate(ACHIEVEMENTS.items()):
            done = key in unlocked
            r,c  = divmod(idx, col_count)
            card = tk.Frame(grid,
                            bg=T.BG_PANEL if done else T.BG_INPUT,
                            highlightthickness=1,
                            highlightbackground=T.PURPLE if done else T.BORDER_PANEL)
            card.grid(row=r, column=c, padx=5, pady=5, sticky="nsew", ipadx=8, ipady=6)
            grid.columnconfigure(c, weight=1)

            col = T.PURPLE if done else T.MUTED
            tk.Label(card, text=data["icon"],
                     bg=card.cget("bg"), fg=col,
                     font=("Courier New",18)).pack()
            tk.Label(card, text=data["title"],
                     bg=card.cget("bg"), fg=col,
                     font=("Courier New",10,"bold")).pack()
            tk.Label(card, text=data["desc"],
                     bg=card.cget("bg"), fg=T.MUTED if not done else col,
                     font=("Courier New",8),
                     wraplength=140, justify="center").pack(pady=(2,0))
            if done:
                tk.Label(card, text="UNLOCKED",
                         bg=card.cget("bg"), fg=T.PURPLE,
                         font=("Courier New",7,"bold")).pack()
            else:
                tk.Label(card, text="LOCKED",
                         bg=card.cget("bg"), fg=T.BORDER_PANEL,
                         font=("Courier New",7)).pack()
