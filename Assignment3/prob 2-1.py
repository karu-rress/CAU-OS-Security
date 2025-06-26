"""

    Assignment 3
    Real-world example of deadlock

"""

# import necessary libraries
import threading
import random
import time
from abc import ABC, abstractmethod # Abstract Base Class
from colorama import init, Fore

# File class : simulates a file
class File:
    def __init__(self, name):
        self.name = name # file name
        self.lock = threading.Lock()
        self.data = ''

    # read method : read the file
    def read(self) -> str:
        time.sleep(1)
        return self.data

    # write method : write the file
    def write(self, data):
        time.sleep(1)
        self.data = data

# Process class : simulates a process
class Process(ABC, threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    # to be implemented by subclasses
    @abstractmethod
    def run(self):
        pass

    # read the given file
    def read_file(self, file: File):
        color = Fore.LIGHTCYAN_EX if self.name == 'Process A' else Fore.LIGHTMAGENTA_EX

        print(color + f"{self.name} is reading {file.name} ...")
        ret = file.read()
        print(color + f"{self.name} read '{ret}' from {file.name}")

    # write to the given file
    def write_file(self, file: File, data: str):
        color = Fore.LIGHTCYAN_EX if self.name == 'Process A' else Fore.LIGHTMAGENTA_EX

        print(color + f"{self.name} is writing '{data}' to {file.name} ...")
        file.write(data)
        print(color + f"{self.name} wrote {file.name}")


class ProcessA(Process):
    def __init__(self, file1, file2):
        super().__init__('Process A')
        self.file1: File = file1
        self.file2: File = file2

    def run(self):
        print(Fore.LIGHTCYAN_EX + 'Process A is running ...')
        # Step 1: Acquire file1's lock
        print(Fore.LIGHTCYAN_EX + f"{self.name} attempting to lock {self.file1.name}")
        with self.file1.lock:
            print(Fore.LIGHTCYAN_EX + f"{self.name} locked {self.file1.name}")
            self.read_file(self.file1)

            # Step 2: Attempt to acquire file2's lock
            print(Fore.LIGHTCYAN_EX + f"{self.name} attempting to lock {self.file2.name}")
            with self.file2.lock:
                print(Fore.LIGHTCYAN_EX + f"{self.name} locked {self.file2.name}")
                self.write_file(self.file2, "Data from Process A")


class ProcessB(Process):
    def __init__(self, file1, file2):
        super().__init__('Process B')
        self.file1: File = file1
        self.file2: File = file2

    def run(self):
        print(Fore.LIGHTMAGENTA_EX + 'Process B is running ...')
        # Step 1: Acquire file2's lock
        print(Fore.LIGHTMAGENTA_EX + f"{self.name} attempting to lock {self.file2.name}")
        with self.file2.lock:
            print(Fore.LIGHTMAGENTA_EX + f"{self.name} locked {self.file2.name}")
            self.read_file(self.file1)

            # Step 2: Attempt to acquire file1's lock
            print(Fore.LIGHTMAGENTA_EX + f"{self.name} attempting to lock {self.file1.name}")
            with self.file1.lock:
                print(Fore.LIGHTMAGENTA_EX + f"{self.name} locked {self.file1.name}")
                self.write_file(self.file1, "Data from Process B")


if __name__ == '__main__':
    init()

    # create two files
    file1 = File('file1.txt')
    file2 = File('file2.txt')

    # create two processes
    processA = ProcessA(file1, file2)
    processB = ProcessB(file1, file2)

    processA.start()
    processB.start()

    processA.join()
    processB.join()