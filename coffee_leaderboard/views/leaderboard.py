import datetime
import operator
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, Response
from coffee_leaderboard.database.models import CoffeeEntry, UserProfile
from coffee_leaderboard import settings
from coffee_leaderboard.services import create_log_entry
from coffee_leaderboard.templating import templates


app = Starlette()


@app.route('/', methods=['GET', 'POST'])
async def leaderboard(request: Request):

    if request.method == 'POST':
        form_data: dict = await request.form()

        # Lock down requests so your Slack is the only sender accepted
        if settings.SLACK_TOKEN:
            token: str = form_data.get('token', None)
            if token is None or token != settings.SLACK_TOKEN:
                return Response(status_code=403)

        user_name: str = form_data.get('user_name', None)
        text: str = form_data.get('text', None)
        channel_name: str = form_data.get('channel_name', None)
        channel_id: str = form_data.get('channel_id', None)

        # require all fields
        if not user_name or not text or not channel_id or not channel_name:
            return Response(status_code=400)

        # get or create user
        user, newly_created_user = await UserProfile.get_or_create(username=user_name)

        await create_log_entry(user, text, channel_id, channel_name)

        return Response(status_code=200)
    
    else:
        # set up time information
        this_morning = datetime.datetime.now().replace(hour=0, minute=0, second=0)
        this_week = this_morning - datetime.timedelta(days=this_morning.weekday())
        this_morning = int(this_morning.timestamp() * 1000)
        this_week = int(this_week.timestamp() * 1000)

        all_users = await UserProfile.all()

        by_user_today = {}
        by_user_week = {}
        by_user_all_time = {}

        for user_profile in all_users:
            # today
            entries_today = await CoffeeEntry.filter(date__gte=this_morning, user=user_profile).count()
            if entries_today > 0:
                by_user_today[user_profile.username] = entries_today

            # this week
            entries_week = await CoffeeEntry.filter(date__gte=this_week, user=user_profile).count()
            if entries_week > 0:
                by_user_week[user_profile.username] = entries_week

            # all time
            entries_all_time = await CoffeeEntry.filter(user=user_profile).count()
            if entries_all_time > 0:
                by_user_all_time[user_profile.username] = entries_all_time

        leaderboard_today = []
        temp = sorted(by_user_today.items(), key=operator.itemgetter(1))
        temp = reversed(temp)
        for item in temp:
            leaderboard_today.append({'user': item[0], 'total': item[1]})

        leaderboard_week = []
        temp = sorted(by_user_week.items(), key=operator.itemgetter(1))
        temp = reversed(temp)
        for item in temp:
            leaderboard_week.append({'user': item[0], 'total': item[1]})

        leaderboard_all_time = []
        temp = sorted(by_user_all_time.items(), key=operator.itemgetter(1))
        temp = reversed(temp)
        for item in temp:
            leaderboard_all_time.append({'user': item[0], 'total': item[1]})

        return templates.TemplateResponse(
            'leaderboard/index.html',
            {
                'request': request,
                'entries_today': leaderboard_today,
                'entries_total': leaderboard_all_time,
                'entries_week': leaderboard_week
            }
        )
