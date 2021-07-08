try:
    from viwe import Windows

except ModuleNotFoundError:
    from os import system

    system("pip install -r requirements.txt")
    from viwe import Windows

if __name__ == '__main__':
    Windows()
