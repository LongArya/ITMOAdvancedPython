import os
from pprint import pprint
import time
from tqdm import tqdm
from collections import defaultdict
from typing import List, Dict, Callable
from threading import Thread
from multiprocessing import Process
import pandas as pd
import threading

SCRIPT_DIR = os.path.dirname(__file__)

BIG_NUMBER = 30
WORKERS_NUM = 10
SINGLE_WORKER_LOAD = 10
EXPERIMENT_NUM = 10


def recursive_fibonacci(n: int) -> int:
    if n <= 2:
        return 1
    return recursive_fibonacci(n - 1) + recursive_fibonacci(n - 2)


def time_fibonacci(n: int) -> None:
    start = time.time()
    recursive_fibonacci(n)
    end = time.time()
    print(f"elapsed time = {end - start} s")


def worker_foo() -> None:
    for _ in range(SINGLE_WORKER_LOAD):
        recursive_fibonacci(BIG_NUMBER)


def time_threads_strategy() -> float:
    start_time = time.time()
    threads: List[Thread] = [Thread(target=worker_foo) for _ in range(WORKERS_NUM)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    end_time = time.time()
    elapsed = end_time - start_time
    return elapsed


def time_process_strategy() -> float:
    start_time = time.time()
    processes: List[Process] = [Process(target=worker_foo) for _ in range(WORKERS_NUM)]
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()
    end_time = time.time()
    elapsed = end_time - start_time
    return elapsed


def time_sequential_strategy() -> float:
    start_time = time.time()
    for _ in range(WORKERS_NUM):
        worker_foo()
    end_time = time.time()
    elapsed = end_time - start_time
    return elapsed


def main():
    recorded_time_measurements: Dict[str, List[float]] = defaultdict(list)
    experiment_name2function: Dict[str, Callable] = {
        "sequential": time_sequential_strategy,
        "threads": time_threads_strategy,
        "processes": time_process_strategy,
    }
    for _ in tqdm(range(EXPERIMENT_NUM), desc="Running experiments"):
        for experiment_name, function in experiment_name2function.items():
            time_measurement = function()
            recorded_time_measurements[experiment_name].append(time_measurement)
    table = pd.DataFrame(
        [
            [sum(records) / len(records), min(records), max(records)]
            for records in recorded_time_measurements.values()
        ],
        columns=["avg (s)", "min (s)", "max (s)"],
        index=list(experiment_name2function.keys()),
    )
    table_repr = table.to_markdown()
    output_file = os.path.join(SCRIPT_DIR, "artifacts", "task1.txt")
    with open(output_file, "w") as f:
        f.write(f"EXPERIMENTS NUM = {EXPERIMENT_NUM}\n")
        f.write(f"FIBONACCI TARGET = {BIG_NUMBER}\n")
        f.write(f"TABLE:\n")
        f.write(table_repr)


if __name__ == "__main__":
    main()
