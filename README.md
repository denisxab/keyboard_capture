








## Meaning projects
The meaning of the program is to work conveniently with the keyboard layout


## Dependent Library
```cmd
pynput~=1.7.3
pyperclip~=1.8.2
keyboard~=0.13.5
```


## Build to exe

1. Install the mingw
    [Download](https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/installer/mingw-w64-install.exe/download?use_mirror=netix&download=&failedmirror=deac-riga.dl.sourceforge.net)
2. Add global path
    >C:\Program Files\mingw-w64
    ![Example](https://i.imgur.com/I4YnBfv.png)   
    
3. Install Nuitka
    ```cmd
   pip install Nuitka
   ```
4. Build to exe
    ```cmd
    python  -m  nuitka --follow-imports --mingw64 ../main.pyw
   ```
   
   
 
## Examples

1.
    >![П1](https://i.imgur.com/gZNsziH.gif)
    >
    >![П2](https://i.imgur.com/4ngSiFV.gif)
2.
    - Написать "Ghdbtn vbh" нажать Alt_l + Alt_l 
    ```cmd
    >>> Привет мир
    ```
3.
    - Выделить текст "Ghdbtn vbh"
    - нажать Ctr+C 
    - нажать Alt_l + Alt_l 
    ```cmd
    >>> Привет мир
    ```
4.
    - Написать "Ghdbtn vbh" 
    - Нажать ПКМ
    - нажать Alt_l + Alt_l 
    ```cmd
    >>> <Него не должно измениться>
    ```






