# Das Projekt ist zwar nicht direkt damit verbunden, aber als Beispiel wird ein Programm erstellt, das Bilder aus Videos extrahiert.
import time
from PIL import ImageGrab
# PIL : Python Image Library -> Pillow mit dem Befehl "pip install Pillow" im Ternimal installieren 

# Programm ausführen - 5 Sekunden warten - Alle 2 Sekunden insgesamt 10 Screenshots machen - Dateien speichern

time.sleep(5) # 5 Sekunden warten : Zeit für den Benutzer, sich vorzubereiten
for i in range(1, 11): # Alle 2 Sekunden 10 Bildern speichern
    img = ImageGrab.grab() # Aktuelles Bildschirmbild erfassen
    img.save("image{}.png".format(i)) # Bild als Datei speichern (image1.png ~ image10.png)
    time.sleep(2) # 2 Sekunden warten