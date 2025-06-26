"""

    Problem 1

    Generalize the signal pattern so that it works both ways.
    Thread A has to wait for Thread B and vice versa.

    We want to guarantee that a1 happens before b2 and b1 happens
    before a2.

"""

# import necessary libraries
import threading
from colorama import init, Fore

# create two semaphores with S=0
s1 = threading.Semaphore(0)
s2 = threading.Semaphore(0)

# mutex for synchronized print
mutex = threading.Lock()

# synchronized print function
def print_mutex(print_str, **kwargs):
    with mutex:
        print(print_str, **kwargs)

def thread_a():
    print_mutex(Fore.LIGHTMAGENTA_EX + 'statement a1')
    # if s2 is not acquired in 3 seconds
    # we can assume that there is a deadlock!
    if not s2.acquire(timeout=3):
        print_mutex(Fore.LIGHTMAGENTA_EX + 'Deadlock detected in thread A.')
        print_mutex(Fore.LIGHTMAGENTA_EX + 'Halting thread A.')
        return
    s1.release()
    print_mutex(Fore.LIGHTMAGENTA_EX + 'statement a2')

def thread_b():
    print_mutex(Fore.LIGHTCYAN_EX + 'statement b1')
    if not s1.acquire(timeout=3):
        print_mutex(Fore.LIGHTCYAN_EX + 'Deadlock detected in thread B.')
        print_mutex(Fore.LIGHTCYAN_EX + 'Halting thread B.')
        return
    s2.release()
    print_mutex(Fore.LIGHTCYAN_EX + 'statement b2')

if __name__ == '__main__':
    init()
    
    ta = threading.Thread(target=thread_a)
    tb = threading.Thread(target=thread_b)

    ta.start()
    tb.start()

    ta.join()
    tb.join()