# Highrise Bot

Production-ready Highrise bot (Node.js + Express + MongoDB) with WebSocket connection, XP system, admin API, and DM commands.

## Quick Start

1. Copy `.env.example` to `.env` and fill values.
2. Install dependencies: `npm install`
3. Start: `npm start`

## Key Files

- `src/index.js` - Express app & server
- `src/highrise/highriseClient.js` - WebSocket client with auto-reconnect
- `src/models/User.js` - Mongoose User model with XP system
- `src/controllers/userController.js` - DM/XP handlers (emotelist, level-up)
- `src/routes/admin.js` - Admin API routes (/users, /broadcast)
- `src/config/emotes.js` - Emotelist

## Test the DM Flow (Simulation)

Without a real Highrise connection, test the emotelist and XP logic:

```bash
node src/scripts/simulate_dm.js
```

Output will show:
- User sent `/emotelist` → bot replies with emotelist
- User sent normal message → XP awarded, user saved to DB

## Adapt to Real Highrise Protocol

See [HIGHRISE_SOCKET_SCHEMA.md](HIGHRISE_SOCKET_SCHEMA.md) for expected WS payloads. If your Highrise sends different JSON shapes, update `highriseClient.js` methods `handleEvent()` and `sendDM()`.
# 🚀 QUICK START GUIDE - ADVANCED HIGHRISE BOT

## ⚡ 5-MINUTE SETUP

### 1. Install Python (if needed)
Download from: https://python.org

### 2. Install Required Package
```bash
pip install highrise-sdk
```

### 3. Update Bot Token
Edit `run.py`:
```python
bot_configs = [
    ("party", "PARTY", "YOUR_ROOM_ID", "YOUR_BOT_TOKEN")
]
```

### 4. Start the Bot
```bash
python run.py
```

That's it! Bot is now online! 🎉

---

## 📝 FIRST COMMANDS TO TRY

```
-help              See all commands
-info              Bot information
-game trivia       Start a trivia game
-leaderboard       See rankings
-stats             Your statistics
```

---

## 🎮 FEATURES AT A GLANCE

✨ **240+ Emotes** | 🎮 **4+ Games** | 💰 **Economy System**
🔨 **Moderation** | 📢 **Events** | 🏆 **Leaderboards**
👥 **Social Features** | 🆘 **SOS System** | ⚙️ **Auto Features**

---

## 📁 FILE STRUCTURE

```
Downloads/
├── run.py                    # Bot launcher
├── party 2.py               # Main bot code
├── casinodb.py              # Database manager
├── BOT_DOCUMENTATION.md     # Full docs
├── README.md                # This file
├── FEATURES.md              # Feature list
└── DB/                      # Auto-created database
    └── 1/
        ├── user_coins.json
        ├── punishments.json
        └── ... (other data files)
```

---

## 🎯 COMMON TASKS

### Give Players Coins
```
-give @username 100
```

### Warn a Player
```
-warn @username reason here
```

### Start an Event
```
-event start
```

### See Top Players
```
-leaderboard
```

### Play a Game
```
-game trivia
```

---

## ⚠️ TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| Bot won't start | Check Python is installed, run `pip install highrise-sdk` |
| Commands not working | Use correct prefix `-`, check permissions |
| Data not saving | Ensure write access to `DB/` folder |
| Bot unresponsive | Check internet connection, restart bot |

---

## 📞 NEED HELP?

1. Read `BOT_DOCUMENTATION.md` for complete guide
2. Check `FEATURES.md` for feature details
3. Review error messages in terminal

---

**Enjoy your Advanced Highrise Bot! 🤖✨**
