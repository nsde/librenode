import flask

import helpers

from dashboard.dashboard import dashboard_bp
from accounts.accounts import accounts_bp

app = flask.Flask(__name__, static_url_path='/', static_folder='static/')
helpers.setup(app)

app.register_blueprint(dashboard_bp)
app.register_blueprint(accounts_bp)

app.run(port=7878, debug=True)