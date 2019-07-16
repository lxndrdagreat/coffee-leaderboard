from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from coffee_leaderboard.views.leaderboard import app as leaderboard
from coffee_leaderboard.views.profile import app as profile
from coffee_leaderboard.database import init_db
from coffee_leaderboard import settings


app = Starlette()
app.debug = settings.DEBUG
app.mount('/static', StaticFiles(directory=settings.STATIC_FILES_PATH))

# mount child views
app.mount('/profile', profile)
app.mount('', leaderboard)


@app.middleware("http")
async def database_middleware(request, call_next):
    await init_db()
    return await call_next(request)
