import tkinter
from tkinter import messagebox
from app.manualcreation import ManualCreation
from PIL import Image, ImageTk
import webbrowser
from settings import ASSETS_PATH, TITLE

class Top:
    def __init__(self):
        self.root = tkinter.Tk()

        self.root.title(TITLE)
        self.root.configure(background='#FFFFFF')
        self.root.iconbitmap(ASSETS_PATH + '/trat.ico')

        #新規作成用部品生成
        title_label = tkinter.Label(text='ファイル名を入力',background='#FFFFFF', foreground='#ff6b91', font=("MSゴシック",15))
        
        # 画像を表示するためのキャンバスの作成（黒で表示）
        python_canvas = tkinter.Canvas(bg = "#FFFFFF", width=120, height=30, highlightthickness=0)
        # キャンバスに画像を表示する。第一引数と第二引数は、x, yの座標
        python_img = ImageTk.PhotoImage(Image.open(ASSETS_PATH + '/python.png'))
        python_canvas.create_image(0, 0, image=python_img, anchor=tkinter.NW)

        self.title_text = tkinter.Entry(self.root, width=40,background='#FFFFFF', foreground = 'black', font=("MSゴシック",25))
        self.title_text.focus_set()

        create_button = tkinter.Button(self.root, text = '新規作成',background='#ff6b91', foreground = '#FFFFFF',command =self.create, font=("MSゴシック",15))
        extention_label = tkinter.Label(text='.xlsx',background='#FFFFFF', foreground='#ff6b91', font=("MSゴシック",15))

        # 画像を表示するためのキャンバスの作成（黒で表示）
        canvas = tkinter.Canvas(bg = "#FFFFFF", width=40, height=40, highlightthickness=0)
        github_img = ImageTk.PhotoImage(Image.open(ASSETS_PATH + '/github.png'))
        canvas.create_image(0, 0, image=github_img, anchor=tkinter.NW)

        git_repositry_label = tkinter.Label(text='Git Repository:',background='#FFFFFF', foreground='#7F7F7F', font=("MSゴシック",12))
        git_repositry_link_label = tkinter.Label(text='https://github.com/Trend-Research-and-Trial/Screen-Captor-Sakura',background='#FFFFFF', foreground='#3C78A9', font=("MSゴシック",10))
        git_repositry_link_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Trend-Research-and-Trial/Screen-Captor-Sakura"))

        copyright_label = tkinter.Label(text='Copyright © 2021 Trend Research and Trial',background='#FFFFFF', foreground='#7F7F7F', font=("MSゴシック",10))

        title_label.grid(row= 0, column=0, columnspan=2, padx=40, pady=40, sticky=tkinter.W)
        python_canvas.grid(row= 0, column=2, padx=40, pady=40, sticky=tkinter.E)
        self.title_text.grid(row= 1, column=0, columnspan=3, padx=40, pady=0, sticky=tkinter.W)
        create_button.grid(row= 2, column=0, padx=40, pady=40, sticky=tkinter.W)
        extention_label.grid(row= 2, column=2, padx=40, pady=0, sticky=tkinter.E + tkinter.N)
        canvas.grid(row=3, rowspan=2, column=0, padx=40, sticky=tkinter.E) 
        git_repositry_label.grid(row= 3, column=1, columnspan=2, padx=0, pady=5, sticky=tkinter.W)
        git_repositry_link_label.grid(row= 4, column=1, columnspan=2, padx=40, pady=5, sticky=tkinter.W)
        copyright_label.grid(row= 5, column=1, padx=60, pady=40)

        self.root.mainloop()

    def create(self):
        messagebox.showinfo('確認', '処理を開始します\n画面キャプチャをとる場合はPrtScreenキーを押してください\nツールを終了する場合はEscキーを押してください')
        manual_title = self.title_text.get()
        self.root.destroy()
        ManualCreation(manual_title)
        self.root.quit()