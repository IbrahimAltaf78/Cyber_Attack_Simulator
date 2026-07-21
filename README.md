# Cyber-Attack Simulator & Defense Lab

**Gamified Cybersecurity Education Platform**
OSSD Final Term Project — CLO 4

---

## Description

A Python Tkinter desktop application where users play as a Security Officer and must stop incoming cyber attacks within a time limit to earn points. The game teaches real cybersecurity concepts through interactive, hands-on defense challenges.

---

## Features

### Window 1 — Attack Lab
- Live scrolling terminal-style attack logs
- 30/20/12 second countdown timer (per difficulty)
- 4 attack types: Phishing, Brute Force, DDoS, SQL Injection
- Animated log feed with color-coded severity

### Window 2 — Defense Terminal
| Attack        | Widget                   | Action                           |
| ------------- | ------------------------ | -------------------------------- |
| Phishing      | Clickable email elements | Click the malicious link         |
| Brute Force   | Entry + Button           | Type attacker IP and block       |
| DDoS          | Allow/Block buttons      | Classify each traffic source     |
| SQL Injection | Radio buttons            | Choose correct parameterized fix |

**Scoring:**
- Correct + fast: +100 pts
- Correct + slow: +50 pts
- Wrong answer: −10/25/50 pts (by difficulty)
- Hint used: −10/20/40 pts
- Time runs out: 0 pts, BREACH recorded

### Window 3 — Dashboard
- Personal stats: score, win rate, sessions, breaches
- Bar chart of score per attack type (drawn with Canvas)
- Leaderboard (Top 10 players, Treeview-style)
- Full attack history with results and scores
- Weakness detection: shows which attack type you fail most

---

## Technologies Used

| Technology   | Purpose                           |
| ------------ | --------------------------------- |
| Python 3.x   | Core language                     |
| Tkinter      | All GUI windows                   |
| SQLite3      | Database (built-in)               |
| hashlib      | Password hashing (SHA-256 + salt) |
| Git + GitHub | Version control                   |

---

## How to Run

### Requirements
- Python 3.7 or higher
- Tkinter (usually included with Python)

### On Windows
```bash
python main.py
```

### On Linux/macOS
```bash
# If tkinter not found:
sudo apt-get install python3-tk   # Ubuntu/Debian
brew install python-tk            # macOS

python3 main.py
```

---

## Project Structure

```
cyber-attack-simulator/
├── main.py               ← App entry point (run this)
├── login_screen.py       ← Login + Register UI
├── home_screen.py        ← Difficulty selection
├── attack_lab.py         ← Window 1: Attack Lab
├── defense_screen.py     ← Window 2: Defense Terminal
├── dashboard.py          ← Window 3: Dashboard
├── game_controller.py    ← Round flow, answer validation
├── score_manager.py      ← Scoring rules per difficulty
├── database.py           ← SQLite setup + all queries
├── auth.py               ← Login/register logic + hashing
├── theme.py              ← Colors, fonts, style helpers
├── requirements.txt
├── README.md
└── cyber_simulator.db    ← Auto-created on first run
```

---

## Team Division

| Member        | Window                      | Files                                    |
| ------------- | --------------------------- | ---------------------------------------- |
| Leader        | Home + Login                | main.py, login_screen.py, home_screen.py |
| Member 2      | Window 1 — Attack Lab       | attack_lab.py                            |
| Member 3      | Window 2 — Defense Terminal | defense_screen.py                        |
| Member 4      | Window 3 — Dashboard        | dashboard.py                             |
| Backend Dev 1 | Database                    | database.py, auth.py                     |
| Backend Dev 2 | Game Logic                  | game_controller.py, score_manager.py     |

---

## Database Schema

```sql
users         (id, username, password_hash, total_score, level, sessions_played)
attacks       (id, attack_type, description, correct_answer, hint, difficulty, log_lines)
game_sessions (id, user_id, attack_type, result, score, time_taken, difficulty)
logs          (id, user_id, timestamp, attack_type, action_taken, outcome)
```

---

## GitHub Workflow

| Branch             | Purpose                       |
| ------------------ | ----------------------------- |
| main               | Final submission only         |
| dev                | Merge all features here first |
| feature/login      | Login + Register screens      |
| feature/attack-lab | Window 1                      |
| feature/defense    | Window 2                      |
| feature/dashboard  | Window 3                      |
| feature/database   | SQLite models                 |
| feature/game-logic | Game controller + scoring     |

**Rules:**
- Never commit directly to `main`
- Pull from `dev` every day before working
- Clear commit messages: `Added timer to attack lab window`
- Create Pull Request → leader reviews → merge to `dev`
- Add `cyber_simulator.db` and `__pycache__/` to `.gitignore`

---

*OSSD Final Term 2026 — Cybersecurity Department*
