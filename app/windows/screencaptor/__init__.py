import pyautogui  # キーボード操作を扱う外部ライブラリ
from PIL import Image, ImageTk, ImageGrab, ImageDraw  # 外部ライブラリ
import pynput
from pynput import keyboard
from pynput.keyboard import Key
from tkinter import messagebox
import uuid
import os
import shutil
from settings import TMP_IMAGE_PATH, LINE_WIDTH
from time import sleep
from app.windows.screencaptor.window import Window
from app.windows.screencaptor.setting import SCALED_POINT, SCALED_POINT_FOREXCEL

class ScreenCaptor:
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
        self.rectangle_start_x = 0
        self.rectangle_start_y = 0
        self.rectangle_end_x = 0
        self.rectangle_end_y = 0
        self.rectangle_count = 0

        self.window = Window()
        self.window.canvas(self.__start_drawing_rectangle, self.__draw_rectangle)
        self.window.next_button(self.__next)
        self.window.rollback_button(self.__rollback)
        self.window.cancel_button(self.__cancel)
        self.window.display()

    # キーボード押したときの関数
    def __check_pressed_key(self, key):
        # 入力されたキーに応じて処理
        # スクリーンショットキーで最前面に移動
        if key == Key.print_screen:
            MAX_RETRY = 10
            for i in range(MAX_RETRY + 1):
                try:
                    sleep(0.5)
                    self.__print_screen()
                    return
                except OSError as e:
                    if MAX_RETRY == i:
                            raise e

        # Escで閉じる
        if key == Key.esc:
            messagebox.showinfo('確認', '処理を終了します')
            # 作成した画像を削除
            if os.path.isdir(TMP_IMAGE_PATH):
                shutil.rmtree(TMP_IMAGE_PATH)
            self.window.quit()
        if key == Key.f12 and self.window.winfo_viewable() == 1:
            self.__next()

    def __print_screen(self):
        self.__clear()
        # クリップボードのスクリーンショットを取得
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            # 表示する画像の取得（スクリーンショット）
            self.img = im
            # スクリーンショットした画像は表示しきれないので画像リサイズ
            self.resized_img = self.img.resize(size=(int(self.img.width * SCALED_POINT),
                                                    int(self.img.height * SCALED_POINT)), resample=Image.BILINEAR)
            # tkinterで表示できるように画像変換
            self.img_tk = ImageTk.PhotoImage(self.resized_img)

            canvas = self.window.get_canvas()
            canvas.config(width=self.img_tk.width(), height=self.img_tk.height())
            # Canvasウィジェットに取得した画像を描画
            canvas.itemconfig(self.window.get_drawed_screenshot_area(), image=self.img_tk)

            # 画面を最大化する
            self.window.deiconify()
            self.window.deiconify()
            self.window.focus_set_comment_text()

        else:
            print('failed grab print screen image')

    def __next(self):
        # "red_rectangle"タグの画像の座標を元の縮尺に戻して取得
        for rectangle_count in range(self.rectangle_count):
            canvas = self.window.get_canvas()
            if canvas.coords(f'red_rectangle{rectangle_count+1}') != []:
                self.rectangle_start_x, self.rectangle_start_y, self.rectangle_end_x, self.rectangle_end_y = [
                    round(n / SCALED_POINT) for n in canvas.coords(f'red_rectangle{rectangle_count+1}')
                ]
                self.draw = ImageDraw.Draw(self.img)
                self.draw.rectangle((self.rectangle_start_x, self.rectangle_start_y, self.rectangle_end_x, self.rectangle_end_y),
                                    outline=(255, 0, 0), width=LINE_WIDTH*2)
            self.resized_img = self.img.resize(size=(int(self.img.width *SCALED_POINT_FOREXCEL),
                                                int(self.img.height *SCALED_POINT_FOREXCEL)), resample=Image.BILINEAR)

        if not os.path.isdir(TMP_IMAGE_PATH):
            os.makedirs(TMP_IMAGE_PATH)
        file_name = f'{TMP_IMAGE_PATH}/{uuid.uuid4()}.png'
        self.resized_img.save(file_name, quality=95)
        self.manual.add(self.window.comment_text.get(), file_name)

        self.__clear()

    def __cancel(self):
        self.__clear()

    def __rollback(self):
        canvas = self.window.get_canvas()
        if self.rectangle_count >= 1:
            canvas.delete(f'red_rectangle{self.rectangle_count}')
            self.rectangle_count -= 1

    def __start_drawing_rectangle(self, event):
        # すでに"red_rectangle"タグの図形があれば削除
        # self.canvas.delete("red_rectangle")
        # canvas上に四角形を描画（rectangleは矩形の意味）
        self.rectangle_count += 1
        canvas = self.window.get_canvas()
        canvas.create_rectangle(event.x,
                                      event.y,
                                      event.x,
                                      event.y,
                                      outline="red",
                                      tag=f'red_rectangle{self.rectangle_count}',
                                      width=LINE_WIDTH
                                      )
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
        canvas = self.window.get_canvas()
        canvas.coords(f'red_rectangle{self.rectangle_count}', self.scaled_rectangle_start_x,
                            self.scaled_rectangle_start_y, self.scaled_rectangle_end_x, self.scaled_rectangle_end_y)

    def __clear(self):
        canvas = self.window.get_canvas()
        for rectangle_count in range(self.rectangle_count):
            canvas.delete(f'red_rectangle{rectangle_count+1}')
        self.rectangle_count = 0

        drawed_screenshot_area = self.window.get_drawed_screenshot_area()

        canvas.itemconfig(drawed_screenshot_area, image = self.window.get_initialized_img_tk())
        self.window.withdraw()
        self.window.delete_comment_text()
