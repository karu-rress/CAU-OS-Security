import time

# List of processes with their names and durations
processes = [
    ("Process 1", 3),
    ("Process 2", 1),
    ("Process 3", 4),
    ("Process 4", 2)
]

def fifo_scheduling(processes):
    print("FIFO Scheduling")
    # Run processes in the order they are listed
    for process, duration in processes:
        print(f"{process} is running for {duration} seconds")
        time.sleep(duration)
    print("All processes in FIFO completed.\n")

if __name__ == '__main__':
    # Execute FIFO scheduling
    fifo_scheduling(processes)
