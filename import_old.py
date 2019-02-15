# this script is for taking JSON dumps provided from the OLD leaderboard MongoDB
# (via mongoexport) and importing them into the 2.0 system.
from coffee_leaderboard.database import init_db
from coffee_leaderboard.database.models import CoffeeEntry, UserProfile
from tortoise import run_async
from tortoise.exceptions import IntegrityError, DoesNotExist
import json
import datetime
import aiofiles


async def make_user(data):

    try:
        existing = await UserProfile.get(username=data['username'])

        if existing:
            print(f'User with username "{data["username"]}" already exists. Skipping.')
            return
    except DoesNotExist:
        pass

    try:
        user = UserProfile(username=data['username'],
                           experience=data['experience'],
                           level=data['level'],
                           prestige=data['prestige'])
        await user.save()
    except IntegrityError as error:
        pass


async def import_users():
    profiles = []
    async with aiofiles.open('profiles.json', mode='r') as users_file:
        async for line in users_file:
            await make_user(json.loads(line.strip()))

    # [await make_user(profile) for profile in profiles]


async def make_entry(data):
    # find associated user
    try:
        user = await UserProfile.get(username=data['user'])
    except DoesNotExist:
        print(f'Cannot create entry for non-existing user "{data["user"]}".')
        return

    if not user:
        print(f'Cannot create entry for non-existing user "{data["user"]}".')
        return

    # create entry
    entry_date = datetime.datetime.fromisoformat(data['date']['$date'].replace('Z', ''))
    # print(entry_date, data['date'])
    entry = CoffeeEntry(user=user,
                        text=data['text'],
                        channel_id=data['channel_id'],
                        channel_name=data['channel_name'],
                        date=int(entry_date.timestamp() * 1000))
    await entry.save()


async def import_entries():
    async with aiofiles.open('log.json', mode='r', encoding='utf8') as log_file:
        async for line in log_file:
            await make_entry(json.loads(line.strip()))


async def import_old_data():
    await init_db()

    # create users
    print('IMPORTING USERS')
    await import_users()

    # create entries, connecting them to users
    print('IMPORTING ENTRIES')
    await import_entries()


if __name__ == '__main__':
    run_async(import_old_data())
