# Projekt) Entwicklung eines Arcade-Pang-Spiels
# [Bedingungen]
# 1. Der Charakter befindet sich unten auf dem Bildschirm und kann sich nur nach links und rechts bewegen.
# 2. Wenn die Leertaste gedrückte wird, schießt er eine Waffe ab.
# 3. Beim Beginn des Spiels erscheint ein großer Ball und prallt ab.
# 4. Wenn der Ball von der Waffe getroffen wird, teilt er sich in zwei kleinere Bälle. Der kleinste Ball verschwindet.
# 5. Wenn alle Bälle entfernt sind, endet das Spiel. (Erfolg).
# 6. Wenn der Charakter von einem Ball getroffen wird, endet das Spiel. (Fehlschlag)
# 7. Wenn die Zeitbegrenzung von 99 Sekunden überschritten wird, endet das Spiel. (Fehlschlag)
# 8. FPS ist auf 30 festgelegt (Geschwindigkeit kann bei Bedarf angepasst werden.)

# [Spielbilder]
# 1. Hintergrund : 640 * 480 (Breite * Höhe) - background.png
# 2. Platform : 640 * 50 - platform.png
# 3. Charakter : 33 * 60 - character.png
# 4. Waffe : 20 * 430 - weapon.png
# 5. Ball : 160 * 160, 80 * 80, 40 * 40, 20 * 20 - ball1.png ~ ball4.png

import os
import pygame
########################################################
# Grundlegende Initialisierung
# Dinge, die unbedingt gemacht werden müssen: Nur Größe oder Namen ändern, den Rest bleiben
pygame.init()

# Bildschirmgröße einstellen
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# Bildschrimtitel einstellen
pygame.display.set_caption("JK Arcade")

# FPS = Frames per Second
clock = pygame.time.Clock()
########################################################

# Benutzerspiel-Initialisierung (Hintergrundbild, Spielbilder, Koordinaten, Geschwindigkeit, Schriftart usw.)

# Pfad laden
curr_path = os.path.dirname(__file__) # Gibt den aktuellen Dateipfad zurück
image_path = os.path.join(curr_path, "images") # Gibt den Pfand des Ordners "images" zurück

# Hintergrund
bgrd = pygame.image.load(os.path.join(image_path, "background.png"))

# Platform (Bühne)
platform = pygame.image.load(os.path.join(image_path, "platform.png"))
platform_size = platform.get_rect().size # Gibt die Größe vom Platform als Tuple (Breite, Höhe) zurück 
platform_height = platform_size[1] # Höhe der Platform (platform_height wird verwendet, um den Charakter auf dem Platform zu positionieren)

# Charakter
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
# Position des Characters rechnen, um ihn genau in der Mitte des Bildschirms & des Platforms zu positionieren
character_x_position = (screen_width - character_width) / 2
character_y_position = screen_height - character_height - platform_height

running = True
while running:
    dt = clock.tick(30) # Die Bildrate wird auf 30 FPS beschränkt, um das Spiel gleichmäßig laufen zu lassen
    # Delta Time : framerate (max. 30)

    # Ereignisse verarbeiten (Tastatur, Maus usw.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # Bildschirm, Platform, Charakter zeichnen
    screen.blit(bgrd, (0,0))
    screen.blit(platform, (0, screen_height - platform_height))
    screen.blit(character, (character_x_position, character_y_position))

    pygame.display.update() # Bei jedem Frame erneut zeichnen

pygame.quit()