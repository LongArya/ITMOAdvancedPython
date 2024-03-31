import os
from typing import List
from pydantic import FilePath
import numpy as np


RANDOM_SEED = 0
TEST_MATRIX_SHAPE = (10, 10)


class MatrixTask1:
    def __init__(self, data: List[List[float]]) -> None:
        self._data = data
        self._height, self._width = len(data), len(data[0])

    def _check_shapes_for_elementwise_ops(
        self, mat1: "MatrixTask1", mat2: "MatrixTask1"
    ) -> bool:
        return mat1._height == mat2._height and mat1._width == mat2._width

    def _check_shapes_for_matmul(
        self, mat1: "MatrixTask1", mat2: "MatrixTask1"
    ) -> bool:
        return mat1._width == mat2._height

    def __add__(self, other: "MatrixTask1") -> "MatrixTask1":
        if not self._check_shapes_for_elementwise_ops(self, other):
            raise ValueError(
                f"Unsupported shapes for +, ({self._height}x{self._width}) and ({other._height}x{other._width})"
            )
        output_matrix_data = [
            [0 for _ in range(self._width)] for _ in range(self._height)
        ]
        for i in range(self._height):
            for j in range(self._width):
                output_matrix_data[i][j] = self._data[i][j] + other._data[i][j]
        return MatrixTask1(output_matrix_data)

    def __mul__(self, other: "MatrixTask1") -> "MatrixTask1":
        if not self._check_shapes_for_elementwise_ops(self, other):
            raise ValueError(
                f"Unsupported shapes for *, ({self._height}x{self._width}) and ({other._height}x{other._width})"
            )
        output_matrix_data = [
            [0 for _ in range(self._width)] for _ in range(self._height)
        ]
        for i in range(self._height):
            for j in range(self._width):
                output_matrix_data[i][j] = self._data[i][j] * other._data[i][j]

        return MatrixTask1(output_matrix_data)

    def __matmul__(self, other: "MatrixTask1") -> "MatrixTask1":
        if not self._check_shapes_for_matmul(self, other):
            raise ValueError(
                f"Unsupported shapes for @, ({self._height}x{self._width}) and ({other._height}x{other._width})"
            )
        output_matrix_data = [
            [0 for _ in range(other._width)] for _ in range(self._height)
        ]
        for out_col_index in range(self._height):
            for out_row_index in range(other._width):
                output_element = 0
                for i in range(self._width):
                    output_element += (
                        self._data[out_col_index][i] * other._data[i][out_row_index]
                    )
                output_matrix_data[out_col_index][out_row_index] = output_element

        return MatrixTask1(output_matrix_data)

    def __str__(self) -> str:
        row_formatter = lambda row: " ".join(map(lambda value: f"{value:4d}", row))
        # pretty_print_data = "\n".join(" ".join(map(str, row)) for row in self._data)
        pretty_print_data = "\n".join(row_formatter(row) for row in self._data)
        matrix_pretty_print = (
            f"Matrix {self._height}x{self._width}\n----\n"
            + pretty_print_data
            + "\n----"
        )
        return matrix_pretty_print


def generate_random_test_matrix() -> MatrixTask1:
    data = np.random.randint(0, 10, TEST_MATRIX_SHAPE)
    data_as_list = list(map(list, data))
    return MatrixTask1(data_as_list)


def write_matrices_to_file(
    matrices: List[MatrixTask1], matrices_titles: List[str], file_name: FilePath
):
    with open(file_name, "w") as f:
        for title, matrix in zip(matrices_titles, matrices):
            f.write(f"{title}\n")
            f.write(f"{matrix}\n")


def run_tests():
    script_dir = os.path.dirname(__file__)
    artifacts_dir = os.path.join(script_dir, "artifacts", "3.1")
    os.makedirs(artifacts_dir, exist_ok=True)

    np.random.seed(RANDOM_SEED)
    matrix1 = generate_random_test_matrix()
    matrix2 = generate_random_test_matrix()
    write_matrices_to_file(
        matrices=[matrix1, matrix2, matrix1 + matrix2],
        matrices_titles=["MATRIX1", "MATRIX2", "MATRIX1 + MATRIX2"],
        file_name=os.path.join(artifacts_dir, "matrix+.txt"),
    )
    write_matrices_to_file(
        matrices=[matrix1, matrix2, matrix1 * matrix2],
        matrices_titles=["MATRIX1", "MATRIX2", "MATRIX1 * MATRIX2"],
        file_name=os.path.join(artifacts_dir, "matrix*.txt"),
    )
    write_matrices_to_file(
        matrices=[matrix1, matrix2, matrix1 @ matrix2],
        matrices_titles=["MATRIX1", "MATRIX2", "MATRIX1 @ MATRIX2"],
        file_name=os.path.join(artifacts_dir, "matrix@.txt"),
    )


if __name__ == "__main__":
    run_tests()
