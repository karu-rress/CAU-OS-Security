import time

process_list = [
        ["Process 1", 0, 3],
        ["Process 2", 1, 1],
        ["Process 3", 2, 4],
        ["Process 4", 3, 2],
]

def psjf(processes):
    print("Preemptive SJF Scheduling")

    current_time = 0
    process_queue = []

    while True:
        for process in processes:
            if process[1] <= current_time:
                processes.remove(process)
                process_queue.append(process)

        time.sleep(0.5)
        current_time += 1

        if process_queue:
            shortest = min(process_queue, key=lambda x: x[2])

            print(f'[{current_time:02}s]: {shortest[0]} is running.')
            shortest[2] -= 1

            if shortest[2] == 0:
                process_queue.remove(shortest)

        else:
            print('All processes are completed! Exiting...')
            return


if __name__ == '__main__':
    psjf(process_list)