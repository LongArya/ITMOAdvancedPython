import click
import sys
import os
from pydantic import FilePath
from typing import Optional, List


def extract_user_input_from_arguments() -> Optional[str]:
    user_arguments = sys.argv[1:]
    if len(user_arguments) > 1:
        raise ValueError("Invalid usage, 1 or 0 arguments should be provided")
    if len(user_arguments) == 1:
        return user_arguments[0]
    return None


def run_on_file_path(file_path: FilePath) -> None:
    with open(file_path, "r") as f:
        data: List[str] = f.readlines()
    for line_index, line in enumerate(data, start=1):
        print(f"\t{line_index} {line}")


def run_on_lines_from_user() -> None:
    line_index = 1
    while True:
        line = input()
        print(f"\t{line_index} {line}")
        line_index += 1


def main() -> None:
    try:
        user_file_path: Optional[str] = extract_user_input_from_arguments()
    except ValueError as error:
        print(error)
        return

    if user_file_path is not None:
        if not os.path.isfile(user_file_path):
            print(f"{user_file_path}: No such file or directory")
            return
        run_on_file_path(user_file_path)
    else:
        try:
            run_on_lines_from_user()
        except KeyboardInterrupt:
            print("\n")


if __name__ == "__main__":
    main()
