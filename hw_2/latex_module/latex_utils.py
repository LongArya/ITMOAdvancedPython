from typing import List, Callable
from pydantic import FilePath

# \begin{tabular}{ c c c }
#  cell1 & cell2 & cell3 \\
#  cell4 & cell5 & cell6 \\
#  cell7 & cell8 & cell9
# \end{tabular}


LATEX_ROW_SEPARATOR = " & "


def form_latex_row(row_data: List[str]) -> str:
    return LATEX_ROW_SEPARATOR.join(row_data)


def create_centered_cells_header(columns_number: int) -> str:
    return "{" + " ".join(["c"] * columns_number) + "}"


def validate_table_data_format(table_data: List[List[str]]) -> None:
    rows_lengths = [len(row) for row in table_data]
    if not all([row_len == rows_lengths[0] for row_len in rows_lengths]):
        raise ValueError("All rows should have the same amount of values")


def create_latex_table(
    table_data: List[List[str]],
    header_generator: Callable[[int], str] = create_centered_cells_header,
    row_generator: Callable[[List[str]], str] = form_latex_row,
) -> str:
    validate_table_data_format(table_data)
    columns_num = len(table_data[0])
    rows_num = len(table_data)
    latex_table_header = header_generator(columns_num)
    latex_repr = "\\begin{tabular}" + latex_table_header + "\n"
    for row_index, row in enumerate(table_data):
        latex_row = row_generator(row)
        if row_index != rows_num - 1:
            latex_row += f" \\\\"
        latex_repr += f"{latex_row}\n"
    latex_repr += "\\end{tabular}\n"
    return latex_repr


def latex_img_with_includegraphix(image_path: FilePath) -> str:
    return "\\includegraphics{" + image_path + "}"


def get_graphix_include_instruction():
    return "\\usepackage{graphicx}"


def wrap_latex_content_as_document(tex_content: str) -> str:
    tex_document = ""
    tex_document += "\\begin{document}\n"
    tex_document += tex_content
    tex_document += "\\end{document}\n"
    return tex_document
