import tkinter
import pyautogui  # キーボード操作を扱う外部ライブラリ
from PIL import Image, ImageTk, ImageGrab, ImageDraw  # 外部ライブラリ
import pynput
from pynput import keyboard
from pynput.keyboard import Key
from tkinter import messagebox
import uuid
import sys
import os
import shutil
from settings import ASSETS_PATH, TMP_IMAGE_PATH, TITLE
import win32gui
from time import sleep


class ManualCreation:

    def __init__(self, manual):
        # マニュアル作成
        self.manual = manual

        # 押下したボタンを監視する
        listener = keyboard.Listener(
            on_release=self.__check_pressed_key
        )
        listener.start()

        # 画面に表示する赤枠の座標
        self.scaled_rectangle_start_x = 0
        self.scaled_rectangle_start_y = 0
        self.scaled_rectangle_end_x = 0
        self.scaled_rectangle_end_y = 0
        self.SCALED_POINT = 0.75
        self.SCALED_POINT_FOREXCEL = 0.6
        self.rectangle_start_x = 0
        self.rectangle_start_y = 0
        self.rectangle_end_x = 0
        self.rectangle_end_y = 0
        self.rectangle_count = 0

        self.root = tkinter.Tk()
        self.root.title(TITLE)
        self.root.iconbitmap(ASSETS_PATH + '/trat.ico')
        self.root.geometry('+0+0')
        self.root.configure(background='#FFFFFF')

        comment_label = tkinter.Label(
            text='コメント入力', background='#FFFFFF', foreground='#ff6b91', font=("MSゴシック", 20))

        self.comment_text = tkinter.Entry(
            self.root, width=50, font=("MSゴシック", 20))
        self.comment_text.configure(background='#FFFFFF')

        next_button = tkinter.Button(
            self.root, text='次へ [F12]', width=15, background='#ff6b91', foreground='#FFFFFF', font=("MSゴシック", 15), command=self.__next)
        cancel_button = tkinter.Button(
            self.root, text='取り直し', width=15, background='#7F7F7F', foreground='#FFFFFF', font=("MSゴシック", 15), command=self.__cancel)
        
        rollback_img = tkinter.PhotoImage(file=ASSETS_PATH + '/rollback.png').subsample(6, 6)
        rollback_button = tkinter.Button(self.root,background='#FF89A8', command=self.__rollback, image=rollback_img,  width=55, height=55, compound="top")

        self.canvas = tkinter.Canvas(self.root, bg="black", width=self.root.winfo_screenwidth(
        )*self.SCALED_POINT, height=self.root.winfo_screenheight()*self.SCALED_POINT)
        self.initialized_img = Image.new('RGBA', (int(self.root.winfo_screenwidth(
        )*self.SCALED_POINT), int(self.root.winfo_screenheight()*self.SCALED_POINT)), 'black')
        self.initialized_img_tk = ImageTk.PhotoImage(self.initialized_img)
        # Canvasウィジェットに取得した画像を描画
        self.drawed_screenshot_area = self.canvas.create_image(
            0, 0, image=self.initialized_img_tk, anchor=tkinter.NW, tag="img")

        # イベントとコールバック関数を指定
        self.canvas.bind("<ButtonPress-1>", self.__start_drawing_rectangle)
        self.canvas.bind("<Button1-Motion>", self.__draw_rectangle)

        # 画像をassetsから取得する
        frame_button_img = Image.open(ASSETS_PATH + '/frameButton.png')
        frame_button_img = ImageTk.PhotoImage(frame_button_img)

        # 画像を表示するためのキャンバスの作成（黒で表示）
        frame_button_canvas = tkinter.Canvas(bg="white", width=80, height=55)

        # キャンバスに画像を表示する。第一引数と第二引数は、x, yの座標
        frame_button_canvas.create_image(
            0, 0, image=frame_button_img, anchor=tkinter.NW)

        comment_label.grid(row=0, sticky=tkinter.W, column=0, padx=20, pady=5)
        self.comment_text.grid(row=1, sticky=tkinter.W + tkinter.E,
                               column=0, padx=20, pady=5)
        next_button.grid(row=1, column=1, sticky=tkinter.E, padx=20, pady=5)
        cancel_button.grid(row=1, column=2, sticky=tkinter.E, padx=20, pady=5)
        rollback_button.grid(row=2, column=2, sticky=tkinter.E, padx=20, pady=5)
        frame_button_canvas.grid(
            row=2, column=0, columnspan=2, padx=20, pady=5, sticky=tkinter.W)
        self.canvas.grid(row=5, column=0, columnspan=3, padx=20, pady=5)
        
        self.root.grid_anchor(tkinter.CENTER)
        self.root.withdraw()
        self.root.mainloop()

    # キーボード押したときの関数
    def __check_pressed_key(self, key):
        # 入力されたキーに応じて処理
        # スクリーンショットキーで最前面に移動
        if key == Key.print_screen:
            sleep(0.5)
            self.__print_screen()
        # Escで閉じる
        if key == Key.esc:
            messagebox.showinfo('確認', '処理を終了します')
            # 作成した画像を削除
            if os.path.isdir(TMP_IMAGE_PATH):
                shutil.rmtree(TMP_IMAGE_PATH)
            self.root.quit()
        if key == Key.f12 and self.root.winfo_viewable() == 1:
            self.__next()

    def __print_screen(self):

        # クリップボードのスクリーンショットを取得
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            # 表示する画像の取得（スクリーンショット）
            self.img = im
            # スクリーンショットした画像は表示しきれないので画像リサイズ
            self.resized_img = self.img.resize(size=(int(self.img.width * self.SCALED_POINT),
                                                    int(self.img.height * self.SCALED_POINT)), resample=Image.BILINEAR)
            # tkinterで表示できるように画像変換
            self.img_tk = ImageTk.PhotoImage(self.resized_img)

            self.canvas.config(width=self.img_tk.width(), height=self.img_tk.height())
            
            # Canvasウィジェットに取得した画像を描画
            self.canvas.itemconfig(self.drawed_screenshot_area, image=self.img_tk)

            # 画面を最大化する
            self.root.deiconify()
            self.comment_text.focus_set()

        else:
            print('failed grab print screen image')

    def __next(self):
        # "red_rectangle"タグの画像の座標を元の縮尺に戻して取得

        for rectangle_count in range(self.rectangle_count):
            if self.canvas.coords(f'red_rectangle{rectangle_count+1}') != []:
                self.rectangle_start_x, self.rectangle_start_y, self.rectangle_end_x, self.rectangle_end_y = [
                    round(n / self.SCALED_POINT) for n in self.canvas.coords(f'red_rectangle{rectangle_count+1}')
                ]
                self.draw = ImageDraw.Draw(self.img)
                self.draw.rectangle((self.rectangle_start_x, self.rectangle_start_y, self.rectangle_end_x, self.rectangle_end_y),
                                    outline=(255, 0, 0), width=9)
            self.resized_img = self.img.resize(size=(int(self.img.width *self.SCALED_POINT_FOREXCEL),
                                                int(self.img.height *self.SCALED_POINT_FOREXCEL)), resample=Image.BILINEAR)

        if not os.path.isdir(TMP_IMAGE_PATH):
            os.makedirs(TMP_IMAGE_PATH)
        file_name = f'{TMP_IMAGE_PATH}/{uuid.uuid4()}.png'
        self.resized_img.save(file_name, quality=95)
        self.manual.add(self.comment_text.get(), file_name)

        self.__clear()

    def __cancel(self):
        self.__clear()

    def __rollback(self):
        if self.rectangle_count >= 1:
            self.canvas.delete(f'red_rectangle{self.rectangle_count}')
            self.rectangle_count -= 1

    def __start_drawing_rectangle(self, event):
        # すでに"red_rectangle"タグの図形があれば削除
        # self.canvas.delete("red_rectangle")
        # canvas上に四角形を描画（rectangleは矩形の意味）
        self.rectangle_count += 1
        self.canvas.create_rectangle(event.x,
                                      event.y,
                                      event.x,
                                      event.y,
                                      outline="red",
                                      tag=f'red_rectangle{self.rectangle_count}')
        # グローバル変数に座標を格納
        self.scaled_rectangle_start_x, self.scaled_rectangle_start_y = event.x, event.y

    def __draw_rectangle(self, event):
        # ドラッグ中のマウスポインタが領域外に出た時の処理
        if event.x < 0:
            self.scaled_rectangle_end_x = 0
        else:
            self.scaled_rectangle_end_x = min(self.resized_img.width, event.x)
        if event.y < 0:
            self.scaled_rectangle_end_y = 0
        else:
            self.scaled_rectangle_end_y = min(self.resized_img.height, event.y)
        # "red_rectangle"タグの画像を再描画
        self.canvas.coords(f'red_rectangle{self.rectangle_count}', self.scaled_rectangle_start_x,
                            self.scaled_rectangle_start_y, self.scaled_rectangle_end_x, self.scaled_rectangle_end_y)

    def __clear(self):
        for rectangle_count in range(self.rectangle_count):
            self.canvas.delete(f'red_rectangle{rectangle_count+1}')
        self.rectangle_count = 0
        self.canvas.itemconfig(self.drawed_screenshot_area, image = self.initialized_img_tk)
        self.root.withdraw()
        self.comment_text.delete(0, tkinter.END)
