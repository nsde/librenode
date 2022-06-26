import yaml
import flask
import base64

from io import BytesIO
from datetime import datetime

def fix_formatting(text: str) -> str:
    return text.replace('  ', '&nbsp;').replace('\n', '\n<br>\n')

def readable_size(size: float) -> int:
    return size//1000000000

def ip(request: flask.Request) -> str: # PRIVACY NOTICE
    if not request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ['REMOTE_ADDR']
    return request.environ['HTTP_X_FORWARDED_FOR']

def yml(path: str, edit_to=None):
    path = f'{path}.yml'

    if not edit_to:
        try:
            with open(path) as f:
                return yaml.load(f.read(), Loader=yaml.SafeLoader)
        except:
            open(path, 'w').write('{}')
            return {}

    with open(path, 'w') as f:
        yaml.dump(edit_to, f, sort_keys=False, default_flow_style=False, indent=4)

def unix_to_readable(unix):
    return datetime.utcfromtimestamp(float(unix)).strftime('%Y/%m/%d %H:%M')