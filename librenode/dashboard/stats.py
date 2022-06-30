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

from nbt import nbt

from .nodes import Node

def get_player_file(node: Node, name: str) -> list:
    try:
        with open(node.get_file(name) + '.json') as f:
            return [i['name'] for i in json.load(f)]
    
    except FileNotFoundError:
        return []

def get_ingame_time(node: Node) -> str:
    ingame_time = nbt.NBTFile(f'{node.path}/world/level.dat')[0]['Time'].value % 24000

    if ingame_time <= 6000:
        time_name = 'day'
    if ingame_time > 6000:
        time_name = 'noon'
    if ingame_time > 13000:
        time_name = 'night'
    if ingame_time > 18000:
        time_name = 'midnight'

    return time_name  

def minecraft(node: Node) -> dict:
    ops = get_player_file(node, 'ops')
    bans = get_player_file(node, 'banned-players')
    ip_bans = get_player_file(node, 'banned-ips')
    whitelist = get_player_file(node, 'whitelist')
    last_players = get_player_file(node, 'usercache')

    try:
        with mcipc.query.Client('127.0.0.1', node.port) as client:
            server_data = client.stats(full=True)
    except ConnectionRefusedError:
        server_data = None

    if server_data:
        plugin_list = list(server_data.plugins.values())[0]
        players = server_data.players
        player_count = f'{server_data.num_players}/{server_data.max_players}'
        version = server_data.version
        game_type = server_data.game_type

    try:
        igt = get_ingame_time(node)
    except FileNotFoundError:
        igt = '?'
    
    try:
        software = {
            'name': node.details.get('software'),
            'url': node.details.get('url')
        }

    except FileNotFoundError:
        software = {
            'name': 'Not set up yet',
            'url': '#'
        }

    return {
        'players': players if server_data else 0,
        'player_count': player_count if server_data else '0/0',
        'version': version if server_data else 'Offline',
        'game_type': game_type if server_data else '?',
        'last_players': last_players if server_data else [],
        'whitelist': whitelist if server_data else [],
        'plugins': plugin_list if server_data else [],
        'ops': ops if server_data else [],
        'normal_bans': bans if server_data else [],
        'ip_bans': ip_bans if server_data else [],

        'time': igt,
        'software': software
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
