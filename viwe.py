from tkinter import *
from typing import Optional, Tuple, List

from logic_capture import LogicCapture


class Windows:
    BUTTON: Optional[Button] = None
    HT = 80
    WT = 50

    def __init__(self):
        super().__init__()
        # INIT
        self.windowTk = Tk()
        self.windowTk.geometry(
            f"{160}x{160}+{self.windowTk.winfo_screenwidth() // 2 - 160}+{self.windowTk.winfo_screenheight() // 2 - 160}")
        self.frameRoot = Frame(self.windowTk)
        self.ButtonLage = Button(self.frameRoot, height=50, width=10, bg='#AEAEAE',
                                 command=self.__ShowPositionButtonAndHideButtonLange)
        self.__CreateButtonChangePosition()

        # PACK
        self.__ShowPositionButtonAndHideButtonLange()

        # Setting
        self.windowTk.protocol("WM_DELETE_self.windosTkW", self.OnClosed)
        self.windowTk.wm_attributes('-topmost', 1)
        self.windowTk.overrideredirect(1)
        self.windowTk.resizable(False, False)
        self.windowTk.iconbitmap(default='data_image/none.icon')
        self.windowTk.title = ""

        # Logic
        Windows.BUTTON = self.ButtonLage
        LogicCapture()

        # Start
        self.windowTk.mainloop()

    def __ShowPositionButtonAndHideButtonLange(self):
        self.frameRoot.pack_forget()
        self.ButtonLage.pack_forget()

        self.TableFrame.pack()
        self.bt1.grid(row=1, column=1)
        self.bt8.grid(row=1, column=2)
        self.bt7.grid(row=1, column=3)

        self.bt2.grid(row=2, column=1)
        self.btClose.grid(row=2, column=2)
        self.bt6.grid(row=2, column=3)

        self.bt3.grid(row=3, column=1)
        self.bt4.grid(row=3, column=2)
        self.bt5.grid(row=3, column=3)

        self.windowTk.geometry(
            f"{160}x{160}+{self.windowTk.winfo_screenwidth() // 2 - 80}+{self.windowTk.winfo_screenheight() // 2 - 80}")
        self.windowTk.update()

    def __CreateButtonChangePosition(self):
        """
        8 кнопок перемещения
        +   ^   +
        <   X   >
        +   v   +
        """
        positionArr: List[Tuple[int, int]] = [
            (0, 0),
            (0, self.windowTk.winfo_screenheight() // 2),
            (0, self.windowTk.winfo_screenheight() - Windows.WT),
            (self.windowTk.winfo_screenwidth() // 2, self.windowTk.winfo_screenheight() - Windows.WT),
            (self.windowTk.winfo_screenwidth() - Windows.HT, self.windowTk.winfo_screenheight() - Windows.WT),

            (self.windowTk.winfo_screenwidth() - Windows.HT,
             self.windowTk.winfo_screenheight() // 2),

            (self.windowTk.winfo_screenwidth() - Windows.HT, 0),
            (self.windowTk.winfo_screenwidth() // 2, 0)
        ]
        self.TableFrame = Frame(self.windowTk)

        h = 3
        w = 6
        color = '#BDFFD1'
        self.bt1 = Button(self.TableFrame, height=h, width=w, bg=color, text="+",
                          command=lambda: self.ChangePositionAndShowButtonLange(positionArr[0]))
        self.bt2 = Button(self.TableFrame, height=h, width=w, bg=color, text="<",
                          command=lambda: self.ChangePositionAndShowButtonLange(positionArr[1]))

        self.bt3 = Button(self.TableFrame, height=h, width=w, bg=color, text="+",
                          command=lambda: self.ChangePositionAndShowButtonLange(positionArr[2]))

        self.bt4 = Button(self.TableFrame, height=h, width=w, bg=color, text="v",
                          command=lambda: self.ChangePositionAndShowButtonLange(positionArr[3]))
        self.bt5 = Button(self.TableFrame, height=h, width=w, bg=color, text="+",
                          command=lambda: self.ChangePositionAndShowButtonLange(positionArr[4]))
        self.bt6 = Button(self.TableFrame, height=h, width=w, bg=color, text=">",
                          command=lambda: self.ChangePositionAndShowButtonLange(positionArr[5]))
        self.bt7 = Button(self.TableFrame, height=h, width=w, bg=color, text="+",
                          command=lambda: self.ChangePositionAndShowButtonLange(positionArr[6]))
        self.bt8 = Button(self.TableFrame, height=h, width=w, bg=color, text="^",
                          command=lambda: self.ChangePositionAndShowButtonLange(positionArr[7]))

        self.btClose = Button(self.TableFrame, height=h, width=w, bg="#FF9C83", text="x",
                              command=lambda: self.OnClosed())

    def ChangePositionAndShowButtonLange(self, pos: Tuple[int, int]):
        self.TableFrame.pack_forget()
        self.bt1.grid_forget()
        self.bt8.grid_forget()
        self.bt7.grid_forget()
        self.bt2.grid_forget()
        self.btClose.grid_forget()
        self.bt6.grid_forget()
        self.bt3.grid_forget()
        self.bt4.grid_forget()
        self.bt5.grid_forget()

        self.frameRoot.pack(fill=BOTH, expand=True)
        self.ButtonLage.pack(fill=BOTH, expand=True)

        X, Y = pos
        self.windowTk.geometry(f'{Windows.HT}x{Windows.WT}+{X}+{Y}')
        self.windowTk.update()

    def OnClosed(self):
        LogicCapture.is_FlagLiveThread = False
        self.windowTk.destroy()
