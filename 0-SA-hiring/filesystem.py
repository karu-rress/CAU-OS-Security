# Q1. 파일 시스템 시뮬레이션
#
# 파일 시스템에서 디렉토리와 파일을 생성하고,
# 파일에 데이터를 쓰고 읽는 프로그램을 작성하세요.

import os
import shlex
from pathlib import Path

class FileSystem:
    def __init__(self):
        # 현재 디렉터리 가져오기
        self.file_system: Path = Path.cwd()

    def mkdir(self, dir_name: str):
        path = self.file_system / dir_name
        path.mkdir(exist_ok=True)

    def touch(self, file_name: str):
        path = self.file_system / file_name
        path.touch(exist_ok=True)

    def write(self, file_name: str, data):
        path = self.file_system / file_name
        path.write_text(data)

    def read(self, file_name: str):
        path = self.file_system / file_name
        if path.exists():
            return path.read_text()
        return None

    def ls(self) -> list[str]:
        # Path.iterdir()
        return os.listdir(self.file_system)

if __name__=="__main__":
    fs = FileSystem()

    print("======== Karu's Filesystem Simulation ========\n")
    print("Commands: mkdir | touch | write | read | ls | help | exit")

    while True:
        cmdv = input('\nShell > ')
        cmdv = shlex.split(cmdv)

        print()
        if cmdv[0] not in ["ls", "help", "exit"] and len(cmdv) == 1 or cmdv[0] == "write" and len(cmdv) < 3:
            print(f'Missing argument for command: "{cmdv[0]}"')
            print(f'type "help" first.\n')
            continue

        match cmdv[0]: # first elem (cmd)
            case "mkdir":
                fs.mkdir(cmdv[1])
                print(f'Created directory "{cmdv[1]}".')
            case "touch":
                fs.touch(cmdv[1])
                print(f'Touched file "{cmdv[1]}".')
            case "write":
                fs.write(cmdv[1], cmdv[2])
                print(f'Writed given data to "{cmdv[1]}".')
            case "read":
                ret = fs.read(cmdv[1])
                if ret is None:
                    print(f'Error: "{cmdv[1]}" file not found.')
                    continue
                print(f'Content of "{cmdv[0]}":')
                print(ret)
            case "ls":
                ret = fs.ls()
                print(f'Content of current directory:')
                print(*ret, sep=', ', end='\n\n')
            case "help":
                print('''Usage:
mkdir <dir> : creates dir
touch <file> : creates file if not exists, update last modified time if exists
write <file> <data> : writes data to file
read <file> : reads file and prints data
ls : shows files and folders in current directory
help : prints this message
exit : exit this program
''')
            case "exit":
                exit(0)
