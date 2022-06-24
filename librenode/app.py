import flask

app = flask.Flask(__name__, static_url_path='/')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@app.route('/')
def index():
    return flask.render_template('home.html')

app.run(port=1234, debug=True)