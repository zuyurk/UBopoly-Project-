🎲 UBHACKOPOLY
A fully interactive Monopoly-style game built with Flask, JavaScript, and a custom game engine.

UBHackopoly is a digital board game inspired by Monopoly and themed around the University at Buffalo. It features a Flask backend, a dynamic JavaScript frontend, and a complete set of APIs that power dice rolls, property purchases, turn handling, and full game state syncing.

🚀 Features
🧠 Backend (Flask)

REST API using Flask + JSON

Centralized state for:

Players

Positions

Balances

Properties owned

Endpoints:

/state → fetch full game state

/roll → roll dice & move active player

/buy → attempt to purchase a property

/end_turn → move to the next player

Automatic CORS support for browser frontend

Clean JSON responses with error handling

🖥️ Frontend (HTML/CSS/JS)

Neon-style responsive UI

Interactive digital game board

Player sidebar that updates live

Roll, Buy, End Turn, Use Jail Card controls

Popup notifications for all actions

Player highlighting and animated UI feedback

Full state synchronization with backend APIs

🎮 Game Logic

Turn-based sequence

Dice roll movement

Money management

Property purchasing rules

Jail card placeholder system

Expandable for rent, cards, trades, and more

📡 API Overview
GET /state

Returns current full game state.

POST /roll

Rolls dice and moves the active player.

POST /buy

Attempts to buy the property the active player is currently on.

POST /end_turn

Advances turn to the next player.

All APIs return JSON similar to:

{
  "message": "Player 1 bought Cooke!",
  "players": [...],
  "active_player": 0
}

🏁 How to Run the Project
1. Install dependencies
pip install flask flask-cors

2. Start the backend
python server.py


Runs at:

http://127.0.0.1:5000/

3. Open the frontend

Open page3.html directly or with VSCode Live Server.

📁 Project Structure
UBHackopoly/
│
├── server.py           # Flask REST API & game state engine
├── page1.html          # Start screen
├── page2.html          # Player setup
├── page3.html          # Main game board UI
├── Images/             # Tokens or design assets
└── README.md

🧑‍💻 Technical Summary

The frontend uses JavaScript’s fetch() API to send actions (roll, buy, end turn) to the Flask backend.
Flask modifies the game engine in memory and returns JSON updates.
The browser then updates the UI instantly based on the API response.

This architecture cleanly separates responsibilities:

Flask = game rules + state

Frontend = visuals + user interactions

🛠️ Future Features (Planned)

Rent system based on tile ownership

Chance & Community Chest effects

Trading system

Auctions

Jail / bail mechanics

Animated player movement

Online multiplayer using WebSockets

Save / load game system
