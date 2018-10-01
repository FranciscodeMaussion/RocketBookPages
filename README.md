# RocketBookPages
Generates RocketBook QR Numerated Pages in a PDF depending on the quantity of pages, the template type and the page size.

## Parameters
- `quantity` : int,
    The number of pages that will contain the document.
- `frame` : str,
    The size of the page, it can be A4 or Letter.
- `type` : str,
    A string number that refers to the type of page, it can be (DotGrid:0, Graph:1, Lined:2, Music:3).

## Returns
- `str`,
    Returns a message with the status
- `file`,
    The *.pdf file

## Usage
You must be placed in the program folder.
```bash
python rocket-qr.py <quantity> <frame> <type>
```

## Example
Will generate an A4 sized file with 5 pages and with DotGrid template
```bash
python rocket-qr.py 5 A4 0
```
