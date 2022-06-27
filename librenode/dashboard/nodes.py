import os
import shutil
import subprocess

try:
    import downloads
except ModuleNotFoundError:
    from . import downloads

JAVA_BINARIES = {
    8: '/usr/lib/jvm/adoptopenjdk-8-hotspot-amd64/bin/java',
    16: '/usr/lib/jvm/java-16-oracle/bin/java',
    17: '/opt/jdk17/bin/java',
    18: '/stuff/jdk-18/bin/java'
}

MINECRAFT_JAVA_VERSIONS = {
    '1.8': 8,
    '1.12': 8,
    '1.14': 8,
    '1.16': 16,
    '1.17': 17,
    '1.18': 17,
    '1.19': 18
}

def get_java_binary(minecraft_version: str) -> str:
    version_group = '.'.join(minecraft_version.split('.')[:2]) # e.g. 1.18.2 → 1.18
    return JAVA_BINARIES[MINECRAFT_JAVA_VERSIONS[version_group]]

def replacer(text: str, dictionary: dict) -> str:
    for key, value in dictionary.items():
        text = text.replace(key, value)

    return text

class NodeException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class Node:
    def __init__(self, name: str, minecraft_version: str=None, port: int=25565, max_players: int=20):
        self.name = name
        self.port = port
        self.minecraft_version = minecraft_version
        self.max_players = max_players

        self.id = ''.join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).rstrip().lower()
        self.path = f'nodes/{self.id}'

        self.setup()

    def remove(self) -> None:
        shutil.rmtree(self.path)

    def setup(self) -> None:
        if not os.path.exists(self.path):
            if not self.minecraft_version:
                raise NodeException('Please a provide a valid Minecraft version argument!')

            os.mkdir(self.path)

            VARS = {
                '<java_binary>': get_java_binary(self.minecraft_version),
                '<minecraft_version>': self.minecraft_version,
                '<path>': self.path,
                '<port>': str(self.port),
                '<max_players>': str(self.max_players)
            }

            run_sh_content = open('tools/start_node.sh').read()
            run_sh_content = replacer(run_sh_content, VARS) 

            self.write_to('run.sh', run_sh_content)
            run_sh_file = self.get_file('run.sh')

            self.cmd(f'sudo chmod +x {run_sh_file}')

    def get_file(self, name: str) -> str:
        return os.path.join(self.path, name)

    def write_to(self, name: str, content: str):
        with open(self.get_file(name), 'w') as f:
            f.write(content)

    def accept_eula(self) -> None:
        write_to('eula.txt', 'eula=true')

    def cmd(self, command: str, ):
        try:
            return subprocess.check_output(command, stdin=None, shell=True).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            return False

    @property
    def is_active(self):
        return bool(self.cmd(f'screen -list | grep lino-{self.id}'))

    def start(self) -> None:
        if self.is_active:
            raise NodeException('This node is already active! Can\'t start a node with the same name and ID.') 
        
        self.cmd(f'screen -dmS lino-{self.id} {self.get_file("run.sh")} > {self.get_file("node.log")}')

    def stop(self) -> None:
        self.cmd(f'screen -X -S lino-{self.id} kill')

if __name__ == '__main__':
    test_node = Node('testing_demo', '1.18.2', max_players=42)
    test_node.stop()
    print(test_node.is_active)
    # downloads.download(downloads.purpur_url(), test_node.path)
