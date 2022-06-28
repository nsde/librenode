import os
# go to the correct path (this file's folder)
os.chdir(os.path.dirname(__file__)) # this is really important and should be done first
os.chdir('..')
#»——————————————————————————————————————————————————————————————————————————«#

import flask
import logging

import helpers

from dashboard.dashboard import dashboard_bp
from accounts.accounts import accounts_bp

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = flask.Flask(__name__, static_url_path='/static', static_folder='static/')
helpers.setup(app)

app.register_blueprint(dashboard_bp)
app.register_blueprint(accounts_bp)

app.run(port=7878, debug=True)