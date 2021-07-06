import sys
import sys
import threading
import time
from ctypes import windll
from typing import List, Set

import keyboard
import mouse
import pyperclip

from dataconst import *


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
        LogicCapture.IdentifyLangeKeyBoar()

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
        # Отчистить массив
        LogicCapture.KeyPressDown.clear()

    @classmethod
    def ThCaptureKeyBoard(cls):

        TriggerChangeLang: int = 0
        ShiftTrigger: int = 0
        CopyLast: str = ""

        def pressed_keys(event: keyboard.KeyboardEvent):
            """
            event_type - нажати || отжатие
            name - имя клавиши
            scan_code - номер клавиши
            time - время когда нажата
            """

            nonlocal TriggerChangeLang, ShiftTrigger, CopyLast

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

            # Обработка тригера комбинации перевода текста
            if event.name == 'shift' and event.event_type == 'up':
                ShiftTrigger = 0
                TriggerChangeLang += 1
                if TriggerChangeLang == 2:
                    # Перевод скопированного текста
                    tmp = pyperclip.paste()
                    if tmp != CopyLast:
                        LogicCapture.SetTranslateText(tmp)
                        CopyLast = tmp
                    else:
                        LogicCapture.SetTranslateText(LogicCapture.CodeKeyTranslation(LogicCapture.KeyPressDown))

            else:
                # Запись нажатых клавишь с учетом печатанью через Shift
                if event.event_type == "up":
                    TriggerChangeLang = 0
                    LogicCapture.KeyPressDown.append(event.scan_code + ShiftTrigger)

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


if __name__ == '__main__':
    test_class = LogicCapture()

"""
keyboard.is_pressed('ctrl') - проверка нажатия клавиатуры

keyboard.send("space") - нажать клавиши

keyboard.press("ctrl") - нажимаем кнопку CTRL

keyboard.release("ctrl") - отпускаем кнопку CTRL

keyboard.write("Программирование на Python - это всегда весело!", delay=0.1) - напечатать текст 

events = keyboard.record('esc') - записывать все нажатия на клавиатуру, пока не будет нажата клавиша esc

keyboard.play(events) - проиграйте эти события

list(keyboard.get_typed_strings(events)) - вывести нажатия

keyboard.unhook_all() - выключить слушатель

mouse.get_position() - получить полодение мыши

mouse.move(100, 100, absolute=False, duration=0.2) - перетащить мышь

mouse.on_click(lambda: print("Left Button clicked.")) - следить за нажатием выши и выполнять функцию

mouse.wheel(-1) - прокрутка колесом мыши

mouse.unhook_all() - выключить слушатель
"""
