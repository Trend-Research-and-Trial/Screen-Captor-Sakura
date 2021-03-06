from app.excel import Excel
from PIL import Image

class Manual:
    def __init__(self, title, row=1, column=1, mode=0):
        self.excel = Excel(title, row, column, mode)

    def add(self, description, image):
        self.excel.paste(description)

        img = Image.open(image)
        width, height = img.size
        self.excel.pasteImg(image, width, height)
