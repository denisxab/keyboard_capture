import sys
import threading
import time
from typing import List, Dict

import keyboard as kb

from pyperclip import paste
from pynput import keyboard
from ctypes import windll

from app.assistant_pack.log_debug import printDebug
from app.assistant_pack import hunter_key
from app.general_data import keyCode

from app.assistant_pack.hunter_key import translation_key_En_Ru, translation_key_Ru_En, MouseHunter, KeyboardHunter


class LogicCapture:
    KeyLettersAlphabet: List[int] = []
    MainLangKeyboard: str = hunter_key.GetLangKeyBoard.get()
    SkipTrigger: int = 0
    TriggerConvectionLang: int = 0
    TriggerChangeLang: int = 0
    is_pressAlt: bool = False
    TriggerCopy: bool = False

    is_FlagLiveThread: bool = True

    MouseObj = MouseHunter()

    SpecialSelectKey: List = [False, -1]
    ArrKeySpecialKeys = {29: "crt_l",
                         42: "shift",
                         56: "alt",
                         14: "backspace",
                         83: "del",
                         75: "<",
                         77: ">",
                         72: "^",
                         80: "^",
                         28: "enter",
                         1: "esc",
                         61: "f3",
                         }
    HotKey: List[str] = []
    CopyBuffer: str = ""
    ArrHotKey: Dict = {
        (29, 46): lambda: LogicCapture._CopyTrigger(),
        (61,): lambda: printDebug(f"{LogicCapture._ConversionListCodeKeyToSir()}"),
        (56, 44): lambda: LogicCapture._SetTranslateText(LogicCapture._ConversionListCodeKeyToSir())
    }

    def __init__(self, ):

        # Поток по захвату нажатий клавиш
        threading.Thread(name="ThCaptureKeyBoard",
                         target=KeyboardHunter.ListenKeyboard,
                         args=(lambda *args: 0, self.ThCaptorFeKeyBoard),
                         daemon=True).start()

        # Поток по захвату мыши и отчистки PressedKeys при нажатии ПКМ
        threading.Thread(name="ThCaptureMouse",
                         target=MouseHunter.ListenMouse,
                         args=(lambda *args: 0, self.PressMouse),
                         daemon=True).start()

    @classmethod
    def _SibelTranslation(cls, text: str) -> List[str]:
        # Перевод строки символов на другой язык
        res_text: List[str] = []

        select_transected = {
            "ru": translation_key_Ru_En,
            "en": translation_key_En_Ru,
        }[cls.MainLangKeyboard]
        for symbol in text:
            res_text.append(select_transected.get(symbol, ""))
        return res_text

    @classmethod
    def _SetTranslateText(cls, text: str):

        if cls.CopyBuffer:
            printDebug(f"[INPUT COPY]\t{cls.CopyBuffer}")
            # перевод раскладки
            NewTranslateKey: List[str] = cls._SibelTranslation(cls.CopyBuffer)
            ln = len(NewTranslateKey)
            printDebug(f"[ LEN]\t{ln}")
            printDebug(f"[ RES]\t{NewTranslateKey}")
            # Стереть слова на неправильной раскладки
            kb.send("backspace")


        else:
            printDebug(f"[INPUT]\t{text}")
            # перевод раскладки
            NewTranslateKey: List[str] = cls._SibelTranslation(text)
            ln = len(NewTranslateKey)
            printDebug(f"[ LEN]\t{ln}")
            printDebug(f"[ RES]\t{NewTranslateKey}")
            # Стереть слова на неправильной раскладки
            for _ in range(ln):
                kb.send("backspace")

        try:
            kb.write(NewTranslateKey, delay=0.05)
            cls.KeyLettersAlphabet.clear()
            cls.CopyBuffer = ""
        except ValueError:
            printDebug(f"Warning RES Empty !")

    @classmethod
    def _CopyTrigger(cls):
        cls.CopyBuffer = paste()
        printDebug("[COPY]")

    @classmethod
    def PressMouse(cls, *args):
        if cls.is_FlagLiveThread:
            LogicCapture.KeyLettersAlphabet.clear()
        else:
            sys.exit(0)

    @classmethod
    def _ConversionListCodeKeyToSir(cls) -> str:
        if cls.KeyLettersAlphabet:
            try:
                return "".join(
                    [keyCode[key * -1].upper() if key < 0 else keyCode[key] for key in
                     cls.KeyLettersAlphabet])
            except Exception as  e:
                print(f"{e} == {cls.KeyLettersAlphabet}")
        else:
            return ""

    @classmethod
    def pressed_keys(cls, event):

        """
        event_type - нажати || отжатие
        name - имя клавиши
        scan_code - номер клавиши
        time - время когда нажата
        """

        sc = event.scan_code
        et = 1 if event.event_type == 'down' else 0

        if cls.SpecialSelectKey[1] != sc:

            if sc in (541,):
                # 541 alt up вредная клавиша неизвестного происхождения
                return None

            if cls.ArrKeySpecialKeys.get(sc, False):
                if et and cls.SpecialSelectKey[0] == False:
                    cls.SpecialSelectKey[0] = True
                    cls.SpecialSelectKey[1] = sc
                    cls.HotKey.clear()
                    cls.HotKey.append(sc)
                    printDebug(f"[SelectKey]\t{cls.SpecialSelectKey}")
                    return None

                elif et:
                    cls.HotKey.append(sc)

                if not sc in (61, 42, 56):  # Если это не F3, Alt_l, Shift_l
                    LogicCapture.KeyLettersAlphabet.clear()
                return None

            elif not et and cls.SpecialSelectKey[0] == True:
                cls.HotKey.append(sc)
                printDebug(f"[Hot]\t\t{sc}")
                return None

        elif not et:
            cls.SpecialSelectKey[0] = False
            cls.SpecialSelectKey[1] = -1
            printDebug(f"[SelectKey]\t{cls.SpecialSelectKey}")
            printDebug(f"[HotKey]\t{cls.HotKey}")
            printDebug(f"[LKA 2]\t{cls.KeyLettersAlphabet}")

            # Верификация множественного нажатия на alt + shift
            if len(cls.HotKey) > 1 and cls.HotKey[0] in (56, 42) and cls.HotKey[1] in (56, 42):
                if len(cls.HotKey[1:]) % 2 != 0:
                    LogicCapture.MainLangKeyboard = 'en' if cls.MainLangKeyboard == 'ru' else 'ru'
                printDebug(f"[MainLangKeyboard]\t{cls.MainLangKeyboard}")

            # Если печатали с зажатым shift
            elif cls.HotKey[0] == 42 and len(cls.HotKey) > 1:
                printDebug(f"[Shift Key]\t{cls.HotKey[1:]}")
                for key_iter in cls.HotKey[1:]:
                    if not cls.ArrKeySpecialKeys.get(key_iter, False):
                        cls.KeyLettersAlphabet.append(key_iter * -1)

            else:
                if cls.ArrHotKey.get(tuple(cls.HotKey), False):
                    cls.ArrHotKey[tuple(cls.HotKey)]()

            return None

        if not et:
            cls.KeyLettersAlphabet.append(sc)
            printDebug(f"[KeyClick]\t{sc}")
            printDebug(f"[LKA 1]\t{cls.KeyLettersAlphabet}")

    @classmethod
    def ThCaptorFeKeyBoard(cls, key):
        # Отчистка буфера обмена
        if windll.user32.OpenClipboard(None):
            windll.user32.EmptyClipboard()
            windll.user32.CloseClipboard()
        kb.hook(LogicCapture.pressed_keys)
        kb.wait()


if __name__ == '__main__':
    pass
