from starlette.config import Config

config = Config('.env')

DEBUG = config('DEBUG', cast=bool, default=False)

DATABASE_URL = config('DATABASE_URL', default=None)
DATABASE_USER = config('DATABASE_USER', default=None)
DATABASE_PASSWORD = config('DATABASE_PASSWORD', default=None)

STATIC_FILES_PATH = config('STATIC_FILES_PATH', default='coffee_leaderboard/static')
