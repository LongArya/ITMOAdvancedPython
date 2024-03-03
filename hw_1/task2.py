import os
import sys
from pydantic import FilePath
from typing import List


LAST_N_LINES_FROM_FILE = 10
LAST_N_LINES_FROM_STDIN = 17


def imitate_tail_output_on_file(
    file_path: FilePath, tail_len: int = LAST_N_LINES_FROM_FILE
) -> None:
    with open(file_path, "r") as f:
        file_content = f.readlines()
    tail_content = file_content[-tail_len:]
    print("".join(tail_content))


def read_user_input_files() -> List[str]:
    return sys.argv[1:]


def run_tail_scenario_on_files(user_input_files: List[str]) -> None:
    should_print_file_names = len(user_input_files) > 1
    for user_file in user_input_files:
        if not os.path.isfile(user_file):
            print("")
            continue
        if should_print_file_names:
            print(f"==> {user_file} <==")
        imitate_tail_output_on_file(user_file)


def run_tail_scenario_on_user_input(tail_len: int = LAST_N_LINES_FROM_STDIN):
    collected_user_lines: List[str] = []
    try:
        while True:
            user_line = input()
            collected_user_lines.append(user_line)
    except EOFError:
        tail_content = collected_user_lines[-tail_len:]
        print("\n".join(tail_content))


def main() -> None:
    user_files = read_user_input_files()
    if user_files:
        run_tail_scenario_on_files(user_files)
    else:
        run_tail_scenario_on_user_input()


if __name__ == "__main__":
    main()
