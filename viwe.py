from tkinter import *
from typing import Optional

from logic_capture import LogicCapture


class Windows:
    BUTTON: Optional[Button] = None

    def __init__(self):
        super().__init__()
        # INIT
        self.windowTk = Tk()
        self.windowTk.geometry(f'{self.get_position()}')
        self.windowTk.iconbitmap(default='data_image/none.icon')
        self.windowTk.resizable(False, False)
        self.windowTk.title = ""
        self.frameRoot = Frame(self.windowTk)
        self.ButtonLage = Button(self.frameRoot, height=50, width=10, bg='#AEAEAE', command=self.OnClosed)

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

    def get_position(self) -> str:
        try:
            with open("data_image/config.txt", 'r') as f:
                x, y = f.read().split(" ")
                self.windowTk.overrideredirect(1)
                return f"{80}x{50}+{x}+{y}"
        except FileNotFoundError:
            return f"{80}x{50}+{self.windowTk.winfo_screenwidth() - 90}+{self.windowTk.winfo_screenheight() // 2}"

    @staticmethod
    def save_position(x, y):
        with open("data_image/config.txt", 'w') as f:
            f.write(f"{x} {y}")

    def OnClosed(self):
        Windows.save_position(self.windowTk.winfo_x(), self.windowTk.winfo_y())
        LogicCapture.is_FlagLiveThread = False
        self.windowTk.destroy()
