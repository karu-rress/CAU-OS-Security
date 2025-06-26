# import threading library
import threading
import time

# Define a function for the thread
def worker():
    # Print thread id and name
    print(f'Thread #{threading.get_native_id()} started. ({threading.current_thread().name})')
    time.sleep(1)
    print(f'Thread #{threading.get_native_id()} finished. ({threading.current_thread().name})')

if __name__ == '__main__':
    start_time = time.time()

    # Create threads and start them
    for _ in range(3):
        thread = threading.Thread(target=worker)
        thread.start()

    # This count includes the main thread
    print('Current number of threads (including the main thread):', threading.active_count())

    # Wait for all threads to finish
    for thread in threading.enumerate():
        # 'Join' only if the thread is not the main thread
        if thread is not threading.main_thread():
            thread.join()

    end_time = time.time()
    print('Execution time for concurrency example:', end_time - start_time)