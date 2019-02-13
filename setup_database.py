from coffee_leaderboard.database import init_db, seed_test_data
from tortoise import run_async


if __name__ == '__main__':
    run_async(init_db(True))
    # run_async(seed_test_data())
