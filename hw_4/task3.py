import os
import time
import datetime
import codecs
from queue import Empty
from typing import Tuple
from multiprocessing import Process, Queue, Pipe
from dataclasses import dataclass


POISON_PILL = "done"
MSG_PROCESSING_INTERVAL_SECONDS = 5


@dataclass
class AOutputInfo:
    user_input: str
    A_output: str
    recieved_at: datetime.datetime
    processed_by_A_at: datetime.datetime


@dataclass
class BOutputInfo(AOutputInfo):
    B_output: str
    processed_by_B_at: datetime.datetime

    def __str__(self) -> str:
        info1 = f"stdin -> {self.user_input} AT {self.recieved_at.strftime('%H:%M:%S')}"
        info2 = f"A: {self.user_input} -> {self.A_output} AT {self.processed_by_A_at.strftime('%H:%M:%S')}"
        info3 = f"B: {self.A_output} -> {self.B_output} AT {self.processed_by_B_at.strftime('%H:%M:%S')}"
        repr = f"{info1}\n{info2}\n{info3}\n"
        return repr


def get_cur_timestamp() -> datetime.datetime:
    return datetime.datetime.now()


def A_worker(
    input_queue: "Queue[Tuple[str, datetime.datetime]]",
    output_queue: "Queue[AOutputInfo]",
) -> None:
    while True:
        user_input, timestamp = input_queue.get()
        if user_input == POISON_PILL:
            break
        lower_user_input = user_input.lower()
        A_output = AOutputInfo(
            user_input=user_input,
            A_output=lower_user_input,
            recieved_at=timestamp,
            processed_by_A_at=get_cur_timestamp(),
        )
        output_queue.put(A_output)
        time.sleep(MSG_PROCESSING_INTERVAL_SECONDS)
    output_queue.put(
        AOutputInfo(
            user_input=None,
            A_output=POISON_PILL,
            recieved_at=None,
            processed_by_A_at=None,
        )
    )


def B_worker(
    input_queue: "Queue[AOutputInfo]", output_queue: "Queue[BOutputInfo]"
) -> None:
    while True:
        A_output_info: AOutputInfo = input_queue.get()
        if A_output_info.A_output == POISON_PILL:
            break
        encoded_data = codecs.encode(A_output_info.A_output, "rot13")
        B_output_info = BOutputInfo(
            user_input=A_output_info.user_input,
            A_output=A_output_info.A_output,
            recieved_at=A_output_info.recieved_at,
            processed_by_A_at=A_output_info.processed_by_A_at,
            processed_by_B_at=get_cur_timestamp(),
            B_output=encoded_data,
        )
        output_queue.put(B_output_info)


def test():
    A_input_queue = Queue()
    B_input_queue = Queue()
    A_input_queue.put("A")
    A_input_queue.put("B")
    A_input_queue.put("C")
    A_input_queue.put("done")
    A_worker(A_input_queue, B_input_queue)


def main():
    A_input_queue: "Queue[AOutputInfo]" = Queue()
    B_input_queue: "Queue[BOutputInfo]" = Queue()
    user_outputs_queue: "Queue[str]" = Queue()

    A_process: Process = Process(target=A_worker, args=(A_input_queue, B_input_queue))
    B_process: Process = Process(
        target=B_worker, args=(B_input_queue, user_outputs_queue)
    )
    A_process.start()
    B_process.start()
    while (user_input := input("Print value:\n")) != POISON_PILL:
        A_input_queue.put((user_input, get_cur_timestamp()))
    A_input_queue.put((POISON_PILL, get_cur_timestamp()))
    # ===
    A_process.join()
    B_process.join()
    while True:
        try:
            print(user_outputs_queue.get(block=False))
        except Empty:
            break
    print("DONE")


if __name__ == "__main__":
    main()
