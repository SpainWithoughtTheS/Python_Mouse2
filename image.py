import time
import sys
import pyautogui as pag
import keyboard

# ---------- Settings ----------
IMAGE_PATH = sys.argv[1] if len(sys.argv) > 1 else "target.png"
CONFIDENCE = 0.65          # was ~0.87 — lower to tolerate tiny differences
SEARCH_GRAYSCALE = False   # color helps on colorful UIs
CLICK_INTERVAL = 0.07
SEARCH_COOLDOWN = 0.10
MOVE_DURATION = 0.03
REGION = None              # e.g., (left, top, width, height) to speed up + improve reliability

HOTKEY_START = "ctrl+shift+s"
HOTKEY_STOP  = "ctrl+shift+x"


pag.FAILSAFE = True
running = False

def start():
    global running
    if running:
        return
    print("[*] Started. Press", HOTKEY_STOP, "to stop. Move mouse to a corner for failsafe.")
    running = True
    loop()

def stop():
    global running
    if running:
        running = False
        print("[*] Stopped.")

def loop():
    while running:
        try:
            loc = pag.locateCenterOnScreen(
                IMAGE_PATH,
                confidence=CONFIDENCE,
                grayscale=SEARCH_GRAYSCALE,
                region=REGION
            )
            if not running:
                break

            if loc:
                pag.moveTo(loc.x, loc.y, duration=MOVE_DURATION)
                pag.click()
                time.sleep(CLICK_INTERVAL)
            else:
                time.sleep(SEARCH_COOLDOWN)

        except pag.ImageNotFoundException:
            # PyAutoGUI/pyscreeze throws when the best score < threshold — just keep searching
            time.sleep(SEARCH_COOLDOWN)
        except pag.FailSafeException:
            print("[!] Failsafe triggered; stopping.")
            stop()
        except Exception as e:
            print(f"[!] Error (continuing): {e}")
            time.sleep(0.15)

def main():
    print(f"[-] Image: {IMAGE_PATH}")
    print(f"[-] Start: {HOTKEY_START} | Stop: {HOTKEY_STOP}")
    print("[-] Failsafe: move mouse to any screen corner.")
    keyboard.add_hotkey(HOTKEY_START, start)
    keyboard.add_hotkey(HOTKEY_STOP,  stop)
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        stop()

if __name__ == "__main__":
    main()
