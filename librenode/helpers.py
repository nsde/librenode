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
        return dict(navigation=sidebar.NAV)

def show(*args, **kwargs):
    html = flask.render_template(*args, **kwargs)

    return html