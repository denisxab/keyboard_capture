from typing import Set, Dict

DEBUG_PRINT: int = 0
DEBUG_MAIN: Set[str] = {}
NAME_PRINT_DEBUG: Dict[str, int] = {}


def printDebug(*values: object, key: str = "", sep=' ', end='\n'):
    global DEBUG_PRINT, DEBUG_MAIN, NAME_PRINT_DEBUG

    if DEBUG_PRINT:  # If permitted
        print(*values, sep=sep, end=end)

        # k = key.split(";")
        # for key in k:
        #     key = key.strip()
        #     if NAME_PRINT_DEBUG.get(key, False):
        #         NAME_PRINT_DEBUG[key] += 1
        #     else:
        #         NAME_PRINT_DEBUG[key] = 1
        #
        # if not DEBUG_MAIN:  # Print all
        #     print(*values, sep=sep, end=end)
        #
        # else:
        #     if key in NAME_PRINT_DEBUG:
        #         print(f"[{key}]", end="\t")
        #         print({*values}, sep=sep, end=end)

# from loguru import logger
#
#
# def expensive_function(a):
#     a = [1, 23, 4, 5, 1, 25, 512]
#
#
# if __name__ == '__main__':
#     logger.add(
#         "dd/deb.log",  # Имя файла
#         format="{time} {level} {message}",  # Формат записи
#         level="DEBUG",  # Для каких уровней
#         rotation="10 KB",  # Условия указывающее , когда вошедшего файл должен быть закрыт , и новый начался.
#         compression="zip",  # компрессию формат сжатия файла при компрессии
#         mode="w"
#     )
#
#     for i in range(10):
#         logger.debug(f"{i} we go!")
#
#         time.sleep(0.4)
#
#         os.system('cls' if os.name == 'nt' else 'clear')
#
#     logger.debug(f" we go!")
