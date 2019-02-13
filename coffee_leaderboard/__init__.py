from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from coffee_leaderboard.views.leaderboard import app as leaderboard
from coffee_leaderboard.database import init_db


app = Starlette()
# TODO: get debug from config
app.debug = True
app.mount('/static', StaticFiles(directory='coffee_leaderboard/static'))

# mount child views
app.mount('', leaderboard)


@app.middleware("http")
async def database_middleware(request, call_next):
    await init_db()
    return await call_next(request)
