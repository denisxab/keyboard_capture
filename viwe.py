import threading
import time
from tkinter import *

import get_lang
import logic_capture


class Windows(logic_capture.LogicCapture):

    def __init__(self):
        super().__init__()
        # INIT
        self.windowTk = Tk()
        self.windowTk.geometry('{}x{}'.format('170', '80'))
        self.frameRoot = Frame(self.windowTk)
        self.langKeyBoard: str = ""
        self.ImageButtonLange: PhotoImage = PhotoImage()
        self.ButtonLage = Button(self.frameRoot, height=50, width=10, bg='#AEAEAE',
                                 command=logic_capture.LogicCapture.ChangeLangeKeyBoard)

        threading.Thread(name="ThChengKeyBoard", target=self.ThChengKeyBoard, daemon=True).start()

        # PACK
        self.frameRoot.pack(fill=BOTH, expand=True)
        self.ButtonLage.pack(fill=BOTH, expand=True)
        # Setting
        self.windowTk.protocol("WM_DELETE_self.windosTkW", self.OnClosed)
        self.windowTk.wm_attributes('-topmost', 1)
        # self.windowTk.overrideredirect(1)
        self.windowTk.mainloop()

    def ThChengKeyBoard(self):
        newLang: str = ""
        get_class = get_lang.GetLangeKeyboar()
        while logic_capture.LogicCapture.is_FlagLiveThread:
            newLang = get_class.get_keyboard_language()
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
        logic_capture.LogicCapture.is_FlagLiveThread = False
        self.windowTk.destroy()

    def __del__(self):
        logic_capture.LogicCapture.is_FlagLiveThread = False


if __name__ == '__main__':
    Windows()
