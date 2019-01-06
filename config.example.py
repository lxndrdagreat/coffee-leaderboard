# This is an example of the configuration file.
# Change the settings below as needed.
import os

_basedir = os.path.abspath(os.path.dirname(__file__))


# Flask Settings
DEBUG = True  # Turns on debugging features in Flask


# Slack Settings
SLACK_API_TOKEN = "YOUR-SLACK-API-TOKEN-GOES-HERE"
SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_USERNAME = 'COFFEE LEADERBOARD'

# Database Settings
DATABASE_HOST = ''  # If left blank, default mongodb host/port settings will be used.
DATABASE_USERNAME = ''  # If left blank, app will assume no auth is used.
DATABASE_PASSWORD = ''  # If left blank, app will assume no auth is used.
