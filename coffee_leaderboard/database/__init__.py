from tortoise import Tortoise
from coffee_leaderboard.database.models import CoffeeEntry, UserProfile
from coffee_leaderboard import settings


async def init_db(generate_schemas: bool = False):
    await Tortoise.init(
        db_url=settings.DATABASE_URL,
        modules={
            'models': ['coffee_leaderboard.database.models']
        }
    )
    if generate_schemas:
        await Tortoise.generate_schemas(safe=True)


async def seed_test_data():
    await init_db()

    # for testing only
    user = UserProfile(username='the_dude')
    await user.save()

    dates = [
        1549978467092,
        1549978467092,
        1549892929567
    ]

    for d in dates:
        entry = CoffeeEntry(user=user, text=':coffee:',
                            channel_id='42', channel_name='my-channel',
                            date=d)
        await entry.save()
