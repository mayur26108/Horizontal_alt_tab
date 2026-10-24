import time
import threading
from pynput import mouse, keyboard

kbd = keyboard.Controller()
alt_held = False
last_scroll = 0

def monitor_timeout():
    global alt_held
    while True:
        time.sleep(0.1)
        # Safety release: drops the Alt key if no scroll occurs for 1.5 seconds
        if alt_held and (time.time() - last_scroll > 1.5):
            kbd.release(keyboard.Key.alt)
            alt_held = False

def on_scroll(x, y, dx, dy):
    global alt_held, last_scroll
    
    # dx handles the horizontal scroll axis
    if dx != 0:
        last_scroll = time.time()
        if not alt_held:
            kbd.press(keyboard.Key.alt)
            alt_held = True
        
        if dx > 0:  # Scrolled Right (Forward)
            kbd.press(keyboard.Key.tab)
            kbd.release(keyboard.Key.tab)
        elif dx < 0:  # Scrolled Left (Backward)
            kbd.press(keyboard.Key.shift)
            kbd.press(keyboard.Key.tab)
            kbd.release(keyboard.Key.tab)
            kbd.release(keyboard.Key.shift)

def on_click(x, y, button, pressed):
    global alt_held
    # Instantly release Alt if you left-click to select a window
    if pressed and alt_held:
        kbd.release(keyboard.Key.alt)
        alt_held = False

# Run the safety timeout in the background
threading.Thread(target=monitor_timeout, daemon=True).start()

# Start listening for mouse inputs
with mouse.Listener(on_scroll=on_scroll, on_click=on_click) as listener:
    listener.join()