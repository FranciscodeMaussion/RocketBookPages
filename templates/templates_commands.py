import click
from templates.template_utils import read_from_file, save_to_file, name_validation

from templates.Template import Template

from constants.constants import PAGES_TYPES


@click.group()
def templates():
    """
    All templates part, you may want to use create or show

    """
    pass


@templates.command(name="create")
@click.option('--name', '-n', prompt='Enter template name',
              type=str,
              help='How would be called')
@click.option('--page-size', '-s', prompt='Enter frame size',
              type=str,
              help='The defined by reportlab.lib.pagesizes')
@click.option('--qr-x', '-x', prompt='Enter qr_x',
              type=float,
              help='Where the QR code should go x')
@click.option('--qr-y', '-y', prompt='Enter qr_y',
              type=float,
              help='Where the QR code should go y')
@click.option('--qr-size', '-q', prompt='Enter qr_size',
              type=int,
              help='IDK for mini = 1 rest = 2')
def create(name, page_size, qr_x, qr_y, qr_size):
    """
        Create a new template.

        Parameters
        ----------
        name : str
            The template name
        page_size : str
            The size of the page, it any defined by reportlab.lib.pagesizes.
        qr_x : float
            Where the QR code should go x.
        qr_y : float
            Where the QR code should go y.
        qr_size : int
            IDK for mini = 1 rest = 2

        """
    codes = {}
    while True:
        page_type = click.prompt(f"Enter page type to assign{PAGES_TYPES}",
                                 type=click.Choice([str(x) for x in range(len(PAGES_TYPES))]))
        page_type = PAGES_TYPES[int(page_type)]
        type_code = click.prompt(f"Enter a code to assign to {page_type}", type=str)
        codes[page_type] = type_code
        if not click.confirm('Do you want to continue?'):
            break
    templates_array = read_from_file()
    new_template = name_validation(templates_array, Template(name, page_size, codes, [qr_x, qr_y], qr_size))
    templates_array.append(new_template)
    save_to_file(templates_array)
    click.echo(f"Template added\n{new_template}")


@templates.command(name="show")
def show():
    """
    Shows all templates in default file.

    """
    templates_array = read_from_file()
    for i in templates_array:
        print(i)
