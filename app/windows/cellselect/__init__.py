from app.windows.screencaptor import ScreenCaptor
from app.services.manual import Manual
from app.windows.cellselect.window import Window

class CellSelect:
    def __init__(self, path):
        self.path = path
        self.window = Window()
        self.window.confirm_button(self.__confirm)
        self.window.display()

    def __confirm(self):
        cell = self.window.get_cell_entry()
        self.window.destroy()
        ScreenCaptor(Manual(self.path, mode=1, cell=cell))
        self.window.quit()