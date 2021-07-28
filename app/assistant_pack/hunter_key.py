from ctypes import windll
from typing import Dict

from pynput import mouse


# class KeyboardHunter:
#
#     # print("{")
#     # for i in sorted(keyCode):
#     #     print(f"{i}: '{keyCode[i]}'", end=",\n")
#     # print("}")
#
#     @staticmethod
#     def on_press(key):
#         try:
#             print(f"Клавиша {key.char} - {key}")
#         except AttributeError:
#             print(f"Спец клавиша {key}")
#
#     @staticmethod
#     def on_release(key):
#         print(f"Клавиша {key}")
#         if key == keyboard.Key.esc:
#             return False
#
#     def Click(self, key: Union[str, keyboard.Key], count: int = 1):
#         """
#         :param count: Сколько раз нажать
#         :param key: Нажать и отпустить клавишу
#         """
#         for _ in range(count):
#             self.KeyBoard.tap(key)
#
#     def KeyPress(self, key: Union[str, keyboard.Key]):
#         """
#         :param key: Нажать на клавишу
#         """
#         self.KeyBoard.press(key)
#
#     def KeyRelease(self, key: Union[str, keyboard.Key]):
#         """
#         :param key: Отпустить клавишу
#         """
#         self.KeyBoard.release(key)
#
#     def TypeTextByKeyBoard(self, textPrint: str):
#         """
#         Напечатать текст на клавиатуре
#         """
#         self.KeyBoard.type(textPrint)
#
#     @staticmethod
#     def ListenKeyboard(fun_on_press, fun_on_release):
#         """
#         Запускает в одельном потоки прослушивание клавиотуры
#         :param fun_on_press: Функция вызываемая по нажатию клавишы
#         :param fun_on_release:Функция вызываемая по отпускание клавишы
#         """
#
#         with keyboard.Listener(on_press=fun_on_press, on_release=fun_on_release) as listener:
#             listener.join()
#
#         listener = keyboard.Listener(on_press=fun_on_press, on_release=fun_on_release)
#         listener.start()
#
#     @staticmethod
#     def HunterHotKey(DictHotKey: Dict[str, Any]):
#         """
#         :param DictHotKey: { HotKey : FunctionIfPress, }
#         """
#         # DictHotKey ~= {"<ctrl>+h": on_activate_h}
#         with keyboard.GlobalHotKeys(DictHotKey) as listener:
#             listener.join()
#
#         """
#         # Захват камбинации клавишь
#         def on_activate_h():
#             print(f"Locate HotKey")
#
#
#         if __name__ == '__main__':
#             with keyboard.GlobalHotKeys({"<ctrl>+h": on_activate_h})as h:
#                 h.join()
#         """
#
#         """
#         # Захват камбинации клавишь
#         def on_activate():
#             print(f"Locate HotKey")
#
#
#         def for_canonical(f):
#             return lambda k: f(l.canonical(k))
#
#
#         if __name__ == '__main__':
#             hotkey = keyboard.HotKey(keyboard.HotKey.parse("<ctrl>+h"), on_activate)
#             with keyboard.Listener(
#                     on_press=for_canonical(hotkey.press), on_release=for_canonical(hotkey.release)) as l:
#                 l.join()
#         """
#
#     def __init__(self):
#         self.KeyBoard = keyboard.Controller()


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


keyCode: Dict[int, str] = {
    0: " ",
    48: '0',
    49: '1',
    50: '2',
    51: '3',
    52: '4',
    53: '5',
    54: '6',
    55: '7',
    56: '8',
    57: '9',
    65: 'a',
    66: 'b',
    67: 'c',
    68: 'd',
    69: 'e',
    70: 'f',
    71: 'g',
    72: 'h',
    73: 'i',
    74: 'j',
    75: 'k',
    76: 'l',
    77: 'm',
    78: 'n',
    79: 'o',
    80: 'p',
    81: 'q',
    82: 'r',
    83: 's',
    84: 't',
    85: 'u',
    86: 'v',
    87: 'w',
    88: 'x',
    89: 'y',
    90: 'z',
    186: ';',
    187: '=',
    188: ',',
    189: '-',
    190: '.',
    191: '/',
    192: '`',
    219: '[',
    220: '\\',
    221: ']',
    222: "'",
}

if __name__ == '__main__':
    pass
