from tkinter import messagebox
from app.windows.screencaptor import ScreenCaptor
from app.windows.cellselect import CellSelect
import os, tkinter.filedialog
from app.services.manual import Manual
from app.windows.top.window import Window

class Top:
    def __init__(self):
        self.window = Window()
        self.window.create_button(self.__create)
        self.window.edit_button(self.__edit)
        self.window.display()

    def __create(self):
        messagebox.showinfo('確認', '処理を開始します\n画面キャプチャをとる場合はPrtScreenキーを押してください\nツールを終了する場合はEscキーを押してください')
        manual_title = self.window.get_title_text()

        self.window.destroy()
        ScreenCaptor(Manual(manual_title))
        self.window.quit()
    
    def __edit(self):
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

        self.window.destroy()
        CellSelect(file)
        self.window.quit()