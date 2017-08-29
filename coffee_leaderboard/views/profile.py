# coffee_leaderboard/views/profile.py

from flask import Blueprint, render_template, request, redirect
import requests
import random
import json
import datetime
import operator
import pygal
from coffee_leaderboard.database import db

mod = Blueprint('profile', __name__)


@mod.route('/')
def profile_redirect():
	return redirect('/')


@mod.route('/<user_slug>')
def user_profile(user_slug):
	return render_template('profile/index.html', username=user_slug)
