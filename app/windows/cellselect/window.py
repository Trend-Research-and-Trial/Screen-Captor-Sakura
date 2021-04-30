import tkinter
from PIL import Image, ImageTk
from app.windows.base import Base

class Window(Base):
    pass

    def confirm_button(self, command):
        confirm_button = tkinter.Button(self.root, text = '確定',background='#ff6b91', foreground = '#FFFFFF',command = command, font=("MSゴシック",15))
        confirm_button.grid(row= 2, column=0, padx=40, pady=40, sticky=tkinter.W)

    def display(self):
        # 部品生成
        cell_label = tkinter.Label(text='開始セルを指定する(例: A5)',background='#FFFFFF', foreground='#ff6b91', font=("MSゴシック",15))
        self.cell_entry = tkinter.Entry(self.root, width=5 ,background='#FFFFFF', foreground = 'black', font=("MSゴシック",25))

        # レイアウト設定
        cell_label.grid(row= 0, column=0, columnspan=2, padx=40, pady=40, sticky=tkinter.W)
        self.cell_entry.grid(row= 1, column=0, columnspan=3, padx=40, pady=0, sticky=tkinter.W)

        self.root.deiconify()
        self.cell_entry.focus_set()

        self.root.mainloop()
    
    def get_cell_entry(self):
        return self.cell_entry.get()