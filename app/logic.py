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
    CopyBuffer: str = ""

    KeyboardOdj = KeyboardHunter()
    MouseObj = MouseHunter()

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

        kb.write(NewTranslateKey, delay=0.05)
        cls.KeyLettersAlphabet.clear()
        cls.CopyBuffer = ""

    # @classmethod
    # def _PressDualAlt(cls):
    #     if cls.is_pressAlt and cls.TriggerConvectionLang == int(time.time()):
    #         if cls.TriggerCopy:
    #             cls._SetTranslateText(paste(), delFlag=False)
    #             cls.TriggerCopy = False
    #             printDebug(f"120: Copy")
    #
    #         else:
    #             printDebug(f"123 {cls._ConversionListCodeKeyToSir()}")
    #             cls._SetTranslateText(cls._ConversionListCodeKeyToSir())
    #
    #         cls.is_pressAlt = False
    #
    #     else:
    #         cls.is_pressAlt = True
    #         cls.TriggerConvectionLang = int(time.time())
    # @classmethod
    # def _ChangeLang(cls):
    #     cls.TriggerChangeLang = True
    #
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
    def ThCaptorFeKeyBoard(cls, key):

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

        ArrHotKey: Dict = {
            (29, 46): lambda: LogicCapture._CopyTrigger(),
            (61,): lambda: printDebug(f"{LogicCapture._ConversionListCodeKeyToSir()}"),
            (56, 44): lambda: LogicCapture._SetTranslateText(LogicCapture._ConversionListCodeKeyToSir())
        }

        def pressed_keys(event):
            nonlocal SpecialSelectKey, HotKey, ArrKeySpecialKeys
            """
            event_type - нажати || отжатие
            name - имя клавиши
            scan_code - номер клавиши
            time - время когда нажата
            """

            sc = event.scan_code
            et = 1 if event.event_type == 'down' else 0

            if SpecialSelectKey[1] != sc:

                if sc in (541,):
                    # 541 alt up вредная клавиша неизвестного происхождения
                    return None

                if ArrKeySpecialKeys.get(sc, False):
                    if et and SpecialSelectKey[0] == False:
                        SpecialSelectKey[0] = True
                        SpecialSelectKey[1] = sc
                        HotKey.clear()
                        HotKey.append(sc)
                        printDebug(f"[SelectKey]\t{SpecialSelectKey}")
                        return None

                    elif et:
                        HotKey.append(sc)

                    if not sc in (61, 42, 56):  # Если это не F3, Alt_l, Shift_l
                        LogicCapture.KeyLettersAlphabet.clear()

                    return None

                elif not et and SpecialSelectKey[0] == True:
                    HotKey.append(sc)
                    printDebug(f"[Hot]\t\t{sc}")
                    return None

            elif not et:
                SpecialSelectKey[0] = False
                SpecialSelectKey[1] = -1
                printDebug(f"[SelectKey]\t{SpecialSelectKey}")
                printDebug(f"[HotKey]\t{HotKey}")
                printDebug(f"[LKA 2]\t{LogicCapture.KeyLettersAlphabet}")

                # Верификация множественного нажатия на alt + shift
                if len(HotKey) > 1 and HotKey[0] in (56, 42) and HotKey[1] in (56, 42):
                    if len(HotKey[1:]) % 2 != 0:
                        LogicCapture.MainLangKeyboard = 'en' if LogicCapture.MainLangKeyboard == 'ru' else 'ru'
                    printDebug(f"[MainLangKeyboard]\t{LogicCapture.MainLangKeyboard}")

                # Если печатали с зажатым shift
                elif HotKey[0] == 42 and len(HotKey) > 1:
                    printDebug(f"[Shift Key]\t{HotKey[1:]}")
                    for key_iter in HotKey[1:]:
                        if not ArrKeySpecialKeys.get(key_iter, False):
                            LogicCapture.KeyLettersAlphabet.append(key_iter * -1)

                else:
                    if ArrHotKey.get(tuple(HotKey), False):
                        ArrHotKey[tuple(HotKey)]()

                return None

            if not et:
                LogicCapture.KeyLettersAlphabet.append(sc)
                printDebug(f"[KeyClick]\t{sc}")
                printDebug(f"[LKA 1]\t{LogicCapture.KeyLettersAlphabet}")

        # Отчистка буфера обмена
        if windll.user32.OpenClipboard(None):
            windll.user32.EmptyClipboard()
            windll.user32.CloseClipboard()
        kb.hook(pressed_keys)
        kb.wait()


if __name__ == '__main__':
    pass
