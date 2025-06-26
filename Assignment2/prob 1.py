# Import necessary libraries
import time
from dataclasses import dataclass

# Define a Job class
@dataclass
class Job:
    name: str
    arrival_time: int
    burst_time: int
    priority: int
    turnaround_time: int = 0

# A tick for sleep function
TICK = 0.1

# Define the time slices (and number of queues)
time_slices = [1, 2, 4]

# Define the jobs
# Priority: 1 - Urgent, 2 - Medium, 3 - Low
jobs = [
    Job("Job 1", 0, 3, 3),
    Job("Job 2", 1, 1, 2),
    Job("Job 3", 2, 4, 1),
    Job("Job 4", 3, 2, 3),
    Job("Job 5", 4, 3, 2),
    Job("Job 6", 5, 1, 1),
    Job("Job 7", 6, 4, 3),
    Job("Job 8", 7, 2, 2),
]

# Run the scheduling process
def process():
    current_time: int = 0
    ready_queues: list[list[Job]] = [[] for _ in time_slices]
    current_quantum: int = 0

    while True:
        # If job has arrived, add it to the first queue
        for job in jobs:
            if job.arrival_time == current_time:
                ready_queues[0].append(job)
                if job.priority == 1:
                    print(f'******* URGENT JOB {job.name} ARRIVED *******')

        for queue in ready_queues:
            for job in queue:
                job.turnaround_time += 1

        # Iterate over the queues
        for i, queue in enumerate(ready_queues):
            # If the queue is not empty
            if queue:
                job: Job = queue[0]
                print(f"[{current_time:02}-{current_time+1:02}s]: {job.name} is running in Queue{i + 1}")

                current_quantum += 1
                job.burst_time -= 1

                if job.burst_time == 0:
                    queue.pop(0)
                    current_quantum = 0
                    if job.priority == 1:
                        print(f'******* URGENT JOB {job.name} COMPLETED (TT: {job.turnaround_time})*******')
                elif current_quantum == time_slices[i]:
                    queue.pop(0)
                    if i + 1 < len(time_slices):# and job.priority - 1 > i:
                        ready_queues[i + 1].append(job)
                    else:
                        ready_queues[i].append(job)
                    current_quantum = 0
                break

        # Sleep for a tick
        time.sleep(TICK)
        current_time += 1

        # If all queues are empty, exit
        if all(not q for q in ready_queues):
            print('All jobs are completed! Exiting...')
            break

if __name__ == "__main__":
    process()