import time
import flask

from . import nodes
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
    base = nodes.Node(name='base')

    return flask.render_template(
        'dashboard/templates/home.html',
        stats_mc=stats.minecraft(base),
        stats_hw=stats.hardware(),
        action=flask.request.args.get('action'),
        is_active=base.is_active
    )

@dashboard_bp.route('/shop')
def shop():
    return flask.render_template('dashboard/templates/shop.html')

@dashboard_bp.route('/setup')
def setup():
    return flask.render_template('dashboard/templates/setup.html')

@dashboard_bp.route('/apps', methods=['GET', 'POST'])
def apps():
    form = flask.request.form.to_dict()

    if form.get('url'):
        with open('librenode/admin_ips.json', 'w') as f:
            f.write(form.get('url'))

    return flask.render_template('dashboard/templates/apps.html')

@dashboard_bp.route('/terminal', methods=['GET', 'POST'])
def terminal():
    base = nodes.Node('base')

    form = flask.request.form.to_dict()
    if form.get('command'):
        base.command(form.get('command'))
        time.sleep(0.1)

    log = base.read_from('logs/latest.log')
    log = log.split('\n')
    log.reverse()
    log = log[:100]
    return flask.render_template('dashboard/templates/terminal.html', node_log='\n'.join(log), inactive=not base.is_active)

@dashboard_bp.route('/files')
def files():
    return flask.render_template('dashboard/templates/files.html')

@dashboard_bp.route('/audit')
def audit_log():
    return flask.render_template('dashboard/templates/audit.html')

@dashboard_bp.route('/players')
def players():
    return flask.render_template('dashboard/templates/players.html')
