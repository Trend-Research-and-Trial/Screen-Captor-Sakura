import tkinter
from app.screencaptor import ScreenCaptor
from PIL import Image, ImageTk
from settings import ASSETS_PATH, TITLE
from app.services.manual import Manual

class CellSelect:
    def __init__(self, path):
        self.path = path

        self.root = tkinter.Tk()

        self.root.title(TITLE)
        self.root.configure(background='#FFFFFF')
        self.root.iconbitmap(ASSETS_PATH + '/trat.ico')

        # 部品生成
        cell_label = tkinter.Label(text='開始セルを指定する(例: A5)',background='#FFFFFF', foreground='#ff6b91', font=("MSゴシック",15))
        self.cell_entry = tkinter.Entry(self.root, width=5 ,background='#FFFFFF', foreground = 'black', font=("MSゴシック",25))
        create_button = tkinter.Button(self.root, text = '確定',background='#ff6b91', foreground = '#FFFFFF',command =self.__confirm, font=("MSゴシック",15))

        # レイアウト設定
        cell_label.grid(row= 0, column=0, columnspan=2, padx=40, pady=40, sticky=tkinter.W)
        self.cell_entry.grid(row= 1, column=0, columnspan=3, padx=40, pady=0, sticky=tkinter.W)
        create_button.grid(row= 2, column=0, padx=40, pady=40, sticky=tkinter.W)

        self.root.deiconify()
        self.cell_entry.focus_set()

        self.root.mainloop()

    def __confirm(self):
        cell = self.cell_entry.get()
        self.root.destroy()
        ScreenCaptor(Manual(self.path, mode=1, cell=cell))
        self.root.quit()