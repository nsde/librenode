import flask
from dashboard.dashboard import dashboard_bp

import helpers

app = flask.Flask(__name__, static_url_path='/', static_folder='static/')
helpers.setup(app)

app.register_blueprint(dashboard_bp)

app.run(port=1234, debug=True)