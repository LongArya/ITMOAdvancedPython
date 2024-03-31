import os
from typing import List
import numpy as np
from io import TextIOWrapper
from pydantic import FilePath

RANDOM_SEED = 0
TEST_MATRIX_SHAPE = (10, 10)


class PrettyPrintMixin:
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


class PropertiesMixin:
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width


class FileWriterMixin:
    def write_to_file(self, file_path: FilePath, opening_mode: str = "w") -> None:
        with open(file_path, opening_mode) as f:
            f.write(f"{self}\n")

    def write_to_opened_file(self, f: TextIOWrapper) -> None:
        f.write(f"{self}\n")


class MatrixTask2(
    np.lib.mixins.NDArrayOperatorsMixin,
    PrettyPrintMixin,
    PropertiesMixin,
    FileWriterMixin,
):
    def __init__(self, data: List[List[float]]):
        self._data = data
        self._height, self._width = len(data), len(data[0])

    # One might also consider adding the built-in list type to this
    # list, to support operations like np.add(array_like, list)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get("out", ())
        for x in inputs + out:
            if not isinstance(x, MatrixTask2):
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        x: MatrixTask2
        inputs = tuple(x._data for x in inputs)
        if out:
            kwargs["out"] = tuple(
                x._data if isinstance(x, MatrixTask2) else x for x in out
            )
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == "at":
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self._data)


def write_matrices_to_file(
    matrices: List[MatrixTask2], matrices_titles: List[str], file_name: FilePath
):
    with open(file_name, "w") as f:
        for title, matrix in zip(matrices_titles, matrices):
            f.write(f"{title}\n")
            f.write(f"{matrix}\n")


def generate_random_test_matrix() -> MatrixTask2:
    data = np.random.randint(0, 10, TEST_MATRIX_SHAPE)
    data_as_list = list(map(list, data))
    return MatrixTask2(data_as_list)


def run_tests():
    script_dir = os.path.dirname(__file__)
    artifacts_dir = os.path.join(script_dir, "artifacts", "3.2")
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
