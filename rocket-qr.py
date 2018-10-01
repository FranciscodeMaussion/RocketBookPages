import qrcode, os, sys, importlib, pathlib
from io import BytesIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, LETTER

MESSAGE = 'P{:02d} V0{} S0000000'
TEMPLATE = 'Source/Rocketbook-{}-{}.pdf'
GENERATED_PATH = 'Generated'
OUTPUT_FILENAME = GENERATED_PATH+'/Rocketbook-{}-{}-pages{}.pdf'
PATH = 'QR/{}'
POSITION = {
    'A4':[508, 62],
    'Letter':[527, 47]
}
TYPES = {
    '0': [
        "DotGrid",
        {
            'A4':'5',
            'Letter':'4'
        }
    ],
    '1': [
        "Graph",
        {
            'A4':'P',
            'Letter':'O'
        }
    ],
    '2': [
        "Lined",
        {
            'A4':'N',
            'Letter':'M'
        }
    ],
    '3': [
        "Music",
        {
            'A4':'R',
            'Letter':'Q'
        }
    ],
}

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
    c = getattr(m, class_name)
    return c

def gen_pdf(quantity=1, frame='A4', type='0'):
    """
    Generates a PDF document.

    Generates a PDF document depending on the quantity of pages, the template type and the page size.

    Parameters
    ----------
    quantity : int
        The number of pages that will contain the document.
    frame : str
        The size of the page, it can be A4 or Letter.
    type : str
        A string number that refers to the type of page, it can be (DotGrid:0, Graph:1, Lined:2, Music:3).

    Returns
    -------
    str
        Returns a message with the status

    """
    # Looks for the qr code letter
    frame = frame.lower().capitalize()
    code = TYPES[type][1][frame]
    # Looks for the template type String
    type = TYPES[type][0]
    out_file = OUTPUT_FILENAME.format(frame, type, quantity)
    if os.path.exists(out_file):
        return "The file %s already exists" % out_file
    path = PATH.format('/%s/%s' % (frame, type))
    frame_class = class_for_name("reportlab.lib.pagesizes", frame.upper())
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    output = PdfFileWriter()
    for num in range(1, int(quantity)+1): # Adjust for the 1 start
        # Using ReportLab Canvas to insert image into PDF
        imgTemp = BytesIO()
        imgDoc = canvas.Canvas(imgTemp, pagesize=frame_class)
        # Draw image on Canvas and save PDF in buffer
        imgDoc.drawImage(qr_generate(num, path, code), int(POSITION[frame][0]), int(POSITION[frame][1]))
        imgDoc.save()
        # Select PageToMerge
        pageToMerge = PdfFileReader(open(TEMPLATE.format(frame, type), "rb")).getPage(0)
        #pageToMerge = PdfFileReader(open(TEMPLATE, "rb")).getPage(0)
        pageToMerge.mergePage(PdfFileReader(BytesIO(imgTemp.getvalue())).getPage(0))
        output.addPage(pageToMerge)
    # finally, write "output"
    outputStream = open(out_file, "wb")
    output.write(outputStream)
    outputStream.close()
    return "The file %s was created" % out_file

def qr_generate(page_number, path, code):
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

    Returns
    -------
    str
        Returns the path of the jpg file

    """
    file = '%s/%s.jpg' % (path, str(page_number))
    if not os.path.exists(file):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=2,
            border=1,
        )
        qr.add_data(MESSAGE.format(page_number, code))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(file)
    return file

def clean_folders():
    delete_folder(GENERATED_PATH)
    delete_folder(PATH.format(""))

def delete_folder(pth):
    pth = pathlib.Path(pth)
    for sub in pth.iterdir():
        if sub.is_dir():
            delete_folder(sub)
        else:
            sub.unlink()

def help_doc(command):
    if command == "create":
        print("python rocket-qr.py <number of pages> <A4 or letter> <0:DotGrid, 1:Graph, 2:Lined or 3:Music>")
        print("Generate de PDF doc.")
        print("Default(one page A4 DotGrid): ")
        print("python rocket-qr.py 1 A4 0")
        print("Is the same as")
        print("python rocket-qr.py")
    elif command == "clean":
        print("python rocket-qr.py -c")
        print("python rocket-qr.py --clean")
        print("Clear all the generated files.")
    else:
        print("More help with the command, type:")
        print("python rocket-qr.py -h clean")
        print("python rocket-qr.py -h create")

if __name__ == '__main__':
    args = tuple(sys.argv[1:])
    if args[0] in ['--help', '-h']:
        try:
            help_doc(args[1])
        except IndexError:
            help_doc("")
    elif args[0] in ['--clean', '-c']:
        clean_folders()
    else:
        if not os.path.exists(GENERATED_PATH):
            os.mkdir(GENERATED_PATH)
        print(gen_pdf(*args))
