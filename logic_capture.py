import threading
import time
from tkinter import PhotoImage
from typing import List, Set

import keyboard
import pyperclip

import viwe
from assistant_pack import get_lang, hunter_key
from assistant_pack.dataconst import translation_key


class LogicCapture:
    KeyPressDown: List[str] = []
    MainLangKeyboard: int = 0
    is_pressAlt: bool = False
    TriggerCopy: bool = False
    TriggerChangeLang: int = 0
    is_FlagLiveThread: bool = True
    ErrorListCodeKey: Set[int] = set()

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
        "Key.space": lambda: LogicCapture.KeyPressDown.append(" ")
    }

    KeyboardOdj = hunter_key.KeyboardHunter()
    MouseObj = hunter_key.MouseHunter()

    def __init__(self):

        # Поток по завхату нажатий клавишь
        threading.Thread(name="ThCaptureKeyBoard",
                         target=hunter_key.KeyboardHunter.ListenKeyboard,
                         args=(lambda *args: 0, self.ThCaptureKeyBoard2), daemon=True).start()

        # Поток по захвату мыши и отчистки KeyPressDown при нажатие ПКМ
        threading.Thread(name="ThCaptureMouse",
                         target=hunter_key.MouseHunter.ListenMouse,
                         args=(lambda *args: 0, lambda *args: LogicCapture.KeyPressDown.clear()), daemon=True).start()

        # Поток по поулчению раскладки клавиотурты
        threading.Thread(name="ThChangeKeyBoard", target=LogicCapture.ThChangKeyBoard, daemon=True).start()

    @staticmethod
    def ThChangKeyBoard():
        GetLang = get_lang.GetLangeKeyBoard()
        while LogicCapture.is_FlagLiveThread:
            newLang = GetLang.get_keyboard_language()
            if newLang != LogicCapture.MainLangKeyboard:
                LogicCapture.MainLangKeyboard = newLang
                fileImage: str = ""
                if newLang == 1:
                    fileImage = "data_image/ru.png"
                elif newLang == 2:
                    fileImage = "data_image/en.png"
                ImageButtonLang = PhotoImage(file=fileImage)
                viwe.Windows.BUTTON["image"] = ImageButtonLang
            time.sleep(1)

    @staticmethod
    def SibelTranslation(false_text: str) -> str:
        # Перевод стороки сивлов на другой язык
        res_text: str = ""

        print(f"Lang: {LogicCapture.MainLangKeyboard}")
        if LogicCapture.MainLangKeyboard == 2:  # En
            for symbol in false_text:
                try:
                    res_text += translation_key[symbol]
                except KeyError:
                    res_text += symbol

        elif LogicCapture.MainLangKeyboard == 1:  # Ru
            res_text = false_text

        return res_text

    @classmethod
    def SetTranslateText(cls, text: str, delFlag=True):
        # перевод раскалки
        NewTranslateKey: str = LogicCapture.SibelTranslation(text)
        # Удалть по символьно только когдаа текст напечанно вручную а не взят из буфера когда выделен текст
        if delFlag:
            # Стиреть слова на неправильной раскладки
            for _ in range(len(NewTranslateKey)):
                keyboard.send("backspace")
        else:
            keyboard.send("backspace")
        # Запись
        cls.KeyboardOdj.TypeTextByKeyBoard(NewTranslateKey)
        # Отчистить массив
        cls.KeyPressDown.clear()

    @classmethod
    def PressDualAlt(cls):
        if cls.is_pressAlt and cls.TriggerChangeLang == int(time.time()):
            if cls.TriggerCopy:
                cls.SetTranslateText(pyperclip.paste(), delFlag=False)
                cls.TriggerCopy = False
            else:
                cls.SetTranslateText("".join(cls.KeyPressDown))

            cls.is_pressAlt = False
        else:
            cls.is_pressAlt = True
            cls.TriggerChangeLang = int(time.time())

    @classmethod
    def ThCaptureKeyBoard2(cls, key):
        try:
            if key.char == '\x03':
                cls.TriggerCopy = True

            cls.KeyPressDown.append(key.char)
            print(f"ThCaptureKeyBoard2\t{cls.KeyPressDown} - {key.char} - {key.vk}")

        except AttributeError:
            try:
                cls.switchKey[str(key)]()
            except KeyError:
                pass
                print(key)


if __name__ == '__main__':
    pass
