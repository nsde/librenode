import wget
import json
import requests

def data(url: str, use_headers=False):
    headers = json.load(open('librenode/headers.json')) if use_headers else {}
    return requests.get(url, headers=headers).json()

def download(url: str, path: str):
    
    server_software = {
        'purpurmc.org': 'Purpur',
        'papermc.io': 'Paper'
    }

    for domain in server_software:
        if domain in url:
            current_software = server_software[domain]

    with open(f'{path}/server.jar', 'wb') as f:
        f.write(requests.get(url).content)
    
    with open(f'{path}/node.json', 'w') as f:
        json.dump(
            {
                'url': url,
                'path': path,
                'software': current_software
            },
        f
        )

def purpur_versions() -> list:
    return data('https://api.purpurmc.org/v2/purpur')['versions']

def purpur_url(mc_version: str=None) -> str:
    mc_version = mc_version or purpur_versions()[-1] # no argument? use latest version!
    return f'https://api.purpurmc.org/v2/purpur/{mc_version}/latest/download'

def paper_versions() -> list:
    return data('https://api.papermc.io/v2/projects/paper')['versions']

def paper_url(mc_version: str=None) -> str:
    mc_version = mc_version or paper_versions()[-1] # no argument? use latest version!
    latest_build = data(f'https://api.papermc.io/v2/projects/paper/versions/{mc_version}')['builds'][-1]
    
    return f'https://api.papermc.io/v2/projects/paper/versions/{mc_version}/builds/{latest_build}/downloads/paper-{mc_version}-{latest_build}.jar' 

if __name__ == '__main__':
    pass
