🎲 UBHACKOPOLY
UBHACKOPOLY is a Monopoly-style digital board game themed around the University at Buffalo.
It uses a Flask backend for game logic and a JavaScript frontend for an interactive web UI.

🚀 Overview


Backend: Python + Flask REST API


Frontend: HTML, CSS, JavaScript


Data format: JSON over HTTP


Features: dice rolls, turns, property buying, live player balances



🧠 Backend (Flask)


Manages full game state:


Players, balances, positions, properties




Main endpoints:


GET /state – return current game state


POST /roll – roll dice and move active player


POST /buy – attempt to buy current property


POST /end_turn – advance to next player




Returns structured JSON and uses CORS for browser access



🖥️ Frontend (HTML/CSS/JS)


Neon-style Monopoly board built with CSS grid


Player sidebar with live money updates and active player highlight


Controls:


🎲 Roll Dice


💰 Buy Property


🎟️ Use Jail Card (placeholder)


➡️ End Turn




Uses fetch() to call Flask endpoints and update the UI based on JSON responses


Popup notifications for actions and feedback



🏁 How to Run


Install dependencies:


pip install flask flask-cors



Start the backend:


python server.py

Server runs at:
http://127.0.0.1:5000/


Open the frontend:




Open page3.html in your browser
or use a simple static server (like VS Code Live Server)



📁 Project Structure
UBHackopoly/
  server.py       # Flask API and game engine
  page1.html      # Start screen (player count)
  page2.html      # Player setup and piece selection
  page3.html      # Main board and gameplay UI
  Images/         # Player tokens and assets
  README.md


🔧 Technical Summary


Frontend sends actions (roll, buy, end turn) via fetch()


Flask updates game state in memory and returns JSON


UI re-renders player balances, active player, and notifications from that JSON


Backend = rules and state
Frontend = visuals and interaction

🔮 Future Ideas


Rent and house/hotel system


Chance and Community Chest logic


Trading and auctions


Jail and bail rules


Animated piece movement


Online multiplayer and save/load support

