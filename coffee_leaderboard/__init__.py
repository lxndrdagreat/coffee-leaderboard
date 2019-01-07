from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import PlainTextResponse
from coffee_leaderboard.views.leaderboard import app as leaderboard


app = Starlette()
# TODO: get debug from config
app.debug = True
app.mount('/static', StaticFiles(directory='coffee_leaderboard/static'))
app.mount('', leaderboard)

# @app.route('/')
# def homepage(request):
#     return PlainTextResponse('Hello, world!')

# set up views
# from coffee_leaderboard.views import leaderboard
# from coffee_leaderboard.views import profile
# from coffee_leaderboard.views import plusxp
#
# app.register_blueprint(leaderboard.mod)
# app.register_blueprint(profile.mod, url_prefix='/profile')
# app.register_blueprint(plusxp.mod, url_prefix='/plusxp')
