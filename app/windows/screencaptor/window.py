import tkinter
from PIL import Image, ImageTk  # 外部ライブラリ
from settings import ASSETS_PATH
from app.windows.screencaptor.setting import SCALED_POINT, SCALED_POINT_FOREXCEL
from app.windows.base import Base

class Window(Base):
    pass

    def __init__(self):
        super(Window, self).__init__()
        self.root.geometry('+0+0')

    def display(self):
        comment_label = tkinter.Label(
            text='コメント入力', background='#FFFFFF', foreground='#ff6b91', font=("MSゴシック", 20))

        self.comment_text = tkinter.Entry(self.root, width=50, font=("MSゴシック", 20))
        self.comment_text.configure(background='#FFFFFF')

        # 画像をassetsから取得する
        frame_button_img = Image.open(ASSETS_PATH + '/frameButton.png')
        frame_button_img = ImageTk.PhotoImage(frame_button_img)

        # 画像を表示するためのキャンバスの作成（黒で表示）
        frame_button_canvas = tkinter.Canvas(bg="white", width=80, height=55)

        # キャンバスに画像を表示する。第一引数と第二引数は、x, yの座標
        frame_button_canvas.create_image(0, 0, image=frame_button_img, anchor=tkinter.NW)

        comment_label.grid(row=0, sticky=tkinter.W, column=0, padx=20, pady=5)
        self.comment_text.grid(row=1, sticky=tkinter.W + tkinter.E, column=0, padx=20, pady=5)
        frame_button_canvas.grid(row=2, column=0, columnspan=2, padx=20, pady=5, sticky=tkinter.W)

        self.root.grid_anchor(tkinter.CENTER)
        self.root.withdraw()
        self.root.mainloop()

    def next_button(self, command, mode):
        next_button = tkinter.Button(
            self.root, text='次へ [F12]', width=15, background='#ff6b91', foreground='#FFFFFF', font=("MSゴシック", 15), command=lambda:command(mode))
        next_button.grid(row=1, column=1, sticky=tkinter.E, padx=20, pady=5)

    def rollback_button(self, command):
        self.rollback_img = tkinter.PhotoImage(file=ASSETS_PATH + '/rollback.png').subsample(6, 6)
        rollback_button = tkinter.Button(self.root,background='#FF89A8', command=command, image=self.rollback_img, width=55, height=55, compound="top")
        rollback_button.grid(row=2, column=2, sticky=tkinter.E, padx=20, pady=5)

    def cancel_button(self, command):
        cancel_button = tkinter.Button(
            self.root, text='取り直し', width=15, background='#7F7F7F', foreground='#FFFFFF', font=("MSゴシック", 15), command=command)
        cancel_button.grid(row=1, column=2, sticky=tkinter.E, padx=20, pady=5)

    def get_canvas(self):
        return self.canvas
    
    def get_drawed_screenshot_area(self):
        return self.drawed_screenshot_area
    
    def get_comment_text(self):
        return self.comment_text.get()
    
    def delete_comment_text(self):
        self.comment_text.delete(0, tkinter.END)
    
    def focus_set_comment_text(self):
        self.comment_text.focus_set()

    def canvas(self, press, motion):
        self.canvas = tkinter.Canvas(
            self.root,
            bg="black",
            width=self.root.winfo_screenwidth()*SCALED_POINT,
            height=self.root.winfo_screenheight()*SCALED_POINT
        )

        self.initialized_img = Image.new(
            'RGBA',
            (int(self.root.winfo_screenwidth()*SCALED_POINT), int(self.root.winfo_screenheight()*SCALED_POINT)), 
            'black'
        )
        self.initialized_img_tk = ImageTk.PhotoImage(self.initialized_img)

        # Canvasウィジェットに取得した画像を描画
        self.drawed_screenshot_area = self.canvas.create_image(
            0, 0, image=self.initialized_img_tk, anchor=tkinter.NW, tag="img"
        )

        # イベントとコールバック関数を指定
        self.canvas.bind("<ButtonPress-1>", press)
        self.canvas.bind("<Button1-Motion>", motion)

        self.canvas.grid(row=5, column=0, columnspan=3, padx=20, pady=5)
    
    def get_initialized_img_tk(self):
        return self.initialized_img_tk