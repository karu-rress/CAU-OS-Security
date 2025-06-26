# import threading library
import threading

# Create two locks (mutexes)
lock1 = threading.Lock()
lock2 = threading.Lock()

def thread1():
    print('Thread 1: Attempting to acquire lock1')
    with lock1:
        print('Thread 1 <lock1>: Acquired lock1')
        threading.Event().wait(1) # similar to time.sleep(1)

        print('Thread 1 <lock1>: Attempting to acquire lock2')
        with lock2:
            print('Thread 1 <lock1, lock2>: Acquired lock2')

def thread2():
    print('Thread 2: Attempting to acquire lock2')
    with lock2:
        print('Thread 2 <lock2>: Acquired lock2')
        threading.Event().wait(1) # similar to time.sleep(1)

        print('Thread 2 <lock2>: Attempting to acquire lock1')
        with lock1:
            print('Thread 2 <lock2, lock1>: Acquired lock1')

if __name__ == '__main__':
    # Create two threads
    t1 = threading.Thread(target=thread1)
    t2 = threading.Thread(target=thread2)

    # Start threads
    t1.start()
    t2.start()

    # Wait for both threads to finish
    t1.join()
    t2.join()

    # this line will NEVER be reached
    print('Program finished.')