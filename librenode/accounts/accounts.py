import os
import flask

from requests_oauthlib import OAuth2Session

accounts_bp = flask.Blueprint('accounts_bp',
    __name__,
    template_folder='../'
)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

API_URL = 'https://discordapp.com/api'
CLIENT_ID = '829409199380234259'
CLIENT_SECRET = open('../private/data/discord_login_.secret').read()
REDIRECT_URI = 'https://onlix.me/login'
SCOPES = ['identify', 'email']

@accounts_bp.route('/login')
def login():
    if flask.request.args.get('code'): # OAUTH CALLBACK/REDIRECT
        discord_account = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=flask.session.get('state'), scope=SCOPES)
        token = discord_account.fetch_token(
            f'{API_URL}/oauth2/token',
            client_secret=CLIENT_SECRET,
            authorization_response=flask.request.url,
        )
        flask.session['discord_token'] = token
        return flask.redirect('/login') # LOG IN

    else:
        if flask.session.get('discord_token'): # LOGGED IN
            discord_account = OAuth2Session(CLIENT_ID, token=flask.session['discord_token'])
            profile = discord_account.get(f'{DISCORD_API_URL}/users/@me').json()
            email_full = profile.get('email')
            if email_full:
                email = f'{email_full[:2]}***@{email_full.split("@")[1][:2]}***.{email_full.split(".")[-1]}'
            
            return flask.render_template('accounts/templates/login.html', profile=profile, email=email)

@accounts_bp.route('/login/fail')
def login_fail():
    return flask.render_template('accounts/templates/login-failed.html')

@accounts_bp.before_request
def login_wall():
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)
    login_url, state = oauth.authorization_url(f'{API_URL}/oauth2/authorize')
    flask.session['state'] = state

    return flask.render_template('accounts/templates/login.html', login_url=login_url)
