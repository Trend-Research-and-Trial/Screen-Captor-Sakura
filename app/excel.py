import openpyxl
from openpyxl.styles import Font
import math
import os
from settings import OUTPUT

class Excel:
    """
    Args:
        path str:
        row int:
        column int:
        mode int: 0 => 新規作成モード, 1 => 追記モード
    """
    def __init__(self, path, row=1, column=1, mode=0):

        # pathからのタイトル取得とpath編集を行う
        title = path.split("/")[-1]
        if len(title.split(".")) > 1:
            title = title.split(".")[0]
        else:
            path = path + '.xlsx'
        self.path = path

        self.next_row = row
        self.next_column = column

        if mode==0:
            # 0の場合：新規作成モード
            # Excelファイルの新規作成
            self.book = openpyxl.Workbook()

            sheet, current_cell = self.__getSheetAndCell()

            sheet.title = "手順書" 
            # 指定したセルに文字列を入力する
            current_cell.value = title
            
            self.next_row = row + 2
            self.next_column = column

        elif mode == 1:
            # 1の場合：追記モード
            self.book = openpyxl.load_workbook(self.path)

        if not os.path.isdir(OUTPUT):
            os.makedirs(OUTPUT)
        self.book.save(OUTPUT + '/' + self.path)

    def paste(self, value):
        # シートの取得とシート名の変更
        _, current_cell = self.__getSheetAndCell()

        # 指定したセルに文字列を入力する
        current_cell.value = value
        
        self.__save(row_to_add=2)
        
    def pasteImg(self, value, width, hight):
        # シートの取得とシート名の変更
        sheet, current_cell = self.__getSheetAndCell()
        
        img = openpyxl.drawing.image.Image(value)
        str_current_cell= current_cell.coordinate  # カレントのセルを'A1'のような形式に変換(次行の処理のため)
        img.anchor = str_current_cell
        sheet.add_image(img)

        self.__save(row_to_add=math.ceil(hight*1.25 / 22 + 1))
    
    def __save(self, row_to_add=0, column_to_add=0):
        self.next_row += row_to_add
        self.next_column += column_to_add

        self.book.save('./output/' + self.path)

    def __getSheetAndCell(self):
        sheet = self.book.active
        current_cell = sheet.cell(self.next_row, self.next_column)
        return sheet, current_cell