import flask

from . import stats

dashboard_bp = flask.Blueprint('dashboard_bp',
    __name__,
    template_folder='../'
)

@dashboard_bp.route('/')
def root():
    return flask.redirect('/home')

@dashboard_bp.route('/home')
def home():
    return flask.render_template('dashboard/templates/home.html', stats_minecraft={}, stats_hardware=stats.hardware(), action=flask.request.args.get('action'))

@dashboard_bp.route('/shop')
def shop():
    return flask.render_template('dashboard/templates/shop.html')

@dashboard_bp.route('/setup')
def setup():
    return flask.render_template('dashboard/templates/setup.html')

@dashboard_bp.route('/apps')
def apps():
    return flask.render_template('dashboard/templates/apps.html')

@dashboard_bp.route('/terminal')
def terminal():
    return flask.render_template('dashboard/templates/terminal.html')

@dashboard_bp.route('/files')
def files():
    return flask.render_template('dashboard/templates/files.html')

@dashboard_bp.route('/audit')
def audit():
    return flask.render_template('dashboard/templates/audit.html')

@dashboard_bp.route('/players')
def players():
    return flask.render_template('dashboard/templates/players.html')
