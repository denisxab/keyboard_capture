from tkinter import *
from typing import Tuple, Optional

from logic_capture import LogicCapture


class Windows:
    BUTTON: Optional[Button] = None

    def __init__(self):
        super().__init__()
        # INITs
        self.windowTk = Tk()
        position = self.__get_position()
        self.windowTk.geometry('170x50{}'.format(f"+{position[0]}+{position[1]}" if position else "+0+0"))
        self.windowTk.iconbitmap(default='data_image/none.icon')
        self.windowTk.resizable(False, False)
        self.windowTk.title = ""
        self.frameRoot = Frame(self.windowTk)
        self.ButtonLage = Button(self.frameRoot, height=50, width=10, bg='#AEAEAE', command=self.OnClosed)
        # self.windowTk.overrideredirect(1)

        # PACK
        self.frameRoot.pack(fill=BOTH, expand=True)
        self.ButtonLage.pack(fill=BOTH, expand=True)
        # Setting
        self.windowTk.protocol("WM_DELETE_self.windosTkW", self.OnClosed)
        self.windowTk.wm_attributes('-topmost', 1)

        # Logic
        Windows.BUTTON = self.ButtonLage
        LogicCapture()

        # Start
        self.windowTk.mainloop()

    def __save_position(self, x, y):
        with open("data_image/config.txt", 'w') as f:
            f.write(f"{x} {y}")

    def __get_position(self) -> Optional[Tuple[int, int]]:
        try:
            with open("data_image/config.txt", 'r') as f:
                x, y = f.read().split(" ")
                return x, y
        except FileNotFoundError:
            return None

    def OnClosed(self):
        self.__save_position(self.windowTk.winfo_x(), self.windowTk.winfo_y())
        LogicCapture.is_FlagLiveThread = False
        self.windowTk.destroy()

    def __del__(self):
        self.OnClosed()
