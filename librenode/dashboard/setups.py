import flask

from . import nodes
from . import audit
from . import downloads

setups_bp = flask.Blueprint('setups_bp',
    __name__,
    template_folder='../'
)

@setups_bp.route('/setup/purpur', methods=['POST'])
def setup_purpur():
    form = flask.request.form.to_dict()
    
    base = nodes.Node(
        name='base',
        port=form['port'],
        minecraft_version='1.19',
        max_players=form['max-players']
    )
    base.setup()
    downloads.download(downloads.purpur_url(), base.path)

    return flask.redirect('/home?action=update')

@setups_bp.route('/server/start')
def start():
    audit.log('Started node')
    nodes.Node('base').start()
    return flask.redirect('/home?action=start')

@setups_bp.route('/server/stop')
def stop():
    audit.log('Stopped node')
    nodes.Node('base').stop()
    return flask.redirect('/home?action=stop')

@setups_bp.route('/server/reset')
def reset_confirmation():
    audit.log('Delete node')
    return flask.render_template('dashboard/templates/confirmation.html')

@setups_bp.route('/server/reset/confirm')
def actual_reset():
    nodes.Node('base').remove()
    return flask.redirect('/home?action=reset')
