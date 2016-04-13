import requests
import random
from flask import Flask, redirect, render_template, request
import json
from pymongo import MongoClient
import datetime
import operator

slack_api_token = "YOUR-SLACK-API-TOKEN-GOES-HERE"
slack_api_url = "https://slack.com/api/chat.postMessage"

app = Flask(__name__)

client = MongoClient()

# change to match your collection
db = client.coffee

# if your db needs authentication...
#db.authenticate('username','password')


def slack_message():
    message = {
            "token": slack_api_token,
            "channel": None,
            "text": "",
            "username": "COFFEE STATS",
            "icon_url": ""
    }
    return message

@app.route('/add', methods=['POST'])
def add():
    user_id = None
    user_name = None
    text = None
    channel_name = None
    channel_id = None

    # Lock down requests so your Slack is the only sender accepted
    if request.form.get('token') is None:
        return

    user_name = request.form.get('user_name')
    text = request.form.get('text')
    channel_name = request.form.get('channel_name')
    channel_id = request.form.get('channel_id')

    stat = {
        "user": user_name,
        "text": text,
        "date": datetime.datetime.utcnow(),
        "channel_id": channel_id,
        "channel_name": channel_name
    }

    if "--yesterday" in text or '-y' in text:
        stat['date'] = datetime.datetime.utcnow() - datetime.timedelta(days=1)

    db.log.insert_one(stat)

    user_total = db.stats.find_one({'user': user_name})
    usr = {
        'user': user_name,
        'total': user_total['total'] + 1 if user_total is not None else 1
    }

    db.stats.update({'user':user_name}, usr, True)

    return


@app.route('/', methods=['GET'])
def index():
"""
    Main and only page is the leaderboard itself.
"""
    leaderboard = {
        "totals": [],
        "today": [],
        "week": []
    }        
    cursor = db.log.find()
    lead_total = {}
    for entry in cursor:
        if not entry['user'] in lead_total:
            lead_total[entry['user']] = 0
        lead_total[entry['user']] += 1
    temp = sorted(lead_total.items(), key=operator.itemgetter(1))
    temp = reversed(temp)
    for item in temp:
        leaderboard['totals'].append({'user':item[0],'total':item[1]})

    # get today's stats
    this_morning = datetime.datetime.now().replace(hour=0, minute=0, second=0)
    cursor = db.log.find({'date':{'$gte':this_morning}})

    lead_today = {}
    for entry in cursor:
        if not entry['user'] in lead_today:
            lead_today[entry['user']] = 0
        lead_today[entry['user']] += 1
    temp = sorted(lead_today.items(), key=operator.itemgetter(1))
    temp = reversed(temp)
    for item in temp:
        leaderboard['today'].append({'user':item[0],'total':item[1]})       

    # get week stats
    day_today = datetime.datetime.today()
    week_start = day_today - datetime.timedelta(days = day_today.weekday())
    week_start = week_start.replace(hour=0, minute=0)
    cursor = db.log.find({'date':{'$gte':week_start}})
    lead_week = {}
    for entry in cursor:
        if not entry['user'] in lead_week:
            lead_week[entry['user']] = 0
        lead_week[entry['user']] += 1

    temp = sorted(lead_week.items(), key=operator.itemgetter(1))
    temp = reversed(temp)

    for item in temp:
        leaderboard['week'].append({'user': item[0], 'total':item[1]})

    # coffee by day breakdown        
    cursor = db.log.find({})
    day_stats = [{},{},{},{},{},{},{}]
    day_stats_totals = [0, 0, 0, 0, 0, 0, 0]
    for entry in cursor:
        # get the date from the datetime as a string
        dt = entry['date'].date().isoformat()
        weekday = entry['date'].weekday()
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

    temp = sorted(temp.items(), key=operator.itemgetter(1))
    temp = reversed(temp)
    leaderboard['daystats'] = []
    for item in temp:
        leaderboard['daystats'].append({'day':item[0],'count':item[1]})

    return render_template("index.html", leaderboard=leaderboard)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=4444)
