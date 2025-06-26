import threading
import time

# Note: use ZERO semaphore
s1 = threading.Semaphore(0)
s2 = threading.Semaphore(0)

def work1():
    print('Work A started!')
    time.sleep(1)
    print('Work A ended! Now you can start Work B')
    s1.release() # Release the semaphore s1, so that Work B can start

def work2():
    s1.acquire()
    print('Work B started!')
    time.sleep(1)
    print('Work B ended! Now you can start Work C')
    s2.release() # Release the semaphore s2, so that Work C can start
    
def work3():
    s2.acquire()
    print('Work C started!')
    time.sleep(1)
    print('Work C ended!')


if __name__ == '__main__':
    # Create threads
    ta = threading.Thread(target=work1)
    tb = threading.Thread(target=work2)
    tc = threading.Thread(target=work3)

    # Called: t3 -> t2 -> t1
    # Actual execution with semaphore: t1 -> t2 -> t3
    # Re-order the call sequance as you want, and check the output
    tc.start()
    time.sleep(0.5) # Ensure that t2 is called after t3
    tb.start()
    time.sleep(0.5) # Ensure that t1 is called after t2
    ta.start()

    for t in [ta, tb, tc]:
        t.join()

    print('All work done!')