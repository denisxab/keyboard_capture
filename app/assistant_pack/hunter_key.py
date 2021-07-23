from ctypes import windll
from typing import Union, Dict, Any

from pynput import keyboard, mouse


class KeyboardHunter:

    @staticmethod
    def on_press(key):
        try:
            print(f"Клавиша {key.char} - {key}")
        except AttributeError:
            print(f"Спец клавиша {key}")

    @staticmethod
    def on_release(key):
        print(f"Клавиша {key}")
        if key == keyboard.Key.esc:
            return False

    def Click(self, key: Union[str, keyboard.Key]):
        """
        :param key: Нажать и отпустить клавишу
        """
        self.KeyBoard.press(key)
        self.KeyBoard.release(key)

    def KeyPress(self, key: Union[str, keyboard.Key]):
        """
        :param key: Нажать на клавишу
        """
        self.KeyBoard.press(key)

    def KeyRelease(self, key: Union[str, keyboard.Key]):
        """
        :param key: Отпустить клавишу
        """
        self.KeyBoard.release(key)

    def TypeTextByKeyBoard(self, textPrint: str):
        """
        Напечатаь текст на клавиотуре
        """
        self.KeyBoard.type(textPrint)

    @staticmethod
    def ListenKeyboard(fun_on_press, fun_on_release):
        """
        Запускает в одельном потоки прослушивание клавиотуры
        :param fun_on_press: Функция вызываемая по нажатию клавишы
        :param fun_on_release:Функция вызываемая по отпускание клавишы
        """

        with keyboard.Listener(on_press=fun_on_press, on_release=fun_on_release) as listener:
            listener.join()

        listener = keyboard.Listener(on_press=fun_on_press, on_release=fun_on_release)
        listener.start()

    @staticmethod
    def HunterHotKey(DictHotKey: Dict[str, Any]):
        """
        :param DictHotKey: { HotKey : FunctionIfPress, }
        """
        # DictHotKey ~= {"<ctrl>+h": on_activate_h}
        with keyboard.GlobalHotKeys(DictHotKey) as listener:
            listener.join()

        """
        # Захват камбинации клавишь
        def on_activate_h():
            print(f"Locate HotKey")


        if __name__ == '__main__':
            with keyboard.GlobalHotKeys({"<ctrl>+h": on_activate_h})as h:
                h.join()
        """

        """
        # Захват камбинации клавишь
        def on_activate():
            print(f"Locate HotKey")


        def for_canonical(f):
            return lambda k: f(l.canonical(k))


        if __name__ == '__main__':
            hotkey = keyboard.HotKey(keyboard.HotKey.parse("<ctrl>+h"), on_activate)
            with keyboard.Listener(
                    on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release)) as l:
                l.join()
        """

    def __init__(self):
        self.KeyBoard = keyboard.Controller()


class MouseHunter:

    @staticmethod
    def _on_move(x: int, y: int):
        print(f"Pos: {x}, {y}")

    @staticmethod
    def _on_click(x: int, y: int, button, pressed):
        pressed_status = "Press" if pressed else "Release"
        print(f"Pos cursor: {x},{y}  | Status: {pressed_status} | Button: {button}")

    def ClickMouse(self, key: mouse.Button, countPress: int):
        """
        :param key:
        mouse.Button.left - ЛКМ
        mouse.Button.right - ПКМ
        mouse.Button.middle - ЦКМ
        :param countPress: Колличесвто нажатий
        """

        self.Mouse.click(key, countPress)

    def SetPosMouse(self, x: int, y: int):
        """
        Устоновить позицию мыши
        :param x: Позияиция по вертикали
        :param y: Позияиция по горизантали
        """
        self.Mouse.position = (x, y)

    def MovePosMouse(self, x: int, y: int):
        """
        Добавить к текцжей позиции координаты
        :param x: Позияиция по вертикали
        :param y: Позияиция по горизантали
        """
        self.Mouse.move(x, y)

    def getPosMouse(self) -> tuple:
        """
        :return: (<Позияиция по вертикали><Позияиция по горизантали>)
        """
        return self.Mouse.position

    @staticmethod
    def ListenMouse(on_move, on_click):
        """
        Запускает в одельном потоки прослушивание маши
        """
        with mouse.Listener(on_move, on_click) as listener:
            listener.join()

        listener = mouse.Listener(on_move, on_click)
        listener.start()

    def __init__(self) -> None:
        self.Mouse = mouse.Controller()


class GetLangKeyBoard:
    """
    Получить язык раскладки клавиотуры
    """

    user32 = windll.LoadLibrary("user32.dll")

    languages = {68748313: "ru", 67699721: "en"}

    @classmethod
    def get(cls) -> str:
        cls.user32.GetForegroundWindow()
        handle = cls.user32.GetForegroundWindow()
        thread_id = cls.user32.GetWindowThreadProcessId(handle, 0)
        layout_id = cls.user32.GetKeyboardLayout(thread_id)
        return cls.languages.get(layout_id, None)


translation_key = {
    "q": "й",
    "w": "ц",
    "e": "у",
    "r": "к",
    "t": "е",
    "y": "н",
    "u": "г",
    "i": "ш",
    "o": "щ",
    "p": "з",
    "[": "х",
    "]": "ъ",
    "a": "ф",
    "s": "ы",
    "d": "в",
    "f": "а",
    "g": "п",
    "h": "р",
    "j": "о",
    "k": "л",
    "l": "д",
    ";": "ж",
    "'": "э",
    "z": "я",
    "x": "ч",
    "c": "с",
    "v": "м",
    "b": "и",
    "n": "т",
    "m": "ь",
    ",": "б",
    ".": "ю",
    ########
    "Q": "Й",
    "W": "Ц",
    "E": "У",
    "R": "К",
    "T": "Е",
    "Y": "Н",
    "U": "Г",
    "I": "Ш",
    "O": "Щ",
    "P": "З",
    "{": "Х",
    "}": "Ъ",
    "A": "Ф",
    "S": "Ы",
    "D": "В",
    "F": "А",
    "G": "П",
    "H": "Р",
    "J": "О",
    "K": "Л",
    "L": "Д",
    ":": "Ж",
    '"': "Э",
    "Z": "Я",
    "X": "Ч",
    "C": "С",
    "V": "М",
    "B": "И",
    "N": "Т",
    "M": "Ь",
    "<": "Б",
    ">": "Ю",
    ########
    "й": "q",
    "ц": "w",
    "у": "e",
    "к": "r",
    "е": "t",
    "н": "y",
    "г": "u",
    "ш": "i",
    "щ": "o",
    "з": "p",
    "х": "[",
    "ъ": "]",
    "ф": "a",
    "ы": "s",
    "в": "d",
    "а": "f",
    "п": "g",
    "р": "h",
    "о": "j",
    "л": "k",
    "д": "l",
    "ж": ";",
    "э": "'",
    "я": "z",
    "ч": "x",
    "с": "c",
    "м": "v",
    "и": "b",
    "т": "n",
    "ь": "m",
    "б": ",",
    "ю": ".",
    ###:###
    "Й": "Q",
    "Ц": "W",
    "У": "E",
    "К": "R",
    "Е": "T",
    "Н": "Y",
    "Г": "U",
    "Ш": "I",
    "Щ": "O",
    "З": "P",
    "Х": "{",
    "Ъ": "}",
    "Ф": "A",
    "Ы": "S",
    "В": "D",
    "А": "F",
    "П": "G",
    "Р": "H",
    "О": "J",
    "Л": "K",
    "Д": "L",
    "Ж": ":",
    "Э": '"',
    "Я": "Z",
    "Ч": "X",
    "С": "C",
    "М": "V",
    "И": "B",
    "Т": "N",
    "Ь": "M",
    "Б": "<",
    "Ю": ">",
    ###:###
    "#": "#",
    "/": "/"
}

codeKey = {
    16: 'q',
    17: 'w',
    18: 'e',
    19: 'r',
    20: 't',
    21: 'y',
    22: 'u',
    23: 'i',
    24: 'o',
    25: 'p',
    26: '[',
    27: ']',
    30: 'a',
    31: 's',
    32: 'd',
    33: 'f',
    34: 'g',
    35: 'h',
    36: 'j',
    37: 'k',
    38: 'l',
    39: ';',
    40: "'",
    44: 'z',
    45: 'x',
    46: 'c',
    47: 'v',
    48: 'b',
    49: 'n',
    50: 'm',
    51: ',',
    52: '.',
    57: ' ',
    15: '\t',
    4: '#',
}

if __name__ == '__main__':
    pass

"""

"""
