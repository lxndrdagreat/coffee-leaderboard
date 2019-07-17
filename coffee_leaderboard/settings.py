from starlette.config import Config

config = Config('.env')

DEBUG = config('DEBUG', cast=bool, default=False)

DATABASE_URL = config('DATABASE_URL', default=None)
DATABASE_USER = config('DATABASE_USER', default=None)
DATABASE_PASSWORD = config('DATABASE_PASSWORD', default=None)

STATIC_FILES_PATH = config('STATIC_FILES_PATH', default='coffee_leaderboard/static')

SLACK_TOKEN = config('SLACK_TOKEN', default=None)
SLACK_CLIENT_ID = config('SLACK_CLIENT_ID', default=None)
SLACK_CLIENT_SECRET = config('SLACK_CLIENT_SECRET', default=None)
SLACK_SIGNING_SECRET = config('SLACK_SIGNING_SECRET', default=None)
SLACK_COFFEE_CHANNEL_ID = config('SLACK_COFFEE_CHANNEL_ID', default=None)
SLACK_WEBHOOK_URL = config('SLACK_WEBHOOK_URL', default=None)

APP_TOKEN_PEPPER = config('TOKEN_PEPPER', default=None)
