import time

processes = [
    ["Process 1", 0, 3],
    ["Process 2", 0, 1],
    ["Process 3", 0, 4],
    ["Process 4", 0, 2],
]

def stcf(processes):
    print('Shortest Time to Completion First Scheduling')

    current_time = 0
    ready_queue = []

    while True:
        for process in processes:
            if process[1] == current_time:
                ready_queue.append(process)

        time.sleep(0.1)
        current_time += 1

        if ready_queue:
            shortest = min(ready_queue, key=lambda x: x[2])
            shortest[2] -= 1

            print(f'[{current_time:02}s]: {shortest[0]} is running')

            if shortest[2] == 0:
                ready_queue.remove(shortest)

        else:
            print('All processes have been completed! Exiting...')
            break

if __name__ == '__main__':
    stcf(processes)