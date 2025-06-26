import threading
import time

thread_queue: list[threading.Thread] = []   # waiting thread queue
S = 3                                       # number of threads that can enter critical section
condition = threading.Condition()           # to use wait() and notify()

def wait():
    global S
    S -= 1
    if S < 0:
        thread_queue.append(threading.current_thread())
        print(f'Thread {thread_queue[-1].name} parked! Total parked: {-S}')
        with condition:
            condition.wait()

def post():
    global S
    S += 1
    if S <= 0 and thread_queue:
        thread_to_unpark = thread_queue.pop(0)
        with condition:
            condition.notify()
        print(f'Thread {thread_to_unpark.name} unparked! Total parked: {-S}')

def task():
    thrd = threading.current_thread()
    print(f'Thread {thrd.name} attempting to enter critical section')
    wait()
    print(f'Thread {thrd.name} entered critical section')
    time.sleep(2)                               # Simulate critical section
    print(f'Thread {thrd.name} exiting critical section')
    post()
    

if __name__ == '__main__':
    for i in range(6):
        threading.Thread(target=task, name=chr(65+i)).start()

    for t in threading.enumerate():
        if t != threading.main_thread():
            t.join()

    print('All threads have completed.')