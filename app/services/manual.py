from app.services.excel import Excel
from PIL import Image
from settings import OUTPUT
import os

class Manual:
    def __init__(self, path, row=1, column=1, cell=None, mode=0):
        # pathからのタイトル取得とpath編集を行う

        # タイトルのみ指定されているときはOUTPUTディレクトリを指定する
        if len(path.split("/")) < 2:
            if not os.path.isdir(OUTPUT):
                os.makedirs(OUTPUT)
            path = OUTPUT + "/" + path
        
        # 拡張子が指定されていない場合は追加する
        if len(path.split("/")[-1].split(".")) == 1:
            path = path + '.xlsx'
            
        self.excel = Excel(path, row, column, cell, mode)

    def add(self, description, image):
        self.excel.paste(description)

        img = Image.open(image)
        width, height = img.size
        self.excel.pasteImg(image, width, height)
