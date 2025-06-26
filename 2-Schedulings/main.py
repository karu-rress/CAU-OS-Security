from MLFQ import mlfq
from RR import rr
from STCF import stcf

processes = [
    ["Process 1", 0, 3],
    ["Process 2", 0, 1],
    ["Process 3", 0, 4],
    ["Process 4", 0, 2],
]

if __name__ == '__main__':
    rr(processes, time_quantum=1)
    stcf(processes)
    # mlfq()