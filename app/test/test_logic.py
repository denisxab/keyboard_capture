import unittest
from typing import List

from app.logic import LogicCapture
import app.logic
from app.assistant_pack import log_debug

log_debug.DEBUG_PRINT = 1


class FakeClass:
    ArrPress: List[str] = []

    @classmethod
    def send(cls, text):
        cls.ArrPress.append(text)

    @classmethod
    def write(cls, text, delay=0):
        [cls.ArrPress.append(i) for i in text]

    @classmethod
    def _CopyTrigger(cls):
        LogicCapture.CopyBuffer = "Data in Buffer"


app.logic.kb = FakeClass
LogicCapture._CopyTrigger = FakeClass._CopyTrigger


class Event:
    def __init__(self, scan_code: int, event_type: int):
        self.scan_code = scan_code

        self.event_type = "down" if event_type == 1 else "up"


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
        LogicCapture.Result = []
        FakeClass.ArrPress = []

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
        self.assertEqual(LogicCapture.CopyBuffer, 'Data in Buffer')
        self.assertEqual(FakeClass.ArrPress, [])
        self.assertEqual(LogicCapture.Result, [])

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
        self.assertEqual(LogicCapture.HotKey, [])
        self.assertEqual(LogicCapture.MainLangKeyboard, "en")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(LogicCapture.CopyBuffer, 'Data in Buffer')
        self.assertEqual(FakeClass.ArrPress, [])
        self.assertEqual(LogicCapture.Result, [])

    def test_Press_Key_Alphabet_And_Down_Shift(self):

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

            Event(42, 1),  # Shift Down

            Event(32, 1),
            Event(32, 0),

            Event(20, 1),
            Event(20, 0),

            Event(42, 0),  # Shift Up

            Event(49, 1),
            Event(49, 0),

        ]

        for Dt in dataTest:
            if Dt.scan_code == 42:
                a = 0
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [34, 35, -32, -20, 49])
        self.assertEqual(LogicCapture.HotKey, [])
        self.assertEqual(LogicCapture.MainLangKeyboard, "en")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(LogicCapture.CopyBuffer, "Data in Buffer")
        self.assertEqual(FakeClass.ArrPress, [])
        self.assertEqual(LogicCapture.Result, [])

    def test_Translate_Text_EN_RU(self):

        LogicCapture.MainLangKeyboard = "en"
        dataTest = [

            # Press Key Alphabet
            Event(42, 1),  # Shift Down
            Event(34, 1),
            Event(34, 0),

            Event(35, 1),
            Event(35, 0),
            Event(42, 0),  # Shift Up

            Event(32, 1),
            Event(32, 0),

            Event(20, 1),
            Event(20, 0),

            Event(49, 1),
            Event(49, 0),

            Event(57, 1),
            Event(57, 0),

            Event(47, 1),
            Event(47, 0),

            Event(48, 1),
            Event(48, 0),

            Event(35, 1),
            Event(35, 0),

        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [-34, -35, 32, 20, 49, 57, 47, 48, 35])
        self.assertEqual(LogicCapture.HotKey, [])
        self.assertEqual(LogicCapture.MainLangKeyboard, "en")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(LogicCapture.Result, [])

        # Hot Key Tanleted
        dataTest = [

            Event(56, 1),  # Alt Down

            Event(44, 1),  # z Down
            Event(44, 0),  # z Up

            Event(56, 0),  # Alt Up

        ]
        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [-34, -35, 32, 20, 49, 57, 47, 48, 35])
        self.assertEqual(LogicCapture.Result, ['П', 'Р', 'в', 'е', 'т', ' ', 'м', 'и', 'р'])
        self.assertEqual(LogicCapture.HotKey, [56, 44])
        self.assertEqual(LogicCapture.MainLangKeyboard, "en")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(LogicCapture.CopyBuffer, '')
        self.assertEqual(FakeClass.ArrPress,
                         ['backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace',
                          'backspace', 'backspace', 'П', 'Р', 'в', 'е', 'т', ' ', 'м', 'и', 'р'])

    def test_Translate_Text_RU_EN(self):

        LogicCapture.MainLangKeyboard = "ru"
        dataTest = [

            # Press Key Alphabet
            Event(42, 1),  # Shift Down
            Event(34, 1),
            Event(34, 0),

            Event(35, 1),
            Event(35, 0),
            Event(42, 0),  # Shift Up

            Event(32, 1),
            Event(32, 0),

            Event(20, 1),
            Event(20, 0),

            Event(49, 1),
            Event(49, 0),

            Event(57, 1),
            Event(57, 0),

            Event(47, 1),
            Event(47, 0),

            Event(48, 1),
            Event(48, 0),

            Event(35, 1),
            Event(35, 0),

        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [-34, -35, 32, 20, 49, 57, 47, 48, 35])
        self.assertEqual(LogicCapture.HotKey, [])
        self.assertEqual(LogicCapture.MainLangKeyboard, "ru")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(LogicCapture.Result, [])

        # Hot Key Tanleted
        dataTest = [

            Event(56, 1),  # Alt Down

            Event(44, 1),  # z Down
            Event(44, 0),  # z Up

            Event(56, 0),  # Alt Up

        ]
        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [-34, -35, 32, 20, 49, 57, 47, 48, 35])
        self.assertEqual(LogicCapture.Result, ['G', 'H', 'd', 't', 'n', ' ', 'v', 'b', 'h'])
        self.assertEqual(LogicCapture.HotKey, [56, 44])
        self.assertEqual(LogicCapture.MainLangKeyboard, "ru")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(LogicCapture.CopyBuffer, '')
        self.assertEqual(FakeClass.ArrPress,
                         ['backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace', 'backspace',
                          'backspace', 'backspace', 'G', 'H', 'd', 't', 'n', ' ', 'v', 'b', 'h'])

    def test_Clear_KeyLettersAlphabet_If_Press_Backspace(self):
        dataTest = [

            # Press Key Alphabet
            Event(42, 1),  # Shift Down
            Event(34, 1),
            Event(34, 0),

            Event(35, 1),
            Event(35, 0),
            Event(42, 0),  # Shift Up

            Event(32, 1),
            Event(32, 0),

        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [-34, -35, 32])
        self.assertEqual(LogicCapture.HotKey, [])
        self.assertEqual(LogicCapture.MainLangKeyboard, "en")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(FakeClass.ArrPress, [])
        self.assertEqual(LogicCapture.CopyBuffer, '')
        self.assertEqual(LogicCapture.Result, [])

        dataTest = [
            Event(14, 1),  # backspace Down
            Event(14, 0),  # backspace Up
        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [])
        self.assertEqual(LogicCapture.HotKey, [14])
        self.assertEqual(LogicCapture.MainLangKeyboard, "en")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(LogicCapture.Result, [])

    def test_Many_Change_Lang(self):

        LogicCapture.MainLangKeyboard = "en"
        dataTest = [
            # Press Key Alphabet
            Event(42, 1),  # Shift Down
            Event(56, 1),  # Alt Down
            Event(56, 0),  # Alt Up

            Event(42, 0),  # Shift Up
        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [])
        self.assertEqual(LogicCapture.Result, [])
        self.assertEqual(LogicCapture.HotKey, [42, 56])
        self.assertEqual(LogicCapture.MainLangKeyboard, "ru")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(LogicCapture.CopyBuffer, '')
        self.assertEqual(FakeClass.ArrPress, [])

        dataTest = [
            # Press Key Alphabet
            Event(42, 1),  # Shift Down
            Event(56, 1),  # Alt Down
            Event(56, 0),  # Alt Up
            Event(56, 1),  # Alt Down
            Event(56, 0),  # Alt Up

            Event(42, 0),  # Shift Up
        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [])
        self.assertEqual(LogicCapture.Result, [])
        self.assertEqual(LogicCapture.HotKey, [42, 56, 56])
        self.assertEqual(LogicCapture.MainLangKeyboard, "ru")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(LogicCapture.CopyBuffer, '')
        self.assertEqual(FakeClass.ArrPress, [])

        dataTest = [
            # Press Key Alphabet
            Event(42, 1),  # Shift Down
            Event(56, 1),  # Alt Down
            Event(56, 0),  # Alt Up
            Event(56, 1),  # Alt Down
            Event(56, 0),  # Alt Up
            Event(56, 1),  # Alt Down
            Event(56, 0),  # Alt Up

            Event(42, 0),  # Shift Up
        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [])
        self.assertEqual(LogicCapture.Result, [])
        self.assertEqual(LogicCapture.HotKey, [42, 56, 56, 56])
        self.assertEqual(LogicCapture.MainLangKeyboard, "en")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(LogicCapture.CopyBuffer, '')
        self.assertEqual(FakeClass.ArrPress, [])

    def test_Ctr_C_And_Translate_Test(self):

        LogicCapture.MainLangKeyboard = "ru"
        dataTest = [

            # Press Key Alphabet
            Event(42, 1),  # Shift Down
            Event(34, 1),
            Event(34, 0),

            Event(35, 1),
            Event(35, 0),
            Event(42, 0),  # Shift Up

            Event(32, 1),
            Event(32, 0),

        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [-34, -35, 32])
        self.assertEqual(LogicCapture.HotKey, [])
        self.assertEqual(LogicCapture.MainLangKeyboard, "ru")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(FakeClass.ArrPress, [])
        self.assertEqual(LogicCapture.CopyBuffer, '')
        self.assertEqual(LogicCapture.Result, [])

        dataTest = [
            Event(14, 1),  # backspace Down
            Event(14, 0),  # backspace Up
        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [])
        self.assertEqual(LogicCapture.HotKey, [14])
        self.assertEqual(LogicCapture.MainLangKeyboard, "ru")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(FakeClass.ArrPress, [])
        self.assertEqual(LogicCapture.CopyBuffer, '')
        self.assertEqual(LogicCapture.Result, [])

        dataTest = [
            # Ctr + C
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
        self.assertEqual(LogicCapture.MainLangKeyboard, "ru")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(FakeClass.ArrPress, [])
        self.assertEqual(LogicCapture.CopyBuffer, 'Data in Buffer')
        self.assertEqual(LogicCapture.Result, [])

        # Hot Key Tanleted
        dataTest = [

            Event(56, 1),  # Alt Down

            Event(44, 1),  # z Down
            Event(44, 0),  # z Up

            Event(56, 0),  # Alt Up

        ]

        for Dt in dataTest:
            LogicCapture.pressed_keys(Dt)

        self.assertEqual(LogicCapture.KeyLettersAlphabet, [])
        self.assertEqual(LogicCapture.HotKey, [56, 44])
        self.assertEqual(LogicCapture.MainLangKeyboard, "ru")
        self.assertEqual(LogicCapture.SpecialSelectKey, [False, -1])
        self.assertEqual(FakeClass.ArrPress,
                         ['backspace', 'D', 'a', 't', 'a', ' ', 'i', 'n', ' ', 'B', 'u', 'f', 'f', 'e', 'r'])
        self.assertEqual(LogicCapture.CopyBuffer, '')
        self.assertEqual(LogicCapture.Result, ['D', 'a', 't', 'a', ' ', 'i', 'n', ' ', 'B', 'u', 'f', 'f', 'e', 'r'])


if __name__ == '__main__':
    unittest.main()
