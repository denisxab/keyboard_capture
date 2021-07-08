import threading
import time
from tkinter import *
from typing import Tuple, Optional

import logic_capture
from pack import get_lang


class Windows(logic_capture.LogicCapture):

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
        self.langKeyBoard: str = ""
        self.ImageButtonLange: PhotoImage = PhotoImage()
        self.ButtonLage = Button(self.frameRoot, height=50, width=10, bg='#AEAEAE', command=self.OnClosed)

        threading.Thread(name="ThChengKeyBoard", target=self.ThChengKeyBoard, daemon=True).start()

        # PACK
        self.frameRoot.pack(fill=BOTH, expand=True)
        self.ButtonLage.pack(fill=BOTH, expand=True)
        # Setting
        self.windowTk.protocol("WM_DELETE_self.windosTkW", self.OnClosed)
        self.windowTk.wm_attributes('-topmost', 1)
        # self.windowTk.overrideredirect(1)
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

    def ThChengKeyBoard(self):

        GetLang = get_lang.GetLangeKeyBoard()
        while logic_capture.LogicCapture.is_FlagLiveThread:
            newLang = GetLang.get_keyboard_language()
            if newLang != self.langKeyBoard:
                self.langKeyBoard = newLang
                fileImage: str = ""
                if newLang == 'Russian':
                    fileImage = "data_image/ru.png"
                elif newLang == "English - United States":
                    fileImage = "data_image/en.png"
                self.ImageButtonLange = PhotoImage(file=fileImage)
                self.ButtonLage["image"] = self.ImageButtonLange
        time.sleep(1)

    def OnClosed(self):
        self.__save_position(self.windowTk.winfo_x(), self.windowTk.winfo_y())
        logic_capture.LogicCapture.is_FlagLiveThread = False
        self.windowTk.destroy()

    def __del__(self):
        self.OnClosed()
