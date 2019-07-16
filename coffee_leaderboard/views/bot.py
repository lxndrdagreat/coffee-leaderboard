from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist
from coffee_leaderboard.database.models import CoffeeEntry, UserProfile, UserAppToken
from coffee_leaderboard import settings
import typing
import hashlib
import hmac
import base64
import datetime


app = Starlette(template_directory='coffee_leaderboard/templates')


async def parse_slack_signature(request: Request) -> str:
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    request_body = await request.body()
    sig_basestring = f'v0:{timestamp}:{request_body}'
    hashed = base64.b64encode(hmac.new(settings.SLACK_SIGNING_SECRET, sig_basestring, digestmod=hashlib.sha256).hexdigest())
    return f'v0={hashed}'


def generate_user_auth_token(user_name: str) -> str:
    timestamp = datetime.datetime.utcnow().timestamp()
    pepper_bytes = bytes(settings.APP_TOKEN_PEPPER, 'utf-8')
    encoded_str = f'{user_name}{timestamp}'.encode('utf-8')
    return hmac.new(pepper_bytes, encoded_str, digestmod=hashlib.sha256).hexdigest()


def generate_app_auth_token(user_name: str) -> str:
    timestamp = datetime.datetime.utcnow().timestamp()
    pepper_bytes = bytes(f'{settings.APP_TOKEN_PEPPER}{int(timestamp)}', 'utf-8')
    encoded_str = f'{user_name}{timestamp}'.encode('utf-8')
    return hmac.new(pepper_bytes, encoded_str, digestmod=hashlib.sha256).hexdigest()


@app.route('/auth/request', methods=['POST'])
async def authenticate_app(request: Request):
    form = await request.form()

    token = form.get('token')
    if token != settings.SLACK_TOKEN:
        return JSONResponse(status_code=403)

    # get user_name/userid
    user_name: str = form.get('user_name')
    user, newly_created_user = await UserProfile.get_or_create(username=user_name)

    # create an auth token for that user
    auth_token = generate_user_auth_token(user_name)

    # store token in db
    user_app_token = UserAppToken(user=user, auth_token=auth_token)
    await user_app_token.save()

    # DM that user with the token

    return JSONResponse(status_code=200,
                        content={
                            # only respond to the user
                            'response_type': 'ephemeral',
                            'text': 'Copy/paste this authentication token into the Coffee Logger App:',
                            'attachments': [
                                {
                                    'text': auth_token
                                }
                            ]
                        })


@app.route('/auth/submit', methods=['POST'])
async def connect_app(request: Request):
    payload = await request.json()

    if 'token' not in payload:
        return JSONResponse(status_code=415)

    # look up the model
    try:
        user_app_auth: UserAppToken = await UserAppToken.get(auth_token=payload['token']).prefetch_related('UserProfile')

        # create token for app
        app_token = generate_app_auth_token(user_app_auth.user.username)

        # update model
        user_app_auth.app_token = app_token
        await user_app_auth.save()

        # send response
        return JSONResponse(status_code=200,
                            content={
                                'token': app_token,
                                'username': user_app_auth.user.username
                            })

    except DoesNotExist:
        return JSONResponse(status_code=403)


@app.route('/log', methods=['POST'])
async def log_from_app(request: Request):
    payload = await request.json()

    # look up token
    if 'token' not in payload:
        return JSONResponse(status_code=403)
    try:
        user_app_auth = UserAppToken.get(app_token=payload['token'])
    except DoesNotExist:
        return JSONResponse(status_code=403)

    # get user for token
    
    # log coffee

    # alert Slack coffee channel

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
