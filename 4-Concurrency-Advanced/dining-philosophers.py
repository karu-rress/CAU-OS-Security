import threading
import time
import sys

print = sys.stdout.write

forks = [threading.Lock() for _ in range(5)]

def philosopher(phil_id, left_fork, right_fork):
    while True:
        print(f'Philosopher {phil_id} is thinking.\n')
        time.sleep(1)

        with left_fork:
            print(f'Philosopher {phil_id} picked up the left fork #{forks.index(left_fork)}.\n')
            time.sleep(0.1)

            if right_fork.locked():
                # print(f'Philosopher {phil_id} put down the left fork.\n')
                continue

            with right_fork:
                print(f'Philosopher {phil_id} picked up the right fork. #{forks.index(right_fork)}\n')
                print(f'Philosopher {phil_id} is eating.\n')
                time.sleep(1)

            print(f'Philosopher {phil_id} put down the right fork.\n')

        print(f'Philosopher {phil_id} put down the left fork.\n')

if __name__ == '__main__':
    philosophers = []

    for i in range(5):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % 5]

        t = threading.Thread(target=philosopher, args=(i, left_fork, right_fork))
        philosophers.append(t)

    for t in philosophers:
        t.start()

    for t in philosophers:
        t.join()