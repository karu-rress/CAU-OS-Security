import time

processes = [
    ["Process 1", 0, 4, 'IO'],
    ["Process 2", 0, 7, 'CPU'],
    ["Process 3", 0, 3, 'IO'],
    ["Process 4", 0, 4, 'CPU'],
]

time_slices = [2, 2, 2]

def mlfq(processes, time_slices):
    current_time = 0
    ready_queues = [[] for _ in time_slices]

    current_quantum = 0

    while True:
        for process in processes:
            if process[1] == current_time:
                ready_queues[0].append(process)

        for i, queue in enumerate(ready_queues):
            if queue:
                process = queue[0]
                print(f"[{current_time:02}-{current_time+1:02}s]: {process[0]} is running in Queue{i + 1}")

                current_quantum += 1
                process[2] -= 1

                if process[3] == 'IO':
                    queue.pop(0)
                    if process[2] != 0:
                        ready_queues[0].append(process)
                    current_quantum = 0 
                else:
                    if process[2] == 0:
                        queue.pop(0)
                        current_quantum = 0
                    elif current_quantum == time_slices[i]:
                        queue.pop(0)
                        if i + 1 < len(time_slices):
                            ready_queues[i + 1].append(process)
                        else:
                            ready_queues[i].append(process)
                        current_quantum = 0
                break

        time.sleep(1)
        current_time += 1

        if all(not q for q in ready_queues):
            print('All processes are completed! Exiting...')
            break

if __name__ == '__main__':
    mlfq(processes, time_slices)