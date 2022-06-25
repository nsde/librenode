import flask

def setup(app: flask.Flask):
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

def show(*args, **kwargs):
    html = flask.render_template(*args, **kwargs)

    return html