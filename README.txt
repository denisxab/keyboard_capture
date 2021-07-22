Bild o EXE 
1) Установка mingw
https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/installer/mingw-w64-install.exe/download?use_mirror=netix&download=&failedmirror=deac-riga.dl.sourceforge.net
2) Добавить в переменные окружения
C:\Program Files\mingw-w64
https://i.imgur.com/I4YnBfv.png
3) pip install Nuitka
4) python  -m nuitka --mingw64 C:\Users\denis\PycharmProjects\keyboard_capture\main.pyw
5) Нажимать yes и ждать установки доп модулей 