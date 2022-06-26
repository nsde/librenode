import sys
sys.path.append('..') # this is important - to make local modules work

import json
import time
import flask
import tools
import psutil
import distro
import requests
import subprocess

import mcipc.query

SERVER_PATH = 'server'

def get_player_file(name: str) -> list:
    with open(f'{SERVER_PATH}/{name}.json') as f:
        return [player['name'] for player in json.load(f)]

def minecraft() -> dict:
    ops = get_player_file('ops')
    bans = get_player_file('banned-players')
    ip_bans = get_player_file('banned-ips')
    whitelist = get_player_file('whitelist')
    last_players = get_player_file('usercache')

    with mcipc.query.Client('127.0.0.1', 25565) as client:
        server_data = client.stats(full=True)

    plugin_list = []

    if server_data.plugins:
        plugin_list = list(server_data.plugins.values())[0]

    return {
        'players': server_data.players,
        'player_count': f'{server_data.num_players}/{server_data.max_players}' if server_data else '0/0',
        'version': server_data.version if server_data else 'Offline',
        'game_type': server_data.game_type if server_data else 'Server is not avaiable',
        'last_players': last_players,
        'whitelist': whitelist,
        'plugins': plugin_list,
        'ops': ops,
        'normal_bans': bans,
        'ip_bans': ip_bans,
    }

def hardware() -> dict:
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    return {
        'cpu': psutil.cpu_percent(),
        'cpus': psutil.cpu_count(),
        'threads': psutil.cpu_count(logical=False),
        'ram': f'{tools.readable_size(ram.used)}/{tools.readable_size(ram.total)} GB ({ram.percent}%)',
        'disk': f'{tools.readable_size(disk[1])}/{tools.readable_size(disk[0])} GB ({disk[3]}%)',
        'boot_days': round((time.time()-psutil.boot_time())/86400),
        'os': f'{distro.linux_distribution()[0]} {distro.linux_distribution()[1]}',
    }