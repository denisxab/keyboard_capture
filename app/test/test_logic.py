import unittest

from app.logic import LogicCapture
from app.assistant_pack import log_debug

log_debug.DEBUG_PRINT = 1


class Event:
    def __init__(self, scan_code: int, event_type: int):
        self.scan_code = scan_code

        self.event_type = "down" if event_type == 1 else "up"


# ArrKeySpecialKeys = {29: "crt_l",
#                      42: "shift",
#                      56: "alt",
#                      14: "backspace",
#                      83: "del",
#                      75: "<",
#                      77: ">",
#                      72: "^",
#                      80: "^",
#                      28: "enter",
#                      1: "esc",
#                      61: "f3",
#                      }


class MyTestCase(unittest.TestCase):
    """
    cls.KeyLettersAlphabet = Массив с нажатыми клавишами из алфавита
    cls.HotKey = Массив с нажатыми горячими клавишами
    cls.MainLangKeyboard = Язык клавиатуры
    cls.SpecialSelectKey = Зажатая спец клавиша
    cls.CopyBuffer = копированные текст
    """

    def resetData(self):
        LogicCapture.KeyLettersAlphabet = []
        LogicCapture.HotKey = []
        LogicCapture.MainLangKeyboard = "en"
        LogicCapture.SpecialSelectKey = [False, -1]
        LogicCapture.CopyBuffer = ""

    def setUp(self):
        self.resetData()

    def test_HotKey_Ctr_C(self):
        # Ctr + C
        dataTest = [
            Event(29, 1),
            Event(29, 1),

            Event(46, 1),
            Event(46, 0),

            Event(29, 1),
            Event(29, 1),

            Event(29, 0),
        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [])
        self.assertEqual(LogicCapture.HotKey, [29, 46])
        self.assertEqual(LogicCapture.MainLangKeyboard, "en")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])

    def test_Ctr_C_And_Press_Key_Alphabet(self):

        dataTest = [

            # Ctr + C
            Event(29, 1),
            Event(29, 1),

            Event(46, 1),
            Event(46, 0),

            Event(29, 1),
            Event(29, 1),

            Event(29, 0),

            # Press Key Alphabet

            Event(34, 1),
            Event(34, 0),

            Event(35, 1),
            Event(35, 0),

            Event(32, 1),
            Event(32, 0),

            Event(20, 1),
            Event(20, 0),

            Event(49, 1),
            Event(49, 0),

        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [34, 35, 32, 20, 49])
        self.assertEqual(LogicCapture.HotKey, [29, 46])
        self.assertEqual(LogicCapture.MainLangKeyboard, "en")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])


if __name__ == '__main__':
    unittest.main()
