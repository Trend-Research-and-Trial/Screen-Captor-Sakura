import tkinter
from settings import ASSETS_PATH, TITLE

class Base:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title(TITLE)
        self.root.configure(background='#FFFFFF')
        self.root.iconbitmap(ASSETS_PATH + '/trat.ico')

    def destroy(self):
        self.root.destroy()

    def quit(self):
        self.root.quit()

    def deiconify(self):
        self.root.deiconify()

    def withdraw(self):
        self.root.withdraw()
    
    def winfo_viewable():
        return self.root.winfo_viewable()