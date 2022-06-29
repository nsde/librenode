import flask

from . import nodes
from . import downloads

setups_bp = flask.Blueprint('setups_bp',
    __name__,
    template_folder='../'
)

@setups_bp.route('/setup/purpur', methods=['POST'])
def setup_purpur():
    
    return flask.redirect('/home?action=update')
