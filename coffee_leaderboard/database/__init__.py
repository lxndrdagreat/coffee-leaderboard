from tortoise import Tortoise
from coffee_leaderboard.database.models import CoffeeEntry


async def init_db(generate_schemas: bool = False):
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={
            'models': ['coffee_leaderboard.database.models']
        }
    )
    if generate_schemas:
        await Tortoise.generate_schemas(safe=True)

    # for testing only
    # entry = CoffeeEntry(user='dan', text=':coffee:',
    #                     channel_id='42', channel_name='my-channel')
    # await entry.save()
