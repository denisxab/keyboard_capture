import ctypes

from .dataconst import languages


class GetLangeKeyBoard:
    def __init__(self):
        self.user32 = ctypes.WinDLL('user32', use_last_error=True)

    def get_keyboard_language(self) -> int:
        # Get the current active window handle
        handle = self.user32.GetForegroundWindow()

        # Get the thread id from that window handle
        threadid = self.user32.GetWindowThreadProcessId(handle, 0)

        # Get the keyboard layout id from the threadid
        layout_id = self.user32.GetKeyboardLayout(threadid)

        # Extract the keyboard language id from the keyboard layout id
        language_id = layout_id & (2 ** 16 - 1)

        # Convert the keyboard language id from decimal to hexadecimal
        language_id_hex = hex(language_id)

        """
        1 - Ru
        2 - En
        """

        # Check if the hex value is in the dictionary.
        if language_id_hex in languages.keys():
            tmp = languages[language_id_hex]
            if type(tmp) == int:
                return tmp
            else:
                print("TypeError")
                # raise TypeError()
        else:
            print("TypeError")
            # raise TypeError()
