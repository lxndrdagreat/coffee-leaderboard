# coffee_leaderboard/views/profile.py

from flask import Blueprint, render_template, request, redirect
# import requests
import random
import json
import datetime
import operator
import pygal
from coffee_leaderboard.database import UserProfile

mod = Blueprint('profile', __name__)


@mod.route('/')
def profile_redirect():
	# return redirect('/')
	# TODO: temporary. remove this
	do_wipe = request.values.get('wipe', 0, type=int)
	print(f'do_wipe: {do_wipe}')
	if do_wipe == 1:
		result = UserProfile.wipe()
		return 'wipe complete'

	all_users = list(map(lambda x: x.as_dict(), [user for user in UserProfile.find({})]))
	return json.dumps(all_users)


@mod.route('/<user_slug>')
def user_profile(user_slug):
	user = UserProfile.find_one({'username': user_slug})

	# if not user:
	# 	# test creation
	# 	# TODO remove this test!
	# 	user = UserProfile()
	# 	user.username = user_slug
	# 	print(f'PRE-SAVE: {user.as_dict()}')		
	# 	user.save()
	# 	print(f'POST-SAVE: {user.as_dict()}')

	return render_template('profile/index.html', user=user)

# TODO: remove?
@mod.route('/<user_slug>/delete')
def user_profile_delete(user_slug):
	user = UserProfile.find_one({'username': user_slug})

	if not user:
		return 'No user to delete'

	result = user.delete()

	return result
