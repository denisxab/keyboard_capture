import sys
import threading
import time
from typing import List

from pyperclip import paste
from pynput import keyboard

from app.assistant_pack import log_debug as lg
from app.assistant_pack.hunter_key import translation_key, MouseHunter, KeyboardHunter

lg.DEBUG_PRINT = 0


class LogicCapture:
    KeyPressDown: List[str] = []
    MainLangKeyboard: int = 0
    is_pressAlt: bool = False
    TriggerCopy: bool = False
    TriggerChangeLang: int = 0
    is_FlagLiveThread: bool = True
    SkipTrigger: int = 0
    switchKey = {
        # Отчиска массива при смене фокуса
        "Key.enter": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.backspace": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.delete": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.up": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.down": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.left": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.right": lambda: LogicCapture.KeyPressDown.clear(),
        # При вызаве перевода
        "Key.alt_l": lambda: LogicCapture.PressDualAlt(),
        # добавть пробелы
        "Key.space": lambda: LogicCapture.KeyPressDown.append(" "),
        "Key.ctrl_r": lambda: print(
            f"[HASH]\t{''.join(LogicCapture.KeyPressDown)}") if LogicCapture.KeyPressDown else print("[HASH]\t~\t~\t~"),
        "Key.ctrl_l": lambda: LogicCapture.CopyTrigger()
    }

    KeyboardOdj = KeyboardHunter()
    MouseObj = MouseHunter()

    def __init__(self):

        # Поток по завхату нажатий клавишь
        threading.Thread(name="ThCaptureKeyBoard",
                         target=KeyboardHunter.ListenKeyboard,
                         args=(lambda *args: 0, self.ThCaptureKeyBoard2),
                         daemon=True).start()

        # Поток по захвату мыши и отчистки KeyPressDown при нажатие ПКМ
        threading.Thread(name="ThCaptureMouse",
                         target=MouseHunter.ListenMouse,
                         args=(lambda *args: 0, self.PressMouse),
                         daemon=True).start()

    @staticmethod
    def SibelTranslation(false_text: str) -> str:
        # Перевод стороки сивлов на другой язык
        res_text: str = ""

        # print(f"Lang: {LogicCapture.MainLangKeyboard}")

        for symbol in false_text:
            try:
                res_text += translation_key[symbol]
            except KeyError:
                res_text += symbol

        return res_text

    @classmethod
    def SetTranslateText(cls, text: str, delFlag=True):
        # перевод раскалки
        NewTranslateKey: str = LogicCapture.SibelTranslation(text)
        # Удалть по символьно только когдаа текст напечанно вручную а не взят из буфера когда выделен текст
        if delFlag:
            cls.SkipTrigger = len(NewTranslateKey)
            # Стиреть слова на неправильной раскладки
            for _ in range(cls.SkipTrigger):
                cls.KeyboardOdj.Click(keyboard.Key.backspace)
                # keyboard.send("backspace")
        else:
            cls.KeyboardOdj.Click(keyboard.Key.backspace)
            # keyboard.send("backspace")

        print(f"[RESU]\t{''.join(cls.KeyPressDown)} > {NewTranslateKey}")

        # Запись
        cls.KeyboardOdj.TypeTextByKeyBoard(NewTranslateKey)
        cls.KeyPressDown.clear()

    @classmethod
    def PressDualAlt(cls):
        if cls.is_pressAlt and cls.TriggerChangeLang == int(time.time()):
            if cls.TriggerCopy:
                cls.SetTranslateText("".join(cls.KeyPressDown), delFlag=False)
                cls.TriggerCopy = False
            else:
                cls.SetTranslateText("".join(cls.KeyPressDown))

            cls.is_pressAlt = False

        else:
            cls.is_pressAlt = True
            cls.TriggerChangeLang = int(time.time())

    @classmethod
    def CopyTrigger(cls):
        cls.TriggerCopy = True

    @classmethod
    def PressMouse(cls, *args):
        if cls.is_FlagLiveThread:
            LogicCapture.KeyPressDown.clear()
        else:
            sys.exit(0)

    @classmethod
    def ThCaptureKeyBoard2(cls, key):
        if LogicCapture.is_FlagLiveThread:
            try:
                if key.char:
                    if cls.TriggerCopy and key.vk == 67:
                        cls.KeyPressDown = list(item for item in paste())
                        print(f"[COPY]\t{''.join(cls.KeyPressDown)}")
                    elif cls.SkipTrigger == 0:
                        cls.KeyPressDown.append(key.char)
                    else:
                        cls.SkipTrigger -= 1

            except AttributeError:
                try:
                    cls.switchKey[str(key)]()
                except KeyError:

                    lg.printDebug(key)
        else:
            sys.exit(0)


if __name__ == '__main__':
    pass
