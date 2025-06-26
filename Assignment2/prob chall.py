import time
from dataclasses import dataclass

@dataclass
class Process:
    name: str
    arrival_time: int
    burst_time: int
    allotted_time: int = None

processes: list[Process] = [
    Process("Process 1", 0, 6),
    Process("Process 2", 1, 8),
    Process("Process 3", 2, 4),
    Process("Process 4", 3, 6),
    Process("Process 5", 4, 7),
    Process("Process 6", 5, 8),
]

TICK = 0.1
TIME_PERIOD = 15
time_slices = [1, 2, 4]


def mlfq(processes, time_slices):
    current_time = 0
    ready_queues: list[list[Process]] = [[] for _ in time_slices]

    current_quantum = 0

    while True:
        for process in processes:
            if process.arrival_time == current_time:
                ready_queues[0].append(process) # Add to the first queue

        # Iterate through the queues by priority
        for i, queue in enumerate(ready_queues):
            if queue:
                process: Process = queue[0]
                if process.allotted_time is None:
                    process.allotted_time = time_slices[i]

                print(f"\n[{current_time:02}-{current_time+1:02}s]: {process.name} is running in Queue{i + 1}", end='')

                current_quantum += 1
                process.burst_time -= 1
                process.allotted_time -= 1

                if process.burst_time == 0:
                    queue.pop(0)
                    current_quantum = 0
                    print(f' ====> {process.name} completed!', end='')
                elif current_quantum == time_slices[i] or process.allotted_time == 0:
                    process.allotted_time = None
                    queue.pop(0)
                    if i + 1 < len(time_slices):
                        ready_queues[i + 1].append(process)
                    else:
                        ready_queues[i].append(process)
                    current_quantum = 0

                break

        time.sleep(TICK)
        current_time += 1

        # After some time period S, move all the jobs in the system to the topmost queue
        if current_time % TIME_PERIOD == 0:
            for queue in ready_queues[1:]:
                if queue:
                    ready_queues[0].extend(queue)
                    queue.clear()
            print('\n***** All processes moved to the topmost queue!', end='')

        if all(not q for q in ready_queues):
            print('\nAll processes are completed! Exiting...')
            break

if __name__ == '__main__':
    mlfq(processes, time_slices)