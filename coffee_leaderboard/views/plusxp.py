# coffee_leaderboard/views/plusxp.py

from flask import Blueprint, render_template
from coffee_leaderboard.utils import XP_TABLE


mod = Blueprint('plusxp', __name__)


@mod.route('/')
def about_plusxp():
    return render_template('plusxp/about.html', xp_table=XP_TABLE)
