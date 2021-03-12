import importlib
import os

import qrcode

from constants.constants import MESSAGE


def class_for_name(module_name, class_name):
    """
    Returns non string class.

    Parameters
    ----------
    module_name : str
        Module to find the class.
    class_name : str
        The string name of the class.

    Returns
    -------
    class
        Returns the class from string

    """
    # Load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # Get the class, will raise AttributeError if class cannot be found
    try:
        c = getattr(m, class_name)
    except AttributeError as e:
        c = (527, 47)
    return c


def qr_generate(page_number, path, code, t=2):
    """
    Generates a qr code image.

    Generates a qr code depending on the page number, and the template type.

    Parameters
    ----------
    page_number : int
        The number of the page that will contain the qr code.
    path : str
        Where the jpg file will be stored.
    code : str
        From Rocketbook code of template.
    t : int
        Specify qr size

    Returns
    -------
    str
        Returns the path of the jpg file

    """
    file = f'{path}/{page_number}.jpg'
    if not os.path.exists(file):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=t,
            border=1,
        )
        qr.add_data(MESSAGE.format(page_number, code))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file)
    return file


def delete_folder(target_deletable):
    print("Deleting all in: ", target_deletable)
    for dir_deletable in os.listdir(target_deletable):
        try:
            delete_folder(target_deletable + '/' + dir_deletable)
        except OSError:
            os.remove(target_deletable + '/' + dir_deletable)
    os.rmdir(target_deletable)

