pyside2-rcc -o images.py images.qrc
pyinstaller -F -w main.py --name="Param Vis"
ie4uinit -show