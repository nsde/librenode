import os
import shutil
import subprocess

class Node:
    def __init__(self, name: str):
        self.name = name
        self.path = f'nodes/{name}'

        self.setup()

    def remove(self) -> None:
        os.remove(self.path)

    def setup(self) -> None:
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def get_file(name: str) -> str:
        return os.path.join(self.path, name)

    def accept_eula(self) -> None:
        with open(get_file('eula.txt'), 'w') as f:
            f.write('eula=true')
    
    def run(self, java_version='18') -> None:
        shutil.copy('tools/start_node.sh', get_file('run.sh'))
        command = f'screen -S sh {get_file("run.sh")}'
        subprocess.call(command.split())

if __name__ == '__main__':
    test_node = Node('testing_demo')
    test_node.run()