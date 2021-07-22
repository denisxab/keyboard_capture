from typing import Union, Dict, Any, List

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


def on_activate_h(*arg):
    print("123")


if __name__ == '__main__':
    pass

"""
asd             wq                          
        classmethod                             
"""
