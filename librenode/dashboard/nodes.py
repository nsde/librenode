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

def list_all():
    return [e for e in os.listdir('nodes/') if os.path.isdir(f'nodes/{e}')]

class NodeException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class Node:
    def __init__(self, name: str, minecraft_version: str=None, port: int=25565, max_players: int=20):
        """Connects to an existing node or creates a new one.

        Args:
            name (str): The name of the node.
            minecraft_version (str, optional): Minecraft Version, e.g. 1.19.1. Only required on creation.
            port (int, optional): Minecraft Server port. Defaults to 25565, which is the standard.
            max_players (int, optional): Maximum player count. Defaults to 20.
        """
        self.name = name
        self.port = port
        self.minecraft_version = minecraft_version
        self.max_players = max_players

        self.id = ''.join([c for c in name if c.isalpha() or c.isdigit() or c==' ']).rstrip().lower() # convert to a safe file name
        self.path = f'nodes/{self.id}' # folder of the node

        self.setup() # create the node if it doesn't exist yet

    def remove(self) -> None:
        """Removes the files and folders of the node.
        """
        if self.is_active: # if the server is still running
            self.stop() # shut the server down

        shutil.rmtree(self.path)

    def setup(self) -> None:
        """Creates the startup script, needed folders and files, and more for a node.

        Raises:
            NodeException: if no Minecraft version arument was given.
        """
        if not os.path.exists(self.path): # node does not exist
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
        """Gets the correct full absolute file path for the given file name.

        Args:
            name (str): The file name.

        Returns:
            str: The full absolute path.
        """
        return os.path.join(self.path, name)

    def write_to(self, name: str, content: str):
        """Simply writes content to a file.

        Args:
            name (str): File name.
            content (str): File content.
        """
        with open(self.get_file(name), 'w') as f:
            f.write(content)

    def accept_eula(self) -> None:
        """Accepts the Minecraft EULA.
        """
        self.write_to('eula.txt', 'eula=true')

    def cmd(self, command: str):
        """Runs a shell command.

        Args:
            command (str): The command to run.

        Returns:
            Exception | bool | str: Command result.
        """
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
        if not self.is_active:
            raise NodeException('This node is already inactive! Can\'t stop an inactive node.')

        self.cmd(f'screen -X -S lino-{self.id} kill')

if __name__ == '__main__':
    print(list_all())
    # test_node = Node('testing_demo', '1.18.2', max_players=42)
    # test_node
    # print(test_node.is_active)
    # downloads.download(downloads.purpur_url(), test_node.path)
