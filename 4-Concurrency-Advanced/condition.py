import threading
import time

shared_resources = []

condition = threading.Condition()

def consumer():
    for i in range(5):
        with condition:
            if not shared_resources:
                print('*** Consumer is waiting...')
                condition.wait()
            print(f'*** Consumer consumed {shared_resources.pop(0)}')

        time.sleep(2)

def producer():
    for i in range(5):
        with condition:
            shared_resources.append(i + 1)
            print(f'Producer produced {i + 1}')
            condition.notify()

        time.sleep(1)

if __name__ == '__main__':
    consumer_thread = threading.Thread(target=consumer)
    producer_thread = threading.Thread(target=producer)

    consumer_thread.start()
    producer_thread.start()

    consumer_thread.join()
    producer_thread.join()