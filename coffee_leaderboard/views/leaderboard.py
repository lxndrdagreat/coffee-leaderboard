# coffee-leaderboard/views/leaderboard.py

from flask import Blueprint, render_template, request, abort
import random
import json
import datetime
import operator
import pygal
from coffee_leaderboard.database import UserProfile, CoffeeEntry
from coffee_leaderboard import app


mod = Blueprint('leaderboard', __name__)


@mod.route('/', methods=['GET', 'POST'])
def leaderboard():
    """Primary leaderboard view."""

    if request.method == 'GET':

        leaderboard = {
            "totals": [],
            "today": [],
            "week": []
        }        
        log_entries = CoffeeEntry.find()
        lead_total = {}
        for entry in log_entries:
            if not entry.user in lead_total:
                lead_total[entry.user] = 0
            lead_total[entry.user] += 1
        temp = sorted(lead_total.items(), key=operator.itemgetter(1))
        temp = reversed(temp)
        for item in temp:
            leaderboard['totals'].append({'user':item[0],'total':item[1]})

        # get today's stats
        this_morning = datetime.datetime.now().replace(hour=0, minute=0, second=0)
        log_entries = CoffeeEntry.find({'date':{'$gte':this_morning}})

        lead_today = {}
        for entry in log_entries:
            if not entry.user in lead_today:
                lead_today[entry.user] = 0
            lead_today[entry.user] += 1
        temp = sorted(lead_today.items(), key=operator.itemgetter(1))
        temp = reversed(temp)
        for item in temp:
            leaderboard['today'].append({'user':item[0],'total':item[1]})       

        # get week stats
        day_today = datetime.datetime.today()
        week_start = day_today - datetime.timedelta(days = day_today.weekday())
        week_start = week_start.replace(hour=0, minute=0)
        log_entries = CoffeeEntry.find({'date':{'$gte':week_start}})
        lead_week = {}
        for entry in log_entries:
            if not entry.user in lead_week:
                lead_week[entry.user] = 0
            lead_week[entry.user] += 1

        temp = sorted(lead_week.items(), key=operator.itemgetter(1))
        temp = reversed(temp)

        for item in temp:
            leaderboard['week'].append({'user': item[0], 'total':item[1]})

        # coffee by day breakdown        
        log_entries = CoffeeEntry.find()
        day_stats = [{},{},{},{},{},{},{}]
        day_stats_totals = [0, 0, 0, 0, 0, 0, 0]
        for entry in log_entries:
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

        average_chart = pygal.HorizontalBar()
        average_chart.add('Monday', temp['Monday'])
        average_chart.add('Tuesday', temp['Tuesday'])
        average_chart.add('Wednesday', temp['Wednesday'])
        average_chart.add('Thursday', temp['Thursday'])
        average_chart.add('Friday', temp['Friday'])
        average_chart.add('Saturday', temp['Saturday'])
        average_chart.add('Sunday', temp['Sunday'])
        average_chart_output = average_chart.render(disable_xml_declaration=True)

        temp = sorted(temp.items(), key=operator.itemgetter(1))
        temp = reversed(temp)
        leaderboard['daystats'] = []
        for item in temp:
            leaderboard['daystats'].append({'day':item[0],'count':item[1]})

        return render_template("leaderboard/index.html", leaderboard=leaderboard, average_chart=average_chart_output)

    else:
        token = request.form.get('token', None)

        # Lock down requests so your Slack is the only sender accepted
        if token is None or token != app.config['SLACK_API_TOKEN']:
            abort(403)

        user_name = request.form.get('user_name', None)
        text = request.form.get('text', None)
        channel_name = request.form.get('channel_name', None)
        channel_id = request.form.get('channel_id', None)

        # require all fields
        if not user_name or not text or not channel_id or not channel_name:
            abort(400) # bad request

        entry = CoffeeEntry()
        entry.user = user_name
        entry.text = text
        entry.date = datetime.datetime.utcnow()
        entry.channel_name = channel_name
        entry.channel_id = channel_id

        split_text = text.split(' ')
        index = None

        if "--yesterday" in split_text:
            index = split_text.index('--yesterday')
        elif '-y' in split_text:
            index = split_text.index('-y')

        if index is not None:
            try:
                offset = int(split_text[index + 1])
            except (IndexError, ValueError):
                offset = 1
            entry.date -= datetime.timedelta(days=offset)

        entry.save()

        return ''
