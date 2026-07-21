"""
main.py - App entry point and screen manager  v3
Cyber-Attack Simulator & Defense Lab
"""
import tkinter as tk
from tkinter import messagebox
import database as db
import theme as T


class CyberSimApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Cyber-Attack Simulator & Defense Lab  v3")
        self.root.geometry("860x620")
        self.root.minsize(800, 560)
        self.root.configure(bg=T.BG_DARK)
        self.root.resizable(True, True)

        self.current_user   = None
        self.game_controller= None
        self.current_frame  = None

        db.init_db()
        self._show_login()
        self.root.mainloop()

    # ── Clear ─────────────────────────────────────────────────────────────────

    def _clear(self):
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    # ── Login ─────────────────────────────────────────────────────────────────

    def _show_login(self):
        self._clear()
        from login_screen import LoginScreen
        self.current_frame = LoginScreen(self.root, on_login_success=self._on_login)

    def _on_login(self, user):
        self.current_user = user
        self._show_home()

    # ── Home ──────────────────────────────────────────────────────────────────

    def _show_home(self):
        self._clear()
        self.current_user = db.get_user(self.current_user["username"]) or self.current_user
        from home_screen import HomeScreen
        self.current_frame = HomeScreen(
            self.root, user=self.current_user,
            on_start_game=self._start_game,
            on_view_dashboard=self._show_dashboard_nosession,
            on_logout=self._logout,
        )

    # ── Game ──────────────────────────────────────────────────────────────────

    def _start_game(self, difficulty):
        from game_controller import GameController
        self.game_controller = GameController(
            user_id=self.current_user["id"], difficulty=difficulty)
        self.game_controller.start_session()
        self._next_round()

    def _next_round(self):
        self._clear()
        gc = self.game_controller
        if gc.session_complete():
            # Check achievements before showing dashboard
            self._check_achievements()
            # If daily, save daily result
            if gc.is_daily:
                gc.save_daily_result()
                # Bonus points for completing daily
                db.update_user_score(self.current_user["id"], 50)
            self._show_dashboard()
            return

        atk = gc.get_current_attack()
        gc.start_round_timer()

        from attack_lab import AttackLabWindow
        from score_manager import DIFFICULTY_SETTINGS
        diff_cfg = DIFFICULTY_SETTINGS[gc.difficulty]

        self.current_frame = AttackLabWindow(
            self.root,
            attack_data=atk,
            round_num=gc.current_index + 1,
            total_rounds=gc.ATTACKS_PER_SESSION,
            difficulty_settings=diff_cfg,
            on_open_defense=self._show_defense,
            on_breach=self._on_breach,
            current_streak=gc.score_mgr.current_streak,
            session_score=gc.score_mgr.session_score,
        )

    def _show_defense(self):
        self._clear()
        gc  = self.game_controller
        atk = gc.get_current_attack()
        from defense_screen import DefenseScreen
        self.current_frame = DefenseScreen(
            self.root, attack_data=atk,
            game_controller=gc,
            on_submit=lambda r: None,
            on_next_round=self._next_round,
        )

    def _on_breach(self):
        self.game_controller.submit_breach()
        self._next_round()

    # ── Achievements check ────────────────────────────────────────────────────

    def _check_achievements(self):
        try:
            import achievements as A
            gc      = self.game_controller
            summary = gc.get_session_summary()
            user    = db.get_user_by_id(self.current_user["id"]) or self.current_user
            db_stats= db.get_user_stats(self.current_user["id"])
            newly   = A.check_achievements(self.current_user["id"], summary, db_stats, user)
            if newly:
                names = [A.ACHIEVEMENTS[k]["title"] for k in newly if k in A.ACHIEVEMENTS]
                if names:
                    msg = "Achievement(s) Unlocked!\n\n" + "\n".join(f"  {n}" for n in names)
                    messagebox.showinfo("New Achievement!", msg)
        except Exception:
            pass

    # ── Dashboard ─────────────────────────────────────────────────────────────

    def _show_dashboard(self):
        self._clear()
        self.current_user = db.get_user(self.current_user["username"]) or self.current_user
        summary = self.game_controller.get_session_summary() if self.game_controller else {}
        from dashboard import DashboardWindow
        self.current_frame = DashboardWindow(
            self.root, user=self.current_user,
            session_summary=summary,
            on_play_again=self._show_home,
            on_logout=self._logout,
        )

    def _show_dashboard_nosession(self):
        self._clear()
        self.current_user = db.get_user(self.current_user["username"]) or self.current_user
        from dashboard import DashboardWindow
        self.current_frame = DashboardWindow(
            self.root, user=self.current_user,
            session_summary={},
            on_play_again=self._show_home,
            on_logout=self._logout,
        )

    # ── Logout ────────────────────────────────────────────────────────────────

    def _logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.current_user    = None
            self.game_controller = None
            self._show_login()


if __name__ == "__main__":
    CyberSimApp()
