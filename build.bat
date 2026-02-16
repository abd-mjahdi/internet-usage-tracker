@echo off
REM Install PyInstaller if needed: pip install pyinstaller
pyinstaller --onedir --windowed --name "InternetUsageTracker" --clean ^
  --hidden-import "scapy.layers.l2" ^
  --hidden-import "scapy.layers.inet" ^
  main.py
echo.
echo Done. Run: dist\InternetUsageTracker\InternetUsageTracker.exe
echo (Tray icon appears automatically - no console window)
