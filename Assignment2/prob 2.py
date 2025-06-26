# Import necessary libraries
import time
import heapq
from dataclasses import dataclass

# Define the Seat class
@dataclass
class Seat:
    name: str
    arrival_time: int
    burst_time: int

    def __lt__(self, other):
        return self.burst_time < other.burst_time

# Tick for sleep function
TICK = 0.1

# Define the seats
seats = [
    Seat("Alice", 0, 3),
    Seat("Bob", 1, 1),
    Seat("Charlie", 2, 4),
    Seat("David", 3, 2),
    Seat("Eve", 4, 10),
    Seat("Frank", 5, 1),
    Seat("Grace", 6, 4),
    Seat("Helen", 7, 2),
]

def process():
    current_time: int = 0
    ready_queue: list[Seat] = []
    current: Seat = None

    while True:
        for seat in seats:
            # Check if the seat has started to be used
            if seat.arrival_time == current_time:
                heapq.heappush(ready_queue, seat)

        if ready_queue or current:
            if not current:
                current = heapq.heappop(ready_queue)
            current.burst_time -= 1

            print(f'\n[{current_time:02}-{current_time+1:02}s]: {current.name} is using the seat', end='')
            if current.burst_time == 0:
                print(f'    \t*** {current.name} has left!', end='')
                current = None

        else:
            print('\nAll seats have been completed! Exiting...')
            break

        time.sleep(TICK)
        current_time += 1

if __name__ == '__main__':
    process()