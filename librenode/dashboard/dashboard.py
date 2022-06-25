import flask

dashboard_bp = flask.Blueprint('dashboard_bp',
    __name__,
    template_folder='../'
)

@dashboard_bp.route('/')
def root():
    return flask.redirect('/home')

@dashboard_bp.route('/home')
def home():
    return flask.render_template('dashboard/templates/home.html')

@dashboard_bp.route('/apps')
def apps():
    return flask.render_template('dashboard/templates/apps.html')

@dashboard_bp.route('/terminal')
def terminal():
    return flask.render_template('dashboard/templates/terminal.html')
