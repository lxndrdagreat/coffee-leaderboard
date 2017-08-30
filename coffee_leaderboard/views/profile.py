# coffee_leaderboard/views/profile.py

from flask import Blueprint, render_template, request, redirect
# import requests
import random
import json
import datetime
import operator
import pygal
from coffee_leaderboard.database import UserProfile, CoffeeEntry
from coffee_leaderboard.utils import XP_TABLE, calculate_xp_history, calculate_user_level


mod = Blueprint('profile', __name__)


@mod.route('/')
def profile_redirect():
    # return redirect('/')
    # TODO: temporary. remove this
    do_wipe = request.values.get('wipe', 0, type=int)
    
    if do_wipe == 1:
        result = UserProfile.wipe()
        return 'wipe complete'

    all_users = list(map(lambda x: x.as_dict(), [user for user in UserProfile.find({})]))
    return json.dumps(all_users)


@mod.route('/<user_slug>')
def user_profile(user_slug):
    user = UserProfile.find_one({'username': user_slug})

    if not user:
        # test creation
        # TODO remove this test!
        if len(CoffeeEntry.find({'user': user_slug})) > 0:
            # User has entries, so create profile object
            user = UserProfile()
            user.username = user_slug          
            user.save()
            # redirect to recalc page
            return redirect(f'/profile/{user_slug}/recalc')

    if not user:
        return redirect('/')

    entries = CoffeeEntry.find({'user': user.username})

    # get average day consumption
    day_stats = [{},{},{},{},{},{},{}]
    day_stats_totals = [0, 0, 0, 0, 0, 0, 0]
    for entry in entries:
        # get the date from the datetime as a string
        dt = entry.date.date().isoformat()
        weekday = entry.date.weekday()
        if not dt in day_stats[weekday]:
            day_stats[weekday][dt] = 0

        day_stats[weekday][dt] += 1
        day_stats_totals[weekday] += 1

    temp = {
        'Monday': int(day_stats_totals[0] / len(day_stats[0])) if len(day_stats[0]) > 0 else 0,
        'Tuesday': int(day_stats_totals[1] / len(day_stats[1])) if len(day_stats[1]) > 0 else 0,
        'Wednesday': int(day_stats_totals[2] / len(day_stats[2])) if len(day_stats[2]) > 0 else 0,
        'Thursday': int(day_stats_totals[3] / len(day_stats[3])) if len(day_stats[3]) > 0 else 0,
        'Friday': int(day_stats_totals[4] / len(day_stats[4])) if len(day_stats[4]) > 0 else 0,
        'Saturday': int(day_stats_totals[5] / len(day_stats[5])) if len(day_stats[5]) > 0 else 0,
        'Sunday': int(day_stats_totals[6] / len(day_stats[6])) if len(day_stats[6]) > 0 else 0,
    }

    # make the chart
    average_chart = pygal.HorizontalBar()
    average_chart.add('Monday', temp['Monday'])
    average_chart.add('Tuesday', temp['Tuesday'])
    average_chart.add('Wednesday', temp['Wednesday'])
    average_chart.add('Thursday', temp['Thursday'])
    average_chart.add('Friday', temp['Friday'])
    average_chart.add('Saturday', temp['Saturday'])
    average_chart.add('Sunday', temp['Sunday'])
    day_chart = average_chart.render(disable_xml_declaration=True)

    # Experience Gauge Chart
    calculated = calculate_user_level(user.experience, XP_TABLE)
    if user.level != calculated['level']:
        user.level = calculated['level']
        user.prestige = calculated['prestige']
        user.save()
    xp_start = XP_TABLE[calculated['level'] - 2] if calculated['level'] - 2 >= 0 else 0
    xp_next = XP_TABLE[calculated['level'] - 1]
    xp_total_amount_this_level = xp_next - xp_start
    xp_progress_this_level = user.experience - xp_start
    xp_percent = 1.0 / xp_total_amount_this_level * xp_progress_this_level

    return render_template('profile/index.html', 
                           user=user,
                           entries=entries,
                           day_chart=day_chart,
                           xp_percent=xp_percent,
                           xp_next_level=xp_total_amount_this_level,
                           xp_current_level=xp_progress_this_level,
                           is_owner=False)


@mod.route('/<user_slug>/recalc')
def user_profile_recalculate(user_slug):
    """Forces a recalculation of the user's experience, level, etc."""
    user = UserProfile.find_one({'username': user_slug})
    if not user:
        return redirect('/')

    user_entries = CoffeeEntry.find({'user': user.username})

    total_user_xp = calculate_xp_history(user_entries)
    user_current_stats = calculate_user_level(total_user_xp, XP_TABLE)
    print(user_current_stats)
    user.experience = total_user_xp
    user.level = user_current_stats['level']
    user.prestige = user_current_stats['prestige']
    user.save()

    return redirect(f'/profile/{user.username}')


# TODO: remove?
@mod.route('/<user_slug>/delete')
def user_profile_delete(user_slug):
    user = UserProfile.find_one({'username': user_slug})

    if not user:
        return 'No user to delete'

    result = user.delete()

    return result
