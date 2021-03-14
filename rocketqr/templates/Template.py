class Template(object):
    def __init__(self, name, page_size, codes, qr_position, qr_size):
        self.name = name  # How would be called: A4
        self.page_size = page_size  # The defined by reportlab.lib.pagesizes
        self.codes = codes  # Unique code for this page [DotGrid:1, Lined:V]
        self.qr_position = qr_position  # Where the QR code should go
        self.qr_size = qr_size  # IDK for mini = 1 rest = 2

    def add_code(self, code):
        self.codes.append(code)

    def __str__(self):
        text = (
            f"Template:\n\t"
            f"name = {self.name}\n\t"
            f"page_size = {self.page_size}\n\t"
            f"code = {self.codes}\n\t"
            f"qr_position = {self.qr_position}\n\t"
            f"qr_size = {self.qr_size}"
        )
        return text
