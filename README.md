# RocketBookPages
Generates RocketBook QR Numerated Pages in a PDF depending on the quantity of pages, the template type and the page size.

## Installation
It has been tested in python3 only.
```bash
git clone https://github.com/FranciscodeMaussion/RocketBookPages
cd RocketBookPages
# may activate your venv or install with --user option
pip install -r requirements.txt
pip install --editable .
```

## Usage
You must be placed in the program folder.

- Create a new PDF file 
    ```bash
    rocketqr create
    ```
    - Parameters:
        - --quantity, -q: The number of pages that will contain the document
        - --frame, -f: The page size(A4, Mini, Letter)
        - --type_of_page, -t: The page type(DotGrid:0, Graph:1, Lined:2, Music:3)
        - --numbered, -n: Define if the pages will be numbered or not
    - Note: if a parameter is no provided, it will be asked for.
- Delete all generated files
    ```bash
    rocketqr delete
    ```
- Templates section
    ```bash
    rocketqr templates menu
    rocketqr templates show
    rocketqr templates create
    ```
- Open menu
    ```bash
    rocketqr menu
    ```

## Example
Will generate an A4 sized file with 5 pages and with DotGrid template with numbered pages.
```bash
rocketqr create -q 5 -f A4 -t 0 -n True
```

## Make use of
- [Click](https://click.palletsprojects.com)
- [console-menu](https://github.com/aegirhall/console-menu)
- [Pillow](https://pillow.readthedocs.io/en/stable/)
- [PyPDF2](https://pythonhosted.org/PyPDF2/)
- [qrcode](https://github.com/lincolnloop/python-qrcode)
- [reportlab](https://www.reportlab.com/)
- [six](https://github.com/benjaminp/six)

