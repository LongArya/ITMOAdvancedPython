import os
from pydantic import FilePath
from pdflatex import PDFLaTeX
from latex_module.latex_utils import (
    create_latex_table,
    get_graphix_include_instruction,
    latex_img_with_includegraphix,
    wrap_latex_content_as_document,
)


EXAMPLE_TABLE = [["A", "B"], ["C", "D"]]
SCRIPT_DIR = os.path.dirname(__file__)
ARTIFACTS_DIR = os.path.join(SCRIPT_DIR, "artifacts")
os.makedirs(ARTIFACTS_DIR, exist_ok=True)
TABLE_TEX_OUTPUT = os.path.join(ARTIFACTS_DIR, "table.tex")
TABLE_AND_IMG_TEX_OUTPUT = os.path.join(ARTIFACTS_DIR, "table_and_image.tex")
TEX_IMAGE_PATH = os.path.join(SCRIPT_DIR, "assets", "real.jpg")


def generate_latex_document_with_table() -> None:
    latex_table = create_latex_table(EXAMPLE_TABLE)
    latex_include = get_graphix_include_instruction()
    latex_content = "\n".join([latex_table])
    latex_document = wrap_latex_content_as_document(latex_content)
    doc_class_statement = "\\documentclass{article}\n"
    latex_document = "\n".join([doc_class_statement, latex_include, latex_document])
    with open(TABLE_TEX_OUTPUT, "w") as f:
        f.write(latex_document)


def generate_latex_document_with_table_and_img() -> None:
    latex_table = create_latex_table(EXAMPLE_TABLE)
    latex_include = get_graphix_include_instruction()
    latex_img = latex_img_with_includegraphix(TEX_IMAGE_PATH)
    latex_content = "\n".join([latex_img, latex_table])
    latex_document = wrap_latex_content_as_document(latex_content)
    doc_class_statement = "\\documentclass{article}\n"
    latex_document = "\n".join([doc_class_statement, latex_include, latex_document])
    with open(TABLE_AND_IMG_TEX_OUTPUT, "w") as f:
        f.write(latex_document)


def generate_pdf_from_tex(tex_path: FilePath) -> None:
    if not os.path.exists(tex_path):
        raise ValueError(f"Missing file {tex_path}")
    pdfl = PDFLaTeX.from_texfile(tex_path)
    pdfl.set_output_directory(os.path.dirname(tex_path))
    pdf = pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)


def table_tex_pipeline() -> None:
    generate_latex_document_with_table()
    generate_pdf_from_tex(TABLE_TEX_OUTPUT)


def table_and_image_pipeline() -> None:
    generate_latex_document_with_table_and_img()
    generate_pdf_from_tex(TABLE_AND_IMG_TEX_OUTPUT)


if __name__ == "__main__":
    print("GENERATING LATEX PDF")
    table_tex_pipeline()
    table_and_image_pipeline()
