# Wenn eine Tastatureingabe erfolgt, wird dieser Wert aufgenommen und verarbeitet = Hooking
# Anstatt in regelmäßigen Zeitabständen Screenshots zu machen,
# ein Programm erstellen, das Screenshots macht, wann immer der Benutzer es möchte (=bei Tastatureingabe)
# terminal > pip install keyboard

import time # Wenn der Name des Screenshots die aufgenommene Zeit enthält, gibt es kein Überschreibungsproblem
import keyboard
from PIL import ImageGrab

# Verwendung : keyboard.add_hotkey("Taste", Funktion)
# Taste registrieren : Wenn der Benutzer die "Taste" drückt, führt er die folgende "Funktion"(= screenshot()) aus. (Speichert den Screenshot)

def screenshot():
    current_time = time.strftime("_%Y%m%d_%H%M%S") # Ändert den aktuellen Zeitwert in das Format _YYYYmmdd_HHMMSS
    img = ImageGrab.grab()
    img.save("image{}.png".format(current_time)) # Bsp: Datei mit "image_YYYYmmdd_HHMMSS.png" gespeichert

keyboard.add_hotkey("ctrl+shift+s", screenshot) # Mit den Kombo der Tasten "ctrl+shift+s" kann der Benutzer den Screenshot speichern

keyboard.wait("esc") # Das Programm wird ausgeführt, bis der Benutzer "esc" drückt