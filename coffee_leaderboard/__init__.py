from flask import Flask, redirect, render_template, request

app = Flask(__name__)
app.config.from_object('config')


# set up views
from coffee_leaderboard.views import leaderboard
from coffee_leaderboard.views import profile

app.register_blueprint(leaderboard.mod)
app.register_blueprint(profile.mod, url_prefix='/profile')
