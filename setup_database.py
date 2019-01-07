from coffee_leaderboard.database import init_db
from tortoise import run_async


if __name__ == '__main__':
    run_async(init_db(True))
