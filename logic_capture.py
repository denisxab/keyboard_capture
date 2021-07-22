import threading
import threading
import time
from tkinter import PhotoImage
from typing import List

import keyboard
import pyperclip

import viwe
from assistant_pack import get_lang, hunter_key
from assistant_pack.dataconst import translation_key_EN_RU


# logging.basicConfig(
#     handlers=[logging.FileHandler(filename="log_file/logic_capture.log", encoding='utf-8', mode='w')],
#     format="%(asctime)s %(name)s:\t%(funcName)s:\t%(thread)d:\t%(levelname)s:\t%(message)s",
#     datefmt="%F %T",
#     level=logging.DEBUG)
# log = logging.getLogger("logic")


class LogicCapture:
    KeyPressDown: List[str] = []
    MainLangKeyboard: int = 0
    is_pressAlt: bool = False
    TriggerCopy: bool = False
    TriggerChangeLang: int = 0
    is_FlagLiveThread: bool = True

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
        "Key.alt_l": lambda: LogicCapture.PressDualAlt()
    }

    KeyboardOdj = hunter_key.KeyboardHunter()
    MouseObj = hunter_key.MouseHunter()

    def __init__(self):

        # Поток по завхату нажатий клавишь
        threading.Thread(name="ThCaptureKeyBoard",
                         target=hunter_key.KeyboardHunter.ListenKeyboard,
                         args=(lambda *args: 0, self.ThCaptureKeyBoard2),
                         ).start()

        # Поток по захвату мыши и отчистки KeyPressDown при нажатие ПКМ
        threading.Thread(name="ThCaptureMouse",
                         target=hunter_key.MouseHunter.ListenMouse,
                         args=(lambda *args: 0, lambda *args: LogicCapture.KeyPressDown.clear()),
                         ).start()

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

    # Перевод стороки сивлов на другой язык
    @staticmethod
    def SibelTranslation(false_text: str) -> str:
        res_text: str = ""

        if LogicCapture.MainLangKeyboard == 2:  # En
            for symbol in false_text:
                try:
                    res_text += translation_key_EN_RU[symbol]
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

    @classmethod
    def PressDualAlt(cls):
        if cls.is_pressAlt and cls.TriggerChangeLang == int(time.time()):
            if cls.TriggerCopy:
                cls.SetTranslateText(pyperclip.paste(), delFlag=False)
                cls.TriggerCopy = False

            else:
                cls.SetTranslateText("".join(cls.KeyPressDown))

            cls.is_pressAlt = False
            # Отчистить массив
            cls.KeyPressDown.clear()
        else:
            cls.is_pressAlt = True
            cls.TriggerChangeLang = int(time.time())

    @classmethod
    def ThCaptureKeyBoard2(cls, key):
        try:
            if not cls.is_pressAlt:
                if key.char == '\x03':
                    cls.TriggerCopy = True
                    cls.KeyPressDown.append(key.char)

        except AttributeError:
            try:
                cls.switchKey[str(key)]()
            except KeyError:
                print(f"{key}")


if __name__ == '__main__':
    pass

"""



"""
# class LogicCapture:
#     is_FlagLiveThread: bool = True
#     ErrorListCodeKey: Set[int] = set()
#     KeyPressDown: List[int] = []
#     MainLangeKeyboard: int = 0
#
#     def __init__(self):
#         # Поток по завхату нажатий клавишь
#         threading.Thread(name="ThCaptureKeyBoard", target=LogicCapture.ThCaptureKeyBoard, daemon=True).start()
#         # Поток по захвату мыши и отчистки KeyPressDown при нажатие ПКМ
#         threading.Thread(name="ThClearKeyPressDownIfPressMouse", target=LogicCapture.ThClearKeyPressDownIfPressMouse,
#                          daemon=True).start()
#         # Поток по поулчению раскладки клавиотурты
#         threading.Thread(name="ThChengKeyBoard", target=LogicCapture.ThChangKeyBoard, daemon=True).start()
#
#     @staticmethod
#     def ThChangKeyBoard():
#         GetLang = get_lang.GetLangeKeyBoard()
#         while LogicCapture.is_FlagLiveThread:
#             newLang = GetLang.get_keyboard_language()
#             if newLang != LogicCapture.MainLangeKeyboard:
#                 LogicCapture.MainLangeKeyboard = newLang
#                 fileImage: str = ""
#                 if newLang == 1:
#                     fileImage = "data_image/ru.png"
#                 elif newLang == 2:
#                     fileImage = "data_image/en.png"
#                 ImageButtonLange = PhotoImage(file=fileImage)
#                 viwe.Windows.BUTTON["image"] = ImageButtonLange
#             time.sleep(1)
#
#     @staticmethod
#     def ChangeLangKeyBoard():
#         # Сменить раскладку клавиотур
#         keyboard.press("shift+alt")
#
#     Перевод стороки сивлов на другой язык
#     @staticmethod
#     def SibelTranslation(false_text: str) -> str:
#         res_text: str = ""
#
#         if LogicCapture.MainLangeKeyboard == 2:  # En
#             for symbol in false_text:
#                 try:
#                     res_text += translation_key_EN_RU[symbol]
#                 except KeyError:
#                     res_text += symbol
#
#         elif LogicCapture.MainLangeKeyboard == 1:  # Ru
#             res_text = false_text
#
#         return res_text
#
#     # Перевод массива с номерами клавишь в строку символов
#     @staticmethod
#     def CodeKeyTranslation(listCodeKey: List[int]) -> str:
#         res_text: str = ""
#         for item in listCodeKey:
#             try:
#                 if item >= 1000:  # Оработка ввода с Shift
#                     res_text += (codeKey[item % 1000]).upper()
#                 else:
#                     res_text += codeKey[item]
#             except KeyError:
#                 LogicCapture.ErrorListCodeKey.update(str(item))
#
#         return res_text
#
#     @staticmethod
#     def SetTranslateText(text: str, delFlag=True):
#
#         # перевод раскалки
#         NewTranslateKey: str = LogicCapture.SibelTranslation(text)
#
#         # Удалть по символьно только когдаа текст напечанно вручную а не взят из буфера когда выделен текст
#         if delFlag:
#             # Стиреть слова на неправильной раскладки
#             for _ in range(len(NewTranslateKey)):
#                 keyboard.send("backspace")
#         else:
#             keyboard.send("backspace")
#
#         # Запись
#         keyboard.write(NewTranslateKey, delay=0.05)
#
#         log.debug(NewTranslateKey)  # DEBUG
#
#         # Отчистить массив
#         LogicCapture.KeyPressDown.clear()
#
#     @classmethod
#     def ThCaptureKeyBoard(cls):
#         ShiftTrigger: int = 0
#         TriggerChangeLang: float = 0.0
#         TriggerCopy: int = 0
#
#         def pressed_keys(event: keyboard.KeyboardEvent):
#             """
#             event_type - нажати || отжатие
#             name - имя клавиши
#             scan_code - номер клавиши
#             time - время когда нажата
#             """
#
#             nonlocal ShiftTrigger, TriggerChangeLang, TriggerCopy
#
#             # Принудительно зактрыть поток
#             if not cls.is_FlagLiveThread:
#                 keyboard.unhook_all()
#                 sys.exit(-1)
#
#             # Клавиши при нажатие которые отчищают массив
#             if event.scan_code in (14, 28, 1, 83, 75, 72, 80, 77):  # Enter; Backspace; Esc; Delete; Стрелки перемещения
#                 # Отчиска массива при смене фокуса
#                 LogicCapture.KeyPressDown.clear()
#                 return None
#
#             # Обработка печататния с зажатым shift
#             if event.name == "shift" and event.event_type == 'down':  # обработать зжатия Shift -
#                 ShiftTrigger = 1000
#             elif event.name == "shift" and event.event_type == 'up':
#                 ShiftTrigger = 0
#
#             # Обработка копирования текста
#             if event.name == "ctrl":
#                 if event.event_type == "down":
#                     TriggerCopy = 1
#                 else:
#                     return None
#             if event.scan_code == 46:  # "c"
#                 if TriggerCopy == 1 and event.event_type == "up":
#                     TriggerCopy = 2
#                     return None
#
#             # Обработка тригера комбинации перевода текста с задержко по времни нажатия в 1 секунуд
#             if event.name == 'alt' and event.event_type == 'up':
#                 ShiftTrigger = 0
#                 if TriggerChangeLang == int(time.time()):
#                     if TriggerCopy == 2:
#                         LogicCapture.SetTranslateText(pyperclip.paste(), delFlag=False)
#                     else:
#                         LogicCapture.SetTranslateText(LogicCapture.CodeKeyTranslation(LogicCapture.KeyPressDown),
#                                                       delFlag=True)
#                 else:
#                     TriggerChangeLang = int(time.time())
#                 return None
#
#             else:
#                 # Запись нажатых клавишь с учетом печатанью через Shift
#                 if event.event_type == "up":
#                     LogicCapture.KeyPressDown.append(event.scan_code + ShiftTrigger)
#                     TriggerCopy = 0
#
#             log.debug(LogicCapture.CodeKeyTranslation(LogicCapture.KeyPressDown))  # DEBUG
#
#         # Отчитстка буфера обмена
#         if windll.user32.OpenClipboard(None):
#             windll.user32.EmptyClipboard()
#             windll.user32.CloseClipboard()
#         keyboard.hook(pressed_keys)
#         keyboard.wait()
#
#     @classmethod
#     def ThClearKeyPressDownIfPressMouse(cls):
#         # Асинхронная функция следит за нжатием ПКМ -> олтчищает массив KeyPressDown
#         while cls.is_FlagLiveThread:
#             mouse.on_click(lambda: cls.KeyPressDown.clear())
#             time.sleep(10)
#         mouse.unhook_all()
