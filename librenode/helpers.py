import os
import json
import tools
import flask
import sidebar

from dotenv import load_dotenv

load_dotenv()

UPLOAD_LIMIT_MB = 3000

def setup(app: flask.Flask):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.secret_key = os.getenv('FLASK_SECRET_KEY')
    app.config['MAX_CONTENT_LENGTH'] = UPLOAD_LIMIT_MB * 1024 * 1024

    @app.context_processor
    def inject_sidebar():  
        return dict(navigation=sidebar.NAV,
            discord_id=flask.session.get('discord_id'),         
            discord_avatar=flask.session.get('discord_avatar'),            
            discord_username=flask.session.get('discord_username')            
        )

    @app.before_request
    def login_wall():
        path = flask.request.path
        
        if not path in ['/login', '/auth']:
            if not '/static/' in path:
                # has_access_ip = tools.ip(flask.request) in json.load(open('librenode/admin_ips.json'))
                has_access_session = flask.session.get('discord_username') 

                if flask.session.get('discord_id'):
                    if int(flask.session.get('discord_id')) not in json.load(open('librenode/admins.json')).values():
                        has_access_session = False

                # if not has_access_ip:
                #     return flask.redirect('/login')

                if not has_access_session:
                    return flask.redirect('/login')#?session=new'

    @app.route('/<page>/↑')
    def move_up(page):
        return flask.redirect('/' + sidebar.PATHS[sidebar.PATHS.index(page)-1])

    @app.route('/<page>/↓')
    def move_down(page):
        return flask.redirect('/' + sidebar.PATHS[sidebar.PATHS.index(page)+1])

    @app.route('/redirect/to/<path:subpath>')
    def redirect_to(subpath):
        return flask.redirect(subpath.replace(':/', '://'))

def show(*args, **kwargs):
    html = flask.render_template(*args, **kwargs)

    return html