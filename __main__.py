# __main__.py
# This is for local development only.

from coffee_leaderboard import app
import uvicorn


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1', port=4444)
