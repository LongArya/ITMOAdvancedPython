import os
import pandas as pd
from tqdm import tqdm
import time
import math
import itertools
import logging
from pprint import pprint
from threading import Thread
import concurrent.futures
from typing import List, Callable, Tuple
import datetime

CPU_COUNT = os.cpu_count()
SCRIPT_DIR = os.path.dirname(__file__)
ARTIFACTS_DIR = os.path.join(SCRIPT_DIR, "artifacts")
LOG_FILE = os.path.join(ARTIFACTS_DIR, "task2.log")
ARTIFACT_FILE = os.path.join(ARTIFACTS_DIR, "task2.txt")
RUNS_NUM_FOR_STATISTIC = 10
logging.basicConfig(filename=LOG_FILE, level=logging.INFO)
logger = logging.getLogger(__name__)


def get_cur_timestamp() -> datetime.datetime:
    return datetime.datetime.now()


def baseline_integrate(f, a, b, *, n_job=1, n_iter=10000000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def get_integration_ranges(
    integration_start: float, integration_end: float, n_jobs: int
) -> List[Tuple[float, float]]:
    ranges: List[Tuple[float, float]] = []
    step = (integration_end - integration_start) / n_jobs
    current_start = integration_start
    current_end = integration_start
    while current_end != integration_end:
        current_end = min(current_start + step, integration_end)
        ranges.append((current_start, current_end))
        current_start += step
    return ranges


def range_based_integration_worker(
    f: Callable[[float], float], a: float, b: float, n_iter: int, id: int = 0
):
    logger.info(f"STARTED INTEGRATION WORKER (ID={id}) AT {get_cur_timestamp()}")
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def thread_pool_integration(
    f: Callable[[float], float], a: float, b: float, n_jobs=1, n_iter=10000000
) -> float:
    logger.info("START INTEGRATION WITH THREADS")
    auc = 0
    integration_ranges = get_integration_ranges(a, b, n_jobs=n_jobs)
    integration_iters = [
        int(((end - start) / (b - a)) * n_iter) for start, end in integration_ranges
    ]
    integration_iters = [max(iter, 1) for iter in integration_iters]

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures: List[concurrent.futures.Future] = [
            executor.submit(
                range_based_integration_worker,
                f,
                worker_start,
                worker_end,
                worker_iter,
                id=job_id,
            )
            for job_id, ((worker_start, worker_end), worker_iter) in enumerate(
                zip(integration_ranges, integration_iters)
            )
        ]
        for future in concurrent.futures.as_completed(futures):
            integration_worker_output = future.result()
            auc += integration_worker_output
    return auc


def process_pool_integration(
    f: Callable[[float], float], a: float, b: float, n_jobs=1, n_iter=10000000
) -> float:
    logger.info("START INTEGRATION WITH PROCESSES")
    auc = 0
    integration_ranges = get_integration_ranges(a, b, n_jobs=n_jobs)
    integration_iters = [
        int(((end - start) / (b - a)) * n_iter) for start, end in integration_ranges
    ]
    integration_iters = [max(iter, 1) for iter in integration_iters]
    with concurrent.futures.ProcessPoolExecutor(max_workers=n_jobs) as executor:
        futures: List[concurrent.futures.Future] = [
            executor.submit(
                range_based_integration_worker,
                f,
                worker_start,
                worker_end,
                worker_iter,
                id=job_id,
            )
            for job_id, ((worker_start, worker_end), worker_iter) in enumerate(
                zip(integration_ranges, integration_iters)
            )
        ]
        for future in concurrent.futures.as_completed(futures):
            integration_worker_output = future.result()
            auc += integration_worker_output
    return auc


def get_avg_time_of_function_run(f: Callable, exp_num: int, *args, **kwargs):
    time_measurements: List[float] = []
    for _ in range(exp_num):
        t1 = time.time()
        output = f(*args, **kwargs)
        logger.info(f"OUTPUT = {output}")
        t2 = time.time()
        time_measurements.append(t2 - t1)
    avg_time = sum(time_measurements) / len(time_measurements)
    return avg_time


def main() -> None:
    n_iter = 10**7
    tested_workers_num = list(range(1, os.cpu_count() * 2 + 1))
    table_data = []
    for n_workers in tqdm(tested_workers_num):
        avg_thread_run = get_avg_time_of_function_run(
            thread_pool_integration,
            RUNS_NUM_FOR_STATISTIC,
            math.cos,
            0,
            math.pi / 2,
            n_jobs=n_workers,
            n_iter=n_iter,
        )
        avg_proc_num = get_avg_time_of_function_run(
            process_pool_integration,
            RUNS_NUM_FOR_STATISTIC,
            math.cos,
            0,
            math.pi / 2,
            n_jobs=n_workers,
            n_iter=n_iter,
        )
        table_data.append([avg_thread_run, avg_proc_num])
    dframe = pd.DataFrame(
        table_data,
        columns=["Threads avg time (s)", "Processes avg time (s)"],
        index=[
            f"workers num = {workers_num:02d}" for workers_num in tested_workers_num
        ],
    )
    table_repr = dframe.to_markdown()
    with open(ARTIFACT_FILE, "w") as f:
        f.write(f"CPU CORES NUM = {os.cpu_count()}\n")
        f.write(f"RESULT TABLE:\n")
        f.write(table_repr)


if __name__ == "__main__":
    main()
