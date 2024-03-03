import os
import sys
from pydantic import FilePath
from dataclasses import dataclass
from typing import List


@dataclass
class WCLikeStats:
    word_number: int
    lines_number: int
    symbols_number: int

    def __str__(self) -> str:
        return f" {self.lines_number} {self.word_number} {self.symbols_number}"

    def __add__(self, other: "WCLikeStats") -> "WCLikeStats":
        sum = WCLikeStats(
            word_number=self.word_number + other.word_number,
            lines_number=self.lines_number + other.lines_number,
            symbols_number=self.symbols_number + other.symbols_number,
        )
        return sum


def collect_wc_stats_from_lines(text_lines: List[str]) -> WCLikeStats:
    word_number = 0
    symbols_number = 0
    for line in text_lines:
        words = line.rstrip().split(" ")
        word_number += len(words)
        symbols_number += len(line)

    stats = WCLikeStats(
        word_number=word_number,
        lines_number=len(text_lines),
        symbols_number=symbols_number,
    )
    return stats


def collect_wc_stats_from_file(file_path: FilePath) -> WCLikeStats:
    with open(file_path, "r") as f:
        file_lines = f.readlines()
    return collect_wc_stats_from_lines(file_lines)


def run_wc_scenario_on_files(user_input: List[str]) -> None:
    total_stats = WCLikeStats(lines_number=0, word_number=0, symbols_number=0)
    for file_path in user_input:
        if not os.path.isfile(file_path):
            print(f"{file_path}: No such file or directory")
        file_stat = collect_wc_stats_from_file(file_path)
        total_stats += file_stat
        print(f"{file_stat} {file_path}")
    if len(user_input) > 1:
        print(f"{total_stats} total")


def run_wc_scenario_on_user_input() -> None:
    collected_user_lines: List[str] = []
    try:
        while True:
            user_line = input()
            user_line += "\n"
            collected_user_lines.append(user_line)
    except EOFError:
        stat = collect_wc_stats_from_lines(collected_user_lines)
        print(stat)


def read_user_input_files() -> List[str]:
    return sys.argv[1:]


def main() -> None:
    user_files = read_user_input_files()
    if user_files:
        run_wc_scenario_on_files(user_files)
    else:
        run_wc_scenario_on_user_input()


if __name__ == "__main__":
    main()
