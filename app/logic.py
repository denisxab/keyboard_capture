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
    # switchKey = {
    #     # Отчистка массива при смене фокуса
    #     "Key.enter": lambda: LogicCapture.KeyLettersAlphabet.clear(),
    #     "Key.backspace": lambda: LogicCapture.KeyLettersAlphabet.clear(),
    #     "Key.delete": lambda: LogicCapture.KeyLettersAlphabet.clear(),
    #     "Key.up": lambda: LogicCapture.KeyLettersAlphabet.clear(),
    #     "Key.down": lambda: LogicCapture.KeyLettersAlphabet.clear(),
    #     "Key.left": lambda: LogicCapture.KeyLettersAlphabet.clear(),
    #     "Key.right": lambda: LogicCapture.KeyLettersAlphabet.clear(),
    #     "Key.shift": lambda: LogicCapture._ChangeLang(),
    #     # При вызове перевода
    #     "Key.alt_l": lambda: LogicCapture._PressDualAlt(),
    #     # добавить пробелы
    #     "Key.space": lambda: LogicCapture.KeyLettersAlphabet.append(0),
    #     "Key.ctrl_r": lambda: printDebug(f"[HASH]\t{LogicCapture._ConversionListCodeKeyToSir()}"),
    #     "Key.ctrl_l": lambda: LogicCapture._CopyTrigger()
    # }

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
    def _SetTranslateText(cls, text: str, delFlag=True):
        printDebug(f"[INPUT]\t{text}")
        # перевод раскладки
        NewTranslateKey: List[str] = cls._SibelTranslation(text)
        ln = len(NewTranslateKey)
        printDebug(f"[ LEN]\t{ln}")
        printDebug(f"[ RES]\t{NewTranslateKey}")

        if not delFlag:
            cls.KeyboardOdj.KeyBoard.tap(keyboard.Key.right)
            cls.SkipTrigger = (ln * 4) + 1
        else:
            cls.SkipTrigger = ln * 4

        # Стереть слова на неправильной раскладки
        for _ in range(ln):
            kb.send("backspace")

        kb.write(NewTranslateKey, delay=0.05)

        cls.KeyLettersAlphabet.clear()

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
    # @classmethod
    # def _CopyTrigger(cls):
    #     cls.TriggerCopy = True

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
                             61: "f3"
                             }
        HotKey: List[str] = []

        ArrHotKey: Dict = {
            37.5: lambda: printDebug("[COPY]"),
            61.0: lambda: printDebug(f"{LogicCapture._ConversionListCodeKeyToSir()}"),
            30.0: lambda: LogicCapture._SetTranslateText(LogicCapture._ConversionListCodeKeyToSir())
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
                if ArrKeySpecialKeys.get(sc, False):
                    if et and SpecialSelectKey[0] == False:
                        SpecialSelectKey[0] = True
                        SpecialSelectKey[1] = sc
                        HotKey.clear()
                        HotKey.append(sc)
                        printDebug(f"[SelectKey]\t{SpecialSelectKey}")

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
                mean = sum(HotKey) / len(HotKey)
                printDebug(f"[SelectKey]\t{SpecialSelectKey}")
                printDebug(f"[HotKey]\t{HotKey}")
                printDebug(f"[Mean HotKey]\t{mean}")
                printDebug(f"[LKA 2]\t{LogicCapture.KeyLettersAlphabet}")

                # Верификация множественного нажатия на alt + shift
                if len(HotKey) > 1 and HotKey[0] in (56, 42) and HotKey[1] in (56, 42):
                    if len(HotKey[1:]) % 2 != 0:
                        LogicCapture.MainLangKeyboard = 'en' if LogicCapture.MainLangKeyboard == 'ru' else 'ru'
                    printDebug(f"[MainLangKeyboard]\t{LogicCapture.MainLangKeyboard}")
                    # LogicCapture._SetTranslateText(LogicCapture._ConversionListCodeKeyToSir())

                # Если печатали с зажатым shift
                elif HotKey[0] == 42 and len(HotKey) > 1:
                    printDebug(f"[Shift Key]\t{HotKey[1:]}")
                    for key_iter in HotKey[1:]:
                        if not ArrKeySpecialKeys.get(key_iter, False):
                            LogicCapture.KeyLettersAlphabet.append(key_iter * -1)

                else:
                    if ArrHotKey.get(mean, False):
                        ArrHotKey[mean]()

                return None

            if not et:
                LogicCapture.KeyLettersAlphabet.append(sc)
                printDebug(f"[KeyClick]\t{sc}")
                printDebug(f"[LKA 1]\t{LogicCapture.KeyLettersAlphabet}")

            # printDebug(f"{event.name} - {sc}")
            #
            # nonlocal ShiftTrigger, TriggerChangeLang, TriggerCopy
            #
            # # Принудительно зактрыть поток
            # if not cls.is_FlagLiveThread:
            #     keyboard.unhook_all()
            #     sys.exit(-1)
            #
            # # Клавиши при нажатие которые отчищают массив
            # if event.scan_code in (14, 28, 1, 83, 75, 72, 80, 77):  # Enter; Backspace; Esc; Delete; Стрелки перемещения
            #     # Отчиска массива при смене фокуса
            #     LogicCapture.PressedKeys.clear()
            #     return None
            #
            # # Обработка печататния с зажатым shift
            # if event.name == "shift" and event.event_type == 'down':  # обработать зжатия Shift -
            #     ShiftTrigger = 1000
            # elif event.name == "shift" and event.event_type == 'up':
            #     ShiftTrigger = 0
            #
            # # Обработка копирования текста
            # if event.name == "ctrl":
            #     if event.event_type == "down":
            #         TriggerCopy = 1
            #     else:
            #         return None
            # if event.scan_code == 46:  # "c"
            #     if TriggerCopy == 1 and event.event_type == "up":
            #         TriggerCopy = 2
            #         return None
            #
            # # Обработка тригера комбинации перевода текста с задержко по времни нажатия в 1 секунуд
            # if event.name == 'alt' and event.event_type == 'up':
            #     ShiftTrigger = 0
            #     if TriggerChangeLang == int(time.time()):
            #         if TriggerCopy == 2:
            #             LogicCapture.SetTranslateText(pyperclip.paste(), delFlag=False)
            #         else:
            #             LogicCapture.SetTranslateText(LogicCapture.CodeKeyTranslation(LogicCapture.PressedKeys),
            #                                           delFlag=True)
            #     else:
            #         TriggerChangeLang = int(time.time())
            #     return None
            #
            # else:
            #     # Запись нажатых клавишь с учетом печатанью через Shift
            #     if event.event_type == "up":
            #         LogicCapture.PressedKeys.append(event.scan_code + ShiftTrigger)
            #         TriggerCopy = 0
            #
            # log.debug(LogicCapture.CodeKeyTranslation(LogicCapture.PressedKeys))  # DEBUG
            #

        # Отчистка буфера обмена
        if windll.user32.OpenClipboard(None):
            windll.user32.EmptyClipboard()
            windll.user32.CloseClipboard()
        kb.hook(pressed_keys)
        kb.wait()

        # if cls.SkipTrigger == 0:
        #
        #     if hasattr(key, 'char'):
        #         printDebug(f"164: {cls.PressedKeys}", key="Обработка нажатий")
        #
        #         if cls.TriggerCopy and key.vk == 67:
        #             printDebug(f"[COPY]\t{paste()}", key="Обработка нажатий")
        #
        #         try:
        #             if key.vk:
        #                 if key.char.istitle():
        #                     cls.PressedKeys.append(key.vk * -1)
        #
        #                 else:
        #                     cls.PressedKeys.append(key.vk)
        #
        #         except (AttributeError, TypeError) as e:
        #             printDebug(f"179: {e}", key="Обработка нажатий; Ошибки")
        #
        #     else:
        #         try:
        #             # Слежка за сменой раскладки клавиатуры
        #             if cls.TriggerChangeLang and str(key) == "Key.alt_l":
        #                 cls.MainLangKeyboard = 'en' if cls.MainLangKeyboard == 'ru' else 'ru'
        #                 printDebug(f"185: {cls.MainLangKeyboard} = {fileImage[LogicCapture.MainLangKeyboard]}",
        #                               key="Обработка нажатий; Смена языка")
        #             else:
        #                 cls.TriggerChangeLang = False
        #
        #             if str(key) != "Key.alt_l":
        #                 cls.TriggerCopy = False
        #
        #             cls.switchKey[str(key)]()
        #             printDebug(f"190: {key}", key="Обработка нажатий")
        #         except KeyError as e:
        #             printDebug(f"193: {e}", key="Обработка нажатий; Ошибки")
        #
        # else:
        #     cls.SkipTrigger -= 1


if __name__ == '__main__':
    pass
