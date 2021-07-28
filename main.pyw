import sys

from app.viwe import Windows
from app.assistant_pack import log_debug

# except ModuleNotFoundError:
#     print("Error ModuleNotFoundError: Do you want to install them now ?")
#     if input("[Y,N]\t") in ["Y", "y"]:
#         system("pip install -r requirements.txt")
#         from app.viwe import Windows
#         from app.assistant_pack import log_debug
#     else:
#         sys.exit()

if __name__ == '__main__':
    for param in sys.argv:
        if param == "--debug":
            print("- DEBUG -")
            log_debug.DEBUG_PRINT = 1

    Windows()
