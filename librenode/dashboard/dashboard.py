from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard_bp',
    __name__,
    template_folder='../'
)

@dashboard_bp.route('/apps')
def apps():
    return render_template('dashboard/templates/apps.html')
