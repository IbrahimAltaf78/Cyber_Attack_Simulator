"""
game_controller.py - Orchestrates sessions, daily challenges, answer validation.
Cyber-Attack Simulator & Defense Lab  v3
"""
import random, time, datetime
import database as db
from score_manager import ScoreManager, DIFFICULTY_SETTINGS
import questions as Q


class GameController:
    ATTACKS_PER_SESSION = 4
    ATTACK_TYPES = ["phishing","bruteforce","ddos","sqli"]

    def __init__(self, user_id, difficulty="beginner"):
        self.user_id          = user_id
        self.difficulty       = difficulty
        self.score_mgr        = ScoreManager(difficulty)
        self.attack_queue     = []
        self.current_index    = 0
        self.round_start_time = None
        self.hint_used_this_round = False
        self._used_ids        = []
        self.is_daily         = (difficulty == "daily")

    # ── Session ────────────────────────────────────────────────────────────────

    def start_session(self):
        self._used_ids = []
        types = self.ATTACK_TYPES[:]
        random.shuffle(types)
        selected = []
        diff = "intermediate" if self.is_daily else self.difficulty
        for atype in types:
            q = Q.get_question(atype, diff, exclude_ids=self._used_ids)
            if q:
                q["attack_type"] = atype
                selected.append(q)
                self._used_ids.append(q["id"])
        self.attack_queue  = selected[:self.ATTACKS_PER_SESSION]
        self.current_index = 0
        self.score_mgr.reset()

    def session_complete(self):
        return self.current_index >= len(self.attack_queue)

    # ── Round ──────────────────────────────────────────────────────────────────

    def get_current_attack(self):
        if self.session_complete(): return None
        return self.attack_queue[self.current_index]

    def start_round_timer(self):
        self.round_start_time     = time.time()
        self.hint_used_this_round = False

    def elapsed_time(self):
        return time.time() - self.round_start_time if self.round_start_time else 0.0

    def use_hint(self):
        granted = self.score_mgr.use_hint()
        if granted: self.hint_used_this_round = True
        return granted

    def time_limit(self):
        return DIFFICULTY_SETTINGS[self.difficulty]["time"]

    # ── Answer ─────────────────────────────────────────────────────────────────

    def submit_answer(self, answer):
        atk = self.get_current_attack()
        if not atk:
            return {"correct":False,"points":0,"result":"error","message":"No round.","explanation":""}

        elapsed = self.elapsed_time()
        correct = self._validate(atk, answer)
        pts     = self.score_mgr.apply_round(
                      atk["attack_type"], correct, elapsed, self.hint_used_this_round)
        streak  = self.score_mgr.current_streak

        res_str = "pass" if correct else "fail"
        db.save_session(self.user_id, atk["attack_type"], res_str, pts,
                        round(elapsed,1), self.difficulty)
        db.add_log(self.user_id, atk["attack_type"], str(answer)[:120], res_str)
        db.update_user_score(self.user_id, pts)
        db.update_streak(self.user_id, correct)

        self.current_index += 1

        explain = atk.get("explanation","")
        if correct:
            combo = f"  x{min(streak,5)} COMBO!" if streak >= 2 else ""
            msg   = f"[OK] DEFENSE SUCCESSFUL  +{pts} pts{combo}"
        else:
            msg   = f"[!!] WRONG  {pts} pts  |  {explain}"

        return {"correct":correct,"points":pts,"result":res_str,
                "message":msg,"explanation":explain,"streak":streak}

    def submit_breach(self):
        atk = self.get_current_attack()
        if not atk: return
        self.score_mgr.apply_round(atk["attack_type"], False, 999, False, breach=True)
        db.save_session(self.user_id, atk["attack_type"], "breach", 0, 999, self.difficulty)
        db.add_log(self.user_id, atk["attack_type"], "TIMEOUT", "breach")
        db.update_streak(self.user_id, False)
        self.current_index += 1

    # ── Validation ─────────────────────────────────────────────────────────────

    def _validate(self, atk, answer):
        t = atk["attack_type"]
        if t == "phishing":
            return str(answer) == "malicious_link"
        if t == "bruteforce":
            ip = atk.get("attacker_ip", atk.get("correct_answer",""))
            return str(answer).strip() == ip.strip()
        if t == "ddos":
            expected = {ip:("block" if f else "allow") for ip,_,f in atk.get("traffic",[])}
            return isinstance(answer,dict) and all(answer.get(ip)==a for ip,a in expected.items())
        if t == "sqli":
            return str(answer) == "parameterized_queries"
        return False

    def get_ddos_entries(self):
        atk = self.get_current_attack()
        if atk and atk["attack_type"]=="ddos":
            return [(ip,"block" if f else "allow") for ip,_,f in atk.get("traffic",[])]
        return []

    # ── Daily challenge ────────────────────────────────────────────────────────

    def save_daily_result(self):
        today = datetime.date.today().isoformat()
        completed = self.score_mgr.rounds_passed == self.ATTACKS_PER_SESSION
        db.save_daily_challenge(self.user_id, today,
                                self.score_mgr.session_score, completed)

    # ── Summary ────────────────────────────────────────────────────────────────

    def get_session_summary(self):
        return {
            "final_score": self.score_mgr.session_score,
            "win_rate":    self.score_mgr.get_win_rate(),
            "rounds":      self.score_mgr.rounds_played,
            "passes":      self.score_mgr.rounds_passed,
            "round_log":   self.score_mgr.round_log,
            "max_streak":  self.score_mgr.max_streak,
            "difficulty":  self.difficulty,
            "hint_used_any": self.score_mgr.hint_used_any,
        }
