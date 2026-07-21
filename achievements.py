"""
achievements.py - Achievement / badge system
Cyber-Attack Simulator & Defense Lab
"""

ACHIEVEMENTS = {
    "first_blood":      {"title": "First Blood",        "desc": "Complete your first round",              "icon": "[*]"},
    "perfect_session":  {"title": "Perfect Session",    "desc": "Defend all 4 attacks in one session",   "icon": "[OK]"},
    "speed_demon":      {"title": "Speed Demon",        "desc": "Answer correctly in under 5 seconds",   "icon": "[T]"},
    "no_hints":         {"title": "No Crutches",        "desc": "Complete a session without any hints",  "icon": "[^]"},
    "expert_cleared":   {"title": "Elite Defender",     "desc": "Complete a full Expert session",        "icon": "[E]"},
    "century":          {"title": "Century Club",       "desc": "Reach 100 total score",                 "icon": "[C]"},
    "high_scorer":      {"title": "High Scorer",        "desc": "Reach 500 total score",                 "icon": "[H]"},
    "legend":           {"title": "Legend",             "desc": "Reach 1000 total score",                "icon": "[L]"},
    "phish_hunter":     {"title": "Phish Hunter",       "desc": "Correctly identify 5 phishing attacks", "icon": "[~]"},
    "firewall":         {"title": "The Firewall",       "desc": "Block 5 brute force attacks",           "icon": "[K]"},
    "flood_control":    {"title": "Flood Control",      "desc": "Stop 5 DDoS attacks",                   "icon": "[W]"},
    "sql_master":       {"title": "SQL Master",         "desc": "Fix 5 SQL injection vulnerabilities",   "icon": "[D]"},
    "comeback":         {"title": "Comeback King",      "desc": "Score 100+ after a breach",             "icon": "[!]"},
    "streak_3":         {"title": "On Fire",            "desc": "3 correct answers in a row",            "icon": "[3]"},
    "streak_5":         {"title": "Unstoppable",        "desc": "5 correct answers in a row",            "icon": "[5]"},
}


def check_achievements(user_id, session_summary, db_stats, user):
    """
    Compare session + lifetime stats against achievement criteria.
    Returns list of newly unlocked achievement keys.
    """
    import database as db
    already = set(db.get_user_achievements(user_id))
    newly_unlocked = []

    round_log  = session_summary.get("round_log", [])
    passes     = session_summary.get("passes", 0)
    rounds     = session_summary.get("rounds", 0)
    final_sc   = session_summary.get("final_score", 0)
    diff       = session_summary.get("difficulty", "beginner")
    hint_used  = session_summary.get("hint_used_any", False)
    total_sc   = user.get("total_score", 0)

    def unlock(key):
        if key not in already:
            newly_unlocked.append(key)
            db.unlock_achievement(user_id, key)

    # First round ever
    if db_stats.get("total", 0) >= 1:
        unlock("first_blood")

    # Perfect session
    if rounds == 4 and passes == 4:
        unlock("perfect_session")

    # Speed demon — any correct answer under 5s
    for r in round_log:
        if r.get("result") == "pass" and r.get("time_taken", 99) <= 5:
            unlock("speed_demon")
            break

    # No hints full session
    if rounds == 4 and not hint_used:
        unlock("no_hints")

    # Expert cleared
    if diff == "expert" and rounds == 4 and passes == 4:
        unlock("expert_cleared")

    # Score milestones
    if total_sc >= 100:  unlock("century")
    if total_sc >= 500:  unlock("high_scorer")
    if total_sc >= 1000: unlock("legend")

    # Per-type counts from DB
    for atype, key in [("phishing","phish_hunter"),("bruteforce","firewall"),
                       ("ddos","flood_control"),("sqli","sql_master")]:
        cnt = db_stats.get(f"{atype}_wins", 0)
        if cnt >= 5:
            unlock(key)

    # Comeback — had a breach but session score >= 100
    had_breach = any(r.get("result") == "breach" for r in round_log)
    if had_breach and final_sc >= 100:
        unlock("comeback")

    # Streaks
    streak = 0
    max_streak = 0
    for r in round_log:
        if r.get("result") == "pass":
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 0
    if max_streak >= 3: unlock("streak_3")
    if max_streak >= 5: unlock("streak_5")

    return newly_unlocked
