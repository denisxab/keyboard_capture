DEBUG_PRINT: int = 0


def printDebug(*values: object, sep=' ', end='\n', file=None):
    global DEBUG_PRINT
    if DEBUG_PRINT:
        print(*values, sep=sep, end=end)
