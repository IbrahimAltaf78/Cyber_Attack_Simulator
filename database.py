"""
database.py - SQLite setup and all query functions
Cyber-Attack Simulator & Defense Lab  (v3 - advanced)
"""

import sqlite3
import os

DB_FILE = "cyber_simulator.db"


def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        total_score INTEGER DEFAULT 0,
        level TEXT DEFAULT 'Rookie',
        sessions_played INTEGER DEFAULT 0,
        current_streak INTEGER DEFAULT 0,
        best_streak INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS game_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        attack_type TEXT NOT NULL,
        result TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        time_taken REAL DEFAULT 0,
        difficulty TEXT NOT NULL,
        played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        attack_type TEXT NOT NULL,
        action_taken TEXT NOT NULL,
        outcome TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        achievement_key TEXT NOT NULL,
        unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, achievement_key),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS daily_challenge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        challenge_date TEXT NOT NULL,
        score INTEGER DEFAULT 0,
        completed INTEGER DEFAULT 0,
        UNIQUE(user_id, challenge_date),
        FOREIGN KEY (user_id) REFERENCES users(id)
    )""")

    conn.commit()
    conn.close()


# ── User ───────────────────────────────────────────────────────────────────────

def create_user(username, password_hash):
    conn = get_connection()
    try:
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?,?)",
                     (username, password_hash))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def get_user(username):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    conn = get_connection()
    row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_user_score(user_id, points_delta):
    conn = get_connection()
    conn.execute(
        "UPDATE users SET total_score=MAX(0,total_score+?), sessions_played=sessions_played+1 WHERE id=?",
        (points_delta, user_id))
    row = conn.execute("SELECT total_score FROM users WHERE id=?", (user_id,)).fetchone()
    if row:
        conn.execute("UPDATE users SET level=? WHERE id=?",
                     (_get_level(row["total_score"]), user_id))
    conn.commit()
    conn.close()


def update_streak(user_id, correct):
    conn = get_connection()
    row = conn.execute("SELECT current_streak, best_streak FROM users WHERE id=?",
                       (user_id,)).fetchone()
    if row:
        cur = (row["current_streak"] + 1) if correct else 0
        best = max(row["best_streak"], cur)
        conn.execute("UPDATE users SET current_streak=?, best_streak=? WHERE id=?",
                     (cur, best, user_id))
        conn.commit()
    conn.close()


def _get_level(score):
    if score < 100:   return "Rookie"
    if score < 300:   return "Analyst"
    if score < 700:   return "Defender"
    if score < 1500:  return "Expert"
    if score < 3000:  return "Elite"
    return "Legend"


# ── Sessions ───────────────────────────────────────────────────────────────────

def save_session(user_id, attack_type, result, score, time_taken, difficulty):
    conn = get_connection()
    conn.execute("""INSERT INTO game_sessions
        (user_id,attack_type,result,score,time_taken,difficulty)
        VALUES (?,?,?,?,?,?)""",
        (user_id, attack_type, result, score, time_taken, difficulty))
    conn.commit()
    conn.close()


def get_user_sessions(user_id, limit=30):
    conn = get_connection()
    rows = conn.execute("""SELECT * FROM game_sessions WHERE user_id=?
        ORDER BY played_at DESC LIMIT ?""", (user_id, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_stats(user_id):
    conn = get_connection()
    total   = conn.execute("SELECT COUNT(*) as c FROM game_sessions WHERE user_id=?",
                            (user_id,)).fetchone()["c"]
    wins    = conn.execute("SELECT COUNT(*) as c FROM game_sessions WHERE user_id=? AND result='pass'",
                            (user_id,)).fetchone()["c"]
    breaches= conn.execute("SELECT COUNT(*) as c FROM game_sessions WHERE user_id=? AND result='breach'",
                            (user_id,)).fetchone()["c"]
    best_t  = conn.execute("SELECT MIN(time_taken) as t FROM game_sessions WHERE user_id=? AND result='pass'",
                            (user_id,)).fetchone()["t"]

    weakness, type_wins = {}, {}
    for t in ["phishing","bruteforce","ddos","sqli"]:
        fails = conn.execute("SELECT COUNT(*) as c FROM game_sessions WHERE user_id=? AND attack_type=? AND result!='pass'",
                              (user_id,t)).fetchone()["c"]
        tw    = conn.execute("SELECT COUNT(*) as c FROM game_sessions WHERE user_id=? AND attack_type=? AND result='pass'",
                              (user_id,t)).fetchone()["c"]
        weakness[t] = fails
        type_wins[f"{t}_wins"] = tw

    conn.close()
    win_rate = round(wins/total*100) if total>0 else 0
    worst    = max(weakness, key=weakness.get) if any(weakness.values()) else None
    return {"total":total,"wins":wins,"breaches":breaches,"win_rate":win_rate,
            "weakness":worst,"best_time":best_t, **type_wins}


def get_leaderboard(limit=10):
    conn = get_connection()
    rows = conn.execute("""SELECT username,total_score,level,sessions_played,best_streak
        FROM users ORDER BY total_score DESC LIMIT ?""", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Logs ───────────────────────────────────────────────────────────────────────

def add_log(user_id, attack_type, action_taken, outcome):
    conn = get_connection()
    conn.execute("INSERT INTO logs (user_id,attack_type,action_taken,outcome) VALUES (?,?,?,?)",
                 (user_id, attack_type, action_taken, outcome))
    conn.commit()
    conn.close()


# ── Achievements ───────────────────────────────────────────────────────────────

def get_user_achievements(user_id):
    conn = get_connection()
    rows = conn.execute("SELECT achievement_key FROM achievements WHERE user_id=?",
                        (user_id,)).fetchall()
    conn.close()
    return [r["achievement_key"] for r in rows]


def unlock_achievement(user_id, key):
    conn = get_connection()
    try:
        conn.execute("INSERT OR IGNORE INTO achievements (user_id,achievement_key) VALUES (?,?)",
                     (user_id, key))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


# ── Daily Challenge ────────────────────────────────────────────────────────────

def get_daily_challenge(user_id, date_str):
    conn = get_connection()
    row = conn.execute("SELECT * FROM daily_challenge WHERE user_id=? AND challenge_date=?",
                       (user_id, date_str)).fetchone()
    conn.close()
    return dict(row) if row else None


def save_daily_challenge(user_id, date_str, score, completed):
    conn = get_connection()
    conn.execute("""INSERT INTO daily_challenge (user_id,challenge_date,score,completed)
        VALUES (?,?,?,?) ON CONFLICT(user_id,challenge_date)
        DO UPDATE SET score=MAX(score,excluded.score), completed=excluded.completed""",
        (user_id, date_str, score, 1 if completed else 0))
    conn.commit()
    conn.close()
