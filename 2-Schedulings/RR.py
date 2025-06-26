import time

processes = [
    ["Process 1", 0, 3],
    ["Process 2", 0, 1],
    ["Process 3", 0, 4],
    ["Process 4", 0, 2],
]

def rr(processes, time_quantum):
    print('Round Robin Scheduling')

    current_time = 0
    current_quantum = 0
    ready_queue = []

    while True:
        for process in processes:
            if process[1] == current_time:
                ready_queue.append(process)

        time.sleep(0.1)
        current_time += 1

        if ready_queue:
            process = ready_queue[0]
            current_quantum += 1
            process[2] -= 1

            print(f'[{current_time-1:02}-{current_time:02}s]{process[0]} is running')

            if process[2] == 0:
                ready_queue.pop(0)
                current_quantum = 0
            elif current_quantum == time_quantum:
                ready_queue.pop(0)
                ready_queue.append(process)
                current_quantum = 0

        if len(ready_queue) == 0:
            print('All processes have been completed')
            break

if __name__ == '__main__':
    rr(processes, time_quantum=1)
