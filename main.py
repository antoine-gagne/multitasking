"""An of multithreading vs multiprocessing.

Adapted from https://code.tutsplus.com/articles/introduction-to-parallel-and-concurrent-programming-in-python--cms-28612
"""

import os
import time
import threading
from multiprocessing import Pool
 
NUM_WORKERS = 4

def non_blocking_fct(_):
    """Execute a non-blocking action.
    
    A non-blocking action is something that doesn't require Python's attention
    and can execute in the background.
    """
    time.sleep(1)
 
 
def blocking_fct(_):
    """Execute a blocking action.

    A blocking action is something that requires Python's attention.
    """
    x = 0
    while x < 10000000:
        x += 1

if __name__ == '__main__':

    print("Execution of non-blocking tasks")

    # Run tasks serially
    start_time = time.time()
    for _ in range(NUM_WORKERS):
        non_blocking_fct(_)
    end_time = time.time()
    print("Serial time={}".format(end_time - start_time))


    # Run tasks using threads
    start_time = time.time()
    threads = [threading.Thread(target=non_blocking_fct, args=(_,)) for _ in range(NUM_WORKERS)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]  # Wait for everything to finish
    end_time = time.time()
    print("Threading time={}".format(end_time - start_time))

    # Run tasks using processes
    start_time = time.time()
    pool = Pool(processes=4)
    pool.map(non_blocking_fct, [_, _, _, _,])
    end_time = time.time()
    print("multiprocessing time={}".format(end_time - start_time))

    print("")
    print("Execution of blocking tasks")

    start_time = time.time()
    for _ in range(NUM_WORKERS):
        blocking_fct(_)
    end_time = time.time()

    print("Serial time={}".format(end_time - start_time))

    start_time = time.time()
    threads = [threading.Thread(target=blocking_fct, args=(_,)) for _ in range(NUM_WORKERS)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]  # Wait for everything to finish
    end_time = time.time()

    print("Threading time={}".format(end_time - start_time))

    start_time = time.time()
    pool = Pool(processes=4)
    pool.map(blocking_fct, [_, _, _, _,])
    end_time = time.time()
    print("multiprocessing time={}".format(end_time - start_time))


"""
Typical output:

Execution of non-blocking tasks
Serial time=4.01600003242
Threading time=1.0150001049
Multiprocessing time=1.10500001907

Execution of blocking tasks
Serial time=1.40599989891
Threading time=5.13499999046
Multiprocessing time=0.421999931335

Analysis:
For non-blocking tasks, threading and multiprocessing give similar results,
since all the waiting can be handled in the background. Multiprocessing does 
perform a bit worse since there is overhead associated with spawning 
additionnal processes. They both perform much faster than if the execution was
made serially though.

For blocking tasks, threading performs even worse than serial execution, because
Python jumping back and forth between threads slows down the execution.
Mutliprocessing, however, cuts down the time significantly.
"""