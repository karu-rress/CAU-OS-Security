import threading
import time

total = 0
lock = threading.Lock()

def increment_n_times(n):
    global total
    for i in range(n):
        time.sleep(0.0001)
        total += 1

def safe_increment_n_times(n):
    global total
    for i in range(n):
        lock.acquire()
        time.sleep(0.001)
        total += 1
        lock.release()

def increment_in_x_threads(x, func, n):
    threads = [threading.Thread(target=func, args=(n,)) for i in range(x)]
    global total
    total = 0
    begin = time.time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('finished in {}s.\ntotal: {}\nexpected: {}\ndifference: {} ({} %)'
           .format(time.time()-begin, total, n*x, n*x-total, 100-total/n/x*100))
    
print('unsafe:')
increment_in_x_threads(70, increment_n_times, 100000)

print('\nwith locks:')
increment_in_x_threads(70, safe_increment_n_times, 100000)