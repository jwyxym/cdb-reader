cd ..
pyinstaller --onefile --icon=.\public\favicon.ico start_server.py
move dist\start_server.exe .\