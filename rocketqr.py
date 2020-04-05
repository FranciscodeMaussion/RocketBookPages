from io import BytesIO
import click
import os
import pathlib
import PyPDF2
from reportlab.pdfgen import canvas
from consolemenu import *
from consolemenu.items import *

from constants import TYPES, OUTPUT_FILENAME, PATH, POSITION, TEMPLATE, GENERATED_PATH
from utils import class_for_name, delete_folder, qr_generate


@click.group()
def main():
    pass


@main.command(name="create")
@click.option('--quantity', '-q', prompt='Enter number of pages',
              show_default=True, default=1, type=int,
              help='The number of pages that will contain the document')
@click.option('--frame', '-f', prompt='Enter frame size',
              show_default=True, default='A4', type=click.Choice(['A4', 'Mini', 'Letter']),
              help='The page size(A4, Mini, Letter)')
@click.option('--type_of_page', '-t', prompt='Enter page type',
              show_default=True, default='0', type=click.Choice(['0', '1', '2', '3']),
              help='The page type(DotGrid:0, Graph:1, Lined:2, Music:3)')  # Not implemented
@click.option('--numbered', '-n', prompt='Enter True for numbered pages',
              show_default=True, default=False, type=bool,
              help='Define if the pages will be numbered or not')
def gen_pdf(quantity, frame, type_of_page, numbered):
    """
    Generates a PDF document.

    Generates a PDF document depending on the quantity of pages, the template type and the page size.

    Parameters
    ----------
    quantity : int
        The number of pages that will contain the document.
    frame : str
        The size of the page, it can be A4 or Letter.
    type_of_page : str
        A string number that refers to the type of page, it can be (DotGrid:0, Graph:1, Lined:2, Music:3).
    numbered : bool
        Define if the pages will be numbered or not.

    Returns
    -------
    str
        Returns a message with the status

    """
    if frame == "Mini":
        t = 1
    else:
        t = 2
    # Looks for the qr code letter
    code = TYPES[type_of_page][1][frame]
    # Looks for the template type String
    type_of_page = TYPES[type_of_page][0]
    out_file = OUTPUT_FILENAME.format(frame, type_of_page, quantity)
    if not os.path.exists(GENERATED_PATH):
        pathlib.Path(GENERATED_PATH).mkdir(parents=True, exist_ok=True)
    elif os.path.exists(out_file):
        return f"The file {out_file} already exists"
    path = PATH.format(f'{frame}/{type_of_page}')
    frame_class = class_for_name("reportlab.lib.pagesizes", frame.upper())
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    output = PyPDF2.PdfFileWriter()
    for num in range(1, int(quantity) + 1):  # Adjust for the 1 start
        # Using ReportLab Canvas to insert image into PDF
        img_temp = BytesIO()
        img_doc = canvas.Canvas(img_temp, pagesize=frame_class)
        # Draw image on Canvas and save PDF in buffer
        img_doc.drawImage(qr_generate(num, path, code, t), int(POSITION[frame][0]), int(POSITION[frame][1]))
        if numbered:
            img_doc.drawRightString(int(POSITION[frame][0]) - 7, int(POSITION[frame][1]) + 3, str(num))
        img_doc.save()

        # Select page_to_merge
        page_to_merge = PyPDF2.PdfFileReader(open(TEMPLATE.format(frame, type_of_page), "rb")).getPage(0)
        # page_to_merge = PdfFileReader(open(TEMPLATE, "rb")).getPage(0)
        page_to_merge.mergePage(PyPDF2.PdfFileReader(BytesIO(img_temp.getvalue())).getPage(0))
        output.addPage(page_to_merge)
    # finally, write "output"
    output_stream = open(out_file, "wb")
    output.write(output_stream)
    output_stream.close()
    message = f"The file {out_file} was created"
    print(message)
    return message


@main.command(name="delete")
def clean_folders():
    """
    Delete all generated files.

    """
    delete_folder(GENERATED_PATH)
    delete_folder(PATH.format(""))
    print("All clear here")


@main.command(name="menu")
def menu():
    """
    Make use of an interactive menu.

    """
    interactive_menu = ConsoleMenu("Welcome to qr-rocket menu", "Select an option")
    interactive_menu.append_item(CommandItem("Create a new PDF file", "rocketqr create"))
    interactive_menu.append_item(CommandItem("Delete all auto generated files",  "rocketqr delete"))
    interactive_menu.show()

if __name__=="__main__":
    main()
