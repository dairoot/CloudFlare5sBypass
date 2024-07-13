import os
import time


def start_xvfb_display():
    from pyvirtualdisplay import Display

    xvfb_display = Display(
        backend="xvfb",
        visible=True,
        size=(1920, 1080),
        use_xauth=True,
    )
    xvfb_display.start()
    # time.sleep(5)
    print(f"DISPLAY={os.getenv('DISPLAY')}")
