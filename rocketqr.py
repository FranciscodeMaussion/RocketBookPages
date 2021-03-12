from io import BytesIO
import click
import os
import PyPDF2
from reportlab.pdfgen import canvas
from consolemenu import *
from consolemenu.items import *
from templates.template_utils import read_from_file

from templates.templates_commands import templates

from constants.constants import OUTPUT_FILENAME, PATH, TEMPLATE, GENERATED_PATH
from utils import class_for_name, delete_folder, qr_generate


def set_up():
    main.add_command(templates)
    main()


@click.group()
def main():
    pass


@main.command(name="create")
@click.option('--quantity', '-q', prompt='Enter number of pages',
              show_default=True, default=1, type=int,
              help='The number of pages that will contain the document')
@click.option('--numbered', '-n', prompt='Enter True for numbered pages',
              show_default=True, default=False, type=bool,
              help='Define if the pages will be numbered or not')
def gen_pdf(quantity, numbered):
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
        A string number that refers to the type of page, it can be (Blank:0, DotGrid:1, Graph:2, Lined:3, Music:4).
    numbered : bool
        Define if the pages will be numbered or not.

    Returns
    -------
    str
        Returns a message with the status

    """
    frames = read_from_file()
    frame = click.prompt(f"Enter frame size{[str(x.name) for x in frames]}",
                         show_default=True, default='0',
                         type=click.Choice([str(x) for x in range(len(frames))])
                         )
    use_template = frames[int(frame)]

    codes_keys = list(use_template.codes.keys())
    type_of_page = click.prompt(f'Enter page type{codes_keys}',
                                show_default=True, default='0',
                                type=click.Choice([str(x) for x in range(len(codes_keys))]),
                                )
    # Looks for the template type String
    type_of_page = codes_keys[int(type_of_page)]
    # Looks for the qr code letter
    code = use_template.codes[type_of_page]
    out_file = OUTPUT_FILENAME.format(use_template.name, type_of_page, quantity)
    os.makedirs(GENERATED_PATH, exist_ok=True)
    if os.path.exists(out_file):
        message = f"The file {out_file} already exists"
        click.echo(message)
        return message
    path = PATH.format(f'{use_template.name}/{type_of_page}')
    frame_class = class_for_name("reportlab.lib.pagesizes", use_template.page_size)
    os.makedirs(path, exist_ok=True)
    output = PyPDF2.PdfFileWriter()
    for num in range(1, int(quantity) + 1):  # Adjust for the 1 start
        # Using ReportLab Canvas to insert image into PDF
        img_temp = BytesIO()
        img_doc = canvas.Canvas(img_temp, pagesize=frame_class)
        # Draw image on Canvas and save PDF in buffer
        img_doc.drawImage(qr_generate(num, path, code, use_template.qr_size),
                          use_template.qr_position[0], use_template.qr_position[1])
        if numbered:
            img_doc.drawRightString(use_template.qr_position[0] - 7, use_template.qr_position[1] + 3, str(num))
        img_doc.save()

        # Select page_to_merge
        page_to_merge = PyPDF2.PdfFileReader(open(TEMPLATE.format(use_template.name, type_of_page), "rb")).getPage(0)
        # page_to_merge = PdfFileReader(open(TEMPLATE, "rb")).getPage(0)
        page_to_merge.mergePage(PyPDF2.PdfFileReader(BytesIO(img_temp.getvalue())).getPage(0))
        output.addPage(page_to_merge)
    # finally, write "output"
    output_stream = open(out_file, "wb")
    output.write(output_stream)
    output_stream.close()
    message = f"The file {out_file} was created"
    click.echo(message)
    return message


@main.command(name="delete")
def clean_folders():
    """
    Delete all generated files.

    """
    delete_folder(GENERATED_PATH)
    delete_folder(PATH.format(""))
    click.echo("All clear here")


@main.command(name="menu")
def menu():
    """
    Make use of an interactive menu.

    """
    interactive_menu = ConsoleMenu("Welcome to qr-rocket menu", "Select an option")
    interactive_menu.append_item(CommandItem("Create a new PDF file", "rocketqr create"))
    interactive_menu.append_item(CommandItem("Delete all auto generated files", "rocketqr delete"))
    interactive_menu.append_item(CommandItem("Go to templates menu", "rocketqr templates menu"))
    interactive_menu.show()


if __name__ == "__main__":
    set_up()
