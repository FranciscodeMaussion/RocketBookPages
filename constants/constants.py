MESSAGE = 'P{:02d} V0{} S0000000'
TEMPLATE = 'Source/Bases/Rocketbook-{}-Base.pdf'
TEMPLATES_JSON = 'Source/templates.json'
GENERATED_PATH = 'Generated'
OUTPUT_FILENAME = GENERATED_PATH + '/Rocketbook-{}-{}-pages{}.pdf'
PATH = 'QR/{}'
POSITION = {
    'A4': [508, 62],
    'Letter': [527, 47],
    'Mini': [215, 12]
}
PAGES_TYPES = ['Blank', 'DotGrid', 'Graph', 'Lined', 'Music']
# TODO Read types from database
TYPES = {
    '0': [
        "DotGrid",
        {
            'A4': '5',
            'Letter': '4',
            'Mini': '3'
        }
    ],
    '1': [
        "Graph",
        {
            'A4': 'P',
            'Letter': 'O',
            'Mini': 'S'
        }
    ],
    '2': [
        "Lined",
        {
            'A4': 'N',
            'Letter': 'M',
            'Mini': 'V'
        }
    ],
    '3': [
        "Music",
        {
            'A4': 'R',
            'Letter': 'Q',
            'Mini': 'X'
        }
    ],
}