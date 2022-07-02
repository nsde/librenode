import sys
sys.path.append('..') # this is important - to make local modules work

import os
import json
import flask

from requests_oauthlib import OAuth2Session

import tools

accounts_bp = flask.Blueprint('accounts_bp',
    __name__,
    template_folder='../'
)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0' # change this to '1' if you're running this on localhost!

API_URL = 'https://discordapp.com/api'
CLIENT_ID = str(os.getenv('DISCORD_CLIENT_ID'))
CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
REDIRECT_URI = 'https://lino.onlix.me/login'
SCOPES = ['identify', 'email']

@accounts_bp.route('/logout')
def logout():
    # admin_ips = json.load(open('librenode/admin_ips.json')) or []
    # admin_ips.remove(tools.ip(flask.request)) # clear IP
    flask.session.pop('discord_token', None)
    # json.dump(admin_ips, open('librenode/admin_ips.json', 'w'))

    return flask.redirect('/login')

@accounts_bp.route('/auth')
def auth():
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPES)
    login_url, state = oauth.authorization_url(f'{API_URL}/oauth2/authorize')
    flask.session['state'] = state

    return flask.redirect(login_url)

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
        return flask.redirect('/login')

    if flask.session.get('discord_token'): # ALREADY LOGGED IN
        discord_account = OAuth2Session(CLIENT_ID, token=flask.session['discord_token'])
        profile = discord_account.get(f'{API_URL}/users/@me').json()

        flask.session['discord_id'] = profile['id']
        flask.session['discord_username'] = profile['username']
        flask.session['discord_avatar'] = profile['avatar']

        if int(profile['id']) not in list(json.load(open('librenode/admins.json')).values()): # User is not admin
            return flask.render_template('accounts/templates/login-failed.html')
        
        # if not tools.ip(flask.request) in json.load(open('librenode/admin_ips.json')):
        #     admin_ips = json.load(open('librenode/admin_ips.json')) or []
        #     admin_ips.append(tools.ip(flask.request))
        #     json.dump(admin_ips, open('librenode/admin_ips.json', 'w'))

        return flask.redirect('/') # DONE

    else: # CONNECT WITH DISCORD
        admins = list(json.load(open('librenode/admins.json')).keys())
        return flask.render_template('accounts/templates/home.html', is_new_session=flask.request.args.get('session') == 'new', admins=admins)
