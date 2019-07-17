from coffee_leaderboard.database.models import CoffeeEntry, UserProfile
import datetime


async def create_log_entry(user: UserProfile, message: str, channel_id: str = '', channel_name: str = ''):

    entry = CoffeeEntry(user=user,
                        text=message,
                        channel_id=channel_id,
                        channel_name=channel_name,
                        date=int(datetime.datetime.utcnow().timestamp() * 1000))

    split_text = message.split(' ')
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
        entry.date = int((datetime.datetime.utcnow() - datetime.timedelta(days=offset)).timestamp() * 1000)

    await entry.save()
