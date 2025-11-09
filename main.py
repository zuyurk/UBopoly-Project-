# main.py
# Convenience launcher for the API on port 5050
from server import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True, use_reloader=False)
