# coffee_leaderboard/views/plusxp.py

from flask import Blueprint, render_template


mod = Blueprint('plusxp', __name__)


@mod.route('/')
def about_plusxp():
    return render_template('plusxp/about.html')
