# import threading library
from concurrent.futures import ThreadPoolExecutor
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

    # Create a thread pool
    with ThreadPoolExecutor(max_workers=3) as executor:
        for _ in range(executor._max_workers):
            executor.submit(worker)

        # This count includes the main thread
        print('Current number of threads (including the main thread):', threading.active_count())

    end_time = time.time()
    print('Execution time for parallelism example:', end_time - start_time)