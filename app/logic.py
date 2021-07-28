import sys
import threading
import time
from typing import List, Dict

from pyperclip import paste
from pynput import keyboard

from app.assistant_pack import log_debug as lg, hunter_key
from app.assistant_pack.hunter_key import translation_key_En_Ru, translation_key_Ru_En, MouseHunter, KeyboardHunter, \
    keyCode

from tkinter import PhotoImage
from app.general_data import fileImage




class LogicCapture:
    KeyPressDown: List[int] = []
    MainLangKeyboard: str = hunter_key.GetLangKeyBoard.get()
    SkipTrigger: int = 0
    TriggerConvectionLang: int = 0
    TriggerChangeLang: int = 0
    is_pressAlt: bool = False
    TriggerCopy: bool = False

    is_FlagLiveThread: bool = True
    switchKey = {
        # Отчистка массива при смене фокуса
        "Key.enter": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.backspace": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.delete": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.up": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.down": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.left": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.right": lambda: LogicCapture.KeyPressDown.clear(),
        "Key.shift": lambda: LogicCapture._ChangeLang(),
        # При вызове перевода
        "Key.alt_l": lambda: LogicCapture._PressDualAlt(),
        # добавить пробелы
        "Key.space": lambda: LogicCapture.KeyPressDown.append(0),
        "Key.ctrl_r": lambda: lg.printDebug(f"[HASH]\t{LogicCapture._ConversionListCodeKeyToSir()}"),
        "Key.ctrl_l": lambda: LogicCapture._CopyTrigger()
    }

    KeyboardOdj = KeyboardHunter()
    MouseObj = MouseHunter()

    def __init__(self, ):

        # Поток по захвату нажатий клавиш
        threading.Thread(name="ThCaptureKeyBoard",
                         target=KeyboardHunter.ListenKeyboard,
                         args=(lambda *args: 0, self.ThCaptorFeKeyBoard),
                         daemon=True).start()

        # Поток по захвату мыши и отчистки KeyPressDown при нажатии ПКМ
        threading.Thread(name="ThCaptureMouse",
                         target=MouseHunter.ListenMouse,
                         args=(lambda *args: 0, self.PressMouse),
                         daemon=True).start()

    @classmethod
    def _SibelTranslation(cls, false_text: str) -> List[str]:
        # Перевод строки символов на другой язык
        res_text: List[str] = []

        lg.printDebug(f"67: Lang: {LogicCapture.MainLangKeyboard}")

        for symbol in false_text:
            if cls.MainLangKeyboard == "ru":
                try:
                    res_text.append(translation_key_Ru_En[symbol])
                except KeyError:
                    res_text += symbol

            elif cls.MainLangKeyboard == "en":
                try:
                    res_text.append(translation_key_En_Ru[symbol])
                except KeyError:
                    res_text.append(symbol)

        return res_text

    @classmethod
    def _SetTranslateText(cls, text: str, delFlag=True):

        lg.printDebug(f"87 {text}")
        # перевод раскладки
        NewTranslateKey: List[str] = LogicCapture._SibelTranslation(text)
        ln = len(NewTranslateKey)
        lg.printDebug(f"[ RES]\t{''.join(NewTranslateKey)}")

        if not delFlag:
            cls.KeyboardOdj.KeyBoard.tap(keyboard.Key.right)
            cls.SkipTrigger = (ln * 4) + 1
        else:
            cls.SkipTrigger = ln * 4
        lg.printDebug(f"98: {NewTranslateKey}")

        # Стереть слова на неправильной раскладки
        for _ in range(ln):
            cls.KeyboardOdj.KeyBoard.tap(keyboard.Key.backspace)
            cls.KeyboardOdj.KeyBoard.tap(NewTranslateKey.pop())
            cls.KeyboardOdj.KeyBoard.tap(keyboard.Key.left)
        for _ in range(ln):
            cls.KeyboardOdj.KeyBoard.tap(keyboard.Key.right)

        cls.KeyPressDown.clear()

    @classmethod
    def _PressDualAlt(cls):
        if cls.is_pressAlt and cls.TriggerConvectionLang == int(time.time()):
            if cls.TriggerCopy:
                cls._SetTranslateText(paste(), delFlag=False)
                cls.TriggerCopy = False
                lg.printDebug(f"120: Copy")

            else:
                lg.printDebug(f"123 {cls._ConversionListCodeKeyToSir()}")
                cls._SetTranslateText(cls._ConversionListCodeKeyToSir())

            cls.is_pressAlt = False

        else:
            cls.is_pressAlt = True
            cls.TriggerConvectionLang = int(time.time())

    @classmethod
    def _ChangeLang(cls):
        cls.TriggerChangeLang = True

    @classmethod
    def _CopyTrigger(cls):
        cls.TriggerCopy = True

    @classmethod
    def PressMouse(cls, *args):
        if cls.is_FlagLiveThread:
            LogicCapture.KeyPressDown.clear()
        else:
            sys.exit(0)

    @classmethod
    def _ConversionListCodeKeyToSir(cls) -> str:
        if cls.KeyPressDown:
            try:
                return "".join(
                    [keyCode[key * -1].upper() if key < 0 else keyCode[key] for key in
                     cls.KeyPressDown])
            except Exception as  e:
                print(f"{e} == {cls.KeyPressDown}")
        else:
            return ""

    @classmethod
    def ThCaptorFeKeyBoard(cls, key):

        if cls.SkipTrigger == 0:

            if hasattr(key, 'char'):
                lg.printDebug(f"164: {cls.KeyPressDown}", key="Обработка нажатий")

                if cls.TriggerCopy and key.vk == 67:
                    lg.printDebug(f"[COPY]\t{paste()}", key="Обработка нажатий")

                try:
                    if key.vk:
                        if key.char.istitle():
                            cls.KeyPressDown.append(key.vk * -1)

                        else:
                            cls.KeyPressDown.append(key.vk)

                except (AttributeError, TypeError) as e:
                    lg.printDebug(f"179: {e}", key="Обработка нажатий; Ошибки")

            else:
                try:
                    # Слежка за сменой раскладки клавиатуры
                    if cls.TriggerChangeLang and str(key) == "Key.alt_l":
                        cls.MainLangKeyboard = 'en' if cls.MainLangKeyboard == 'ru' else 'ru'
                        lg.printDebug(f"185: {cls.MainLangKeyboard} = {fileImage[LogicCapture.MainLangKeyboard]}",
                                      key="Обработка нажатий; Смена языка")
                    else:
                        cls.TriggerChangeLang = False

                    if str(key) != "Key.alt_l":
                        cls.TriggerCopy = False

                    cls.switchKey[str(key)]()
                    lg.printDebug(f"190: {key}", key="Обработка нажатий")
                except KeyError as e:
                    lg.printDebug(f"193: {e}", key="Обработка нажатий; Ошибки")

        else:
            cls.SkipTrigger -= 1


if __name__ == '__main__':
    pass
