Bild to exe
1) Install the mingw
    https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/installer/mingw-w64-install.exe/download?use_mirror=netix&download=&failedmirror=deac-riga.dl.sourceforge.net
2) Add glogal path
    C:\Program Files\mingw-w64
    https://i.imgur.com/I4YnBfv.png
3) Install Nuitka
    pip install Nuitka
4) Build to exe
    python  -m  nuitka --follow-imports --mingw64 ../main.pyw