from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from coffee_leaderboard.database.models import CoffeeEntry, UserProfile
from coffee_leaderboard import settings
import typing
import hashlib
import hmac
import base64


app = Starlette(template_directory='coffee_leaderboard/templates')


async def parse_slack_signature(request: Request) -> str:
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    request_body = await request.body()
    sig_basestring = f'v0:{timestamp}:{request_body}'
    hashed = base64.b64encode(hmac.new(settings.SLACK_TOKEN, sig_basestring, digestmod=hashlib.sha256).hexdigest())
    return f'v0={hashed}'


@app.route('/auth/request', methods=['POST'])
async def authenticate_app(request: Request):
    form = await request.form()

    token = form.get('token')
    if token != settings.SLACK_TOKEN:
        return JSONResponse(status_code=403)

    # get user_name/userid

    # create an auth token for that user

    # store token in db

    # DM that user with the token

    return JSONResponse(status_code=200)


@app.route('/action-event', methods=['POST'])
async def action_event(request: Request):

    # validate
    sig: str = await parse_slack_signature(request)
    if not hmac.compare_digest(sig, request.headers.get('X-Slack-Signature')):
        return JSONResponse(status_code=403)

    payload = await request.json()

    if 'type' not in payload or 'token' not in payload:
        return JSONResponse(status_code=403)

    token = payload['token']
    if token != settings.SLACK_TOKEN:
        return JSONResponse(status_code=403)

    event_type = payload['type']

    if event_type == 'url_verification':
        return JSONResponse(content={
            'challenge': payload['challenge']
        })

    return JSONResponse(status_code=200)
