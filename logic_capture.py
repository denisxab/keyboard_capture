import logging
import sys
import threading
import time
from ctypes import windll
from typing import List, Set

import keyboard
import mouse
import pyperclip

from pack.dataconst import *

# logging.basicConfig(level="DEBUG", filename='log_file/logic_capture.log')


logging.basicConfig(
    # handlers=[logging.FileHandler(filename="log_file/logic_capture.log", encoding='utf-8', mode='w')],
    format="%(asctime)s %(name)s:\t%(funcName)s:\t%(thread)d:\t%(levelname)s:\t%(message)s:",
    datefmt="%F %T",
    level=logging.DEBUG)
log = logging.getLogger("logic")


class LogicCapture:
    is_FlagLiveThread: bool = True
    ErrorListCodeKey: Set[int] = set()
    KeyPressDown: List[int] = []
    MainLangeKeyboard: int = 0

    def __init__(self):
        # Поток по завхату нажатий клавишь
        threading.Thread(name="ThCaptureKeyBoard", target=LogicCapture.ThCaptureKeyBoard, daemon=True).start()
        # Поток по захвату мыши и отчистки KeyPressDown при нажатие ПКМ
        threading.Thread(name="ThClearKeyPressDownIfPressMouse", target=LogicCapture.ThClearKeyPressDownIfPressMouse,
                         daemon=True).start()

    @staticmethod
    def ChangeLangeKeyBoard():
        # Сменить раскладку клавиотур
        keyboard.press("shift+alt")

    # Перевод стороки сивлов на другой язык
    @staticmethod
    def SimblTranslation(false_text: str) -> str:
        res_text: str = ""
        for symbol in false_text:
            try:
                res_text += translation_key[symbol]
            except KeyError:
                res_text += symbol

        return res_text

    # Перевод массива с номерами клавишь в строку символов
    @staticmethod
    def CodeKeyTranslation(listCodeKey: List[int]) -> str:
        res_text: str = ""
        for item in listCodeKey:
            try:
                if item >= 1000:  # Оработка ввода с Shift
                    res_text += (codeKey[item % 1000]).upper()
                else:
                    res_text += codeKey[item]
            except KeyError:
                LogicCapture.ErrorListCodeKey.update(str(item))

        return res_text

    @staticmethod
    def SetTranslateText(text: str):
        # перевод раскалки
        NewTranslateKey: str = LogicCapture.SimblTranslation(text)
        # Стиреть слова на неправильной раскладки
        for _ in range(len(NewTranslateKey)):
            keyboard.send("backspace")
        # Запись новыйх слов
        keyboard.write(NewTranslateKey, delay=0.05)

        log.debug(NewTranslateKey)

        # Отчистить массив
        LogicCapture.KeyPressDown.clear()

    @classmethod
    def ThCaptureKeyBoard(cls):
        ShiftTrigger: int = 0
        CopyLast: str = ""
        Trigger: float = 0.0

        def pressed_keys(event: keyboard.KeyboardEvent):
            """
            event_type - нажати || отжатие
            name - имя клавиши
            scan_code - номер клавиши
            time - время когда нажата
            """

            nonlocal ShiftTrigger, CopyLast, Trigger

            # Зактрыть поток
            if not cls.is_FlagLiveThread:
                keyboard.unhook_all()
                sys.exit(-1)

            # Клавиши при нажатие которые отчищают массив
            if event.scan_code in (14, 28, 1, 83, 75, 72, 80, 77):  # Enter; Backspace; Esc; Delete; Стрелки перемещения
                # Отчиска массива при смене фокуса
                LogicCapture.KeyPressDown.clear()
                return None
            # Обработка печататния с зажатым shift
            if event.name == "shift" and event.event_type == 'down':  # обработать зжатия Shift -
                ShiftTrigger = 1000
            elif event.name == "shift" and event.event_type == 'up':
                ShiftTrigger = 0
            # Обработка тригера комбинации перевода текста с задержко по времни нажатия в 1 секунуд
            if event.name == 'alt' and event.event_type == 'up':
                ShiftTrigger = 0
                if Trigger == int(time.time()):
                    # Перевод скопированного текста
                    tmp = pyperclip.paste()
                    if tmp != CopyLast:
                        LogicCapture.SetTranslateText(tmp)
                        CopyLast = tmp
                    else:
                        LogicCapture.SetTranslateText(LogicCapture.CodeKeyTranslation(LogicCapture.KeyPressDown))
                else:
                    Trigger = int(time.time())

            else:
                # Запись нажатых клавишь с учетом печатанью через Shift
                if event.event_type == "up":
                    LogicCapture.KeyPressDown.append(event.scan_code + ShiftTrigger)

            log.debug(LogicCapture.CodeKeyTranslation(LogicCapture.KeyPressDown))

        # Отчитстка буфера обмена
        if windll.user32.OpenClipboard(None):
            windll.user32.EmptyClipboard()
            windll.user32.CloseClipboard()
        keyboard.hook(pressed_keys)
        keyboard.wait()

    @classmethod
    def ThClearKeyPressDownIfPressMouse(cls):
        # Асинхронная функция следит за нжатием ПКМ -> олтчищает массив KeyPressDown
        while cls.is_FlagLiveThread:
            mouse.on_click(lambda: cls.KeyPressDown.clear())
            time.sleep(10)
        mouse.unhook_all()

    def __del__(self):
        LogicCapture.is_FlagLiveThread = False
