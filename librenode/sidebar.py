NAV = [
    {
        'path': 'home',
        'icon': 'house',
        'name': 'Home'
    },
    {
        'path': 'shop',
        'icon': 'controller',
        'name': 'Mods & Plugins',
    },
    {
        'path': 'apps',
        'icon': 'plugin',
        'name': 'Integrations'
    },
    {
        'path': 'terminal',
        'icon': 'terminal',
        'name': 'Console'
    },
    {
        'path': 'files',
        'icon': 'file-earmark',
        'name': 'Files'
    },
    {
        'path': 'audit',
        'icon': 'list-columns-reverse',
        'name': 'Admin Audit Log',
    },
    {
        'path': 'players',
        'icon': 'people',
        'name': 'Player Management',
        'seperate': True
    },
    {
        'path': 'setup',
        'icon': 'plus-square',
        'name': 'Setup New Node'
    },
    {
        'path': 'redirect/to/https://github.com/nsde/librenode/blob/master/docs/help.md',
        'icon': 'journal-text',
        'name': 'Help',
        'is_external': True
    },
]

PATHS = [i['path'] for i in NAV]

if __name__ == '__main__':
    print(PATHS)