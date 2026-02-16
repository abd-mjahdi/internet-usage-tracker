# Internet usage tracker

Tracks **Ethernet** download usage per process (which app uses how much).

**Requirements:** Windows, Npcap, run as Administrator.

```bash
pip install -r requirements.txt
```

- **Tray (default):** `python main.py` — system tray icon; Start/Stop tracking, tooltip shows top processes.
- **Console:** `python main.py --console` — terminal output, updates every second.

### Build exe

```powershell
pip install pyinstaller
.\build.bat
```

Output: `dist\InternetUsageTracker\InternetUsageTracker.exe`. Run as Administrator. Tray icon appears automatically (no console window).
