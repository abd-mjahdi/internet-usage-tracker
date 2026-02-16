"""
System tray UI for the internet usage tracker.
Run with: python main.py --tray
"""
import threading
import time
import pystray
from PIL import Image, ImageDraw

import main


def make_icon_image():
    """Draw a simple tray icon (network/speed style)."""
    size = 64
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Circle with a downward arrow (download)
    d.ellipse([8, 8, size - 8, size - 8], outline=(70, 130, 180), width=3)
    # Arrow down
    d.polygon([(32, 28), (24, 44), (40, 44)], fill=(70, 130, 180))
    return img


def format_speed(speed):
    """Bytes/s to short string."""
    if speed < 1024:
        return f"{speed:.0f} B/s"
    if speed < 1024 * 1024:
        return f"{speed / 1024:.1f} KB/s"
    return f"{speed / (1024 * 1024):.1f} MB/s"


_tracker_thread = None


def on_start(icon, item):
    global _tracker_thread
    if main.tracking_active:
        return
    _tracker_thread = threading.Thread(target=lambda: main.run_tracker(console=False), daemon=True)
    _tracker_thread.start()
    icon.notify("Tracking started", "Internet usage tracker")


def on_stop(icon, item):
    main.stop_tracker()
    icon.notify("Tracking stopped", "Internet usage tracker")


def on_exit(icon, item):
    main.stop_tracker()
    icon.stop()


def run_tray():
    icon_image = make_icon_image()
    menu = pystray.Menu(
        pystray.MenuItem("Start tracking", on_start, default=True),
        pystray.MenuItem("Stop tracking", on_stop),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Exit", on_exit),
    )
    icon = pystray.Icon("usage_tracker", icon_image, "Usage tracker", menu)

    # Update tooltip every 2 seconds in a daemon thread
    def tooltip_loop():
        while True:
            time.sleep(2)
            if not icon.visible:
                break
            try:
                if main.tracking_active:
                    rows = main.get_current_stats()[:5]
                    if rows:
                        lines = [f"{name}: {format_speed(speed)}" for name, speed in rows]
                        icon.title = "Usage\n" + "\n".join(lines)
                    else:
                        icon.title = "Usage tracker (running)"
                else:
                    icon.title = "Usage tracker (stopped)"
            except Exception:
                pass

    t = threading.Thread(target=tooltip_loop, daemon=True)
    t.start()

    icon.run()


if __name__ == "__main__":
    run_tray()
