import os
import requests

from pprint import pprint

auth = os.getenv('MODRINTH_AUTH')
headers = {'Authorization': auth}

def list_all(loader: str='fabric', mc_version='1.19') -> list:
    limit = 100
    url = f'https://api.modrinth.com/v2/search?limit={limit}&facets=[["versions:{mc_version}"]]&loaders=[{loader}]'
    response = requests.get(url=url, headers=headers).json()
    
    return response['hits']

def filtered(mods: list) -> list:
    filtered_mods = []
    
    for mod in mods:
        if mod['server_side'] != 'unsupported':
            mod_data = {
                'slug': mod['slug'],
                'title': mod['title'],
                'description': mod['description'],
                'logo': mod['icon_url'],
                'downloads': mod['downloads']
            }
            
            filtered_mods.append(mod_data)

    return filtered_mods

if __name__ == '__main__':
    mods = list_all()
    pprint(filtered(mods))
