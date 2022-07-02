import json
import flask
import dhooks

def to_discord(node, text: str) -> None:
    with open(f'{node.path}/webhook.json', 'r') as f:
        data = json.load(f)
    
    hook = dhooks.Webhook('https://discord.com/api/webhooks/992050428772634624/5SnBM0OQ78dEKrRBgsHei0pjcVO8ATDUOvdi0Jo1CnwagMF7HR2qwGSnmkoUMpbhDs4g')
    embed = Embed(
        description=text,
        color=0x662FE8,
        timestamp='now'
    )
    
    embed.set_title(title='ℹ️ · Node Admin Action', url='https://lino.onlix.me/audit')

    embed.set_author(name=flask.session.get('discord_username'))
    embed.set_footer(text='Sent using LibreNode', icon_url='https://lino.onlix.me/static/assets/icon.png')

    hook.send(embed=embed)

def to_file(node, text: str) -> None:
    with open(node.get_file('audit.log'), 'a') as f:
        f.write(f'{flask.session.get("discord_username")} » {text}')

def log(*args, **kwargs) -> None:
    to_discord(*args, **kwargs)
    to_file(*args, **kwargs)
