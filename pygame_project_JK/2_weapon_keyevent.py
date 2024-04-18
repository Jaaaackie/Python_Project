import os
import pygame
########################################################
pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("JK Arcade")

clock = pygame.time.Clock()
########################################################

curr_path = os.path.dirname(__file__)
image_path = os.path.join(curr_path, "images")

bgrd = pygame.image.load(os.path.join(image_path, "background.png"))

platform = pygame.image.load(os.path.join(image_path, "platform.png"))
platform_size = platform.get_rect().size
platform_height = platform_size[1]

character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_position = (screen_width - character_width) / 2
character_y_position = screen_height - character_height - platform_height

# Bewegungsrichtung des Charakters
character_to_x = 0
# to_y brauchen wir nicht, weil der Chrakter sich nur nach links und rechts bewegen kann

# Charaktergeschwindigkeit
character_speed = 5

# Waffe
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0] # Der Charakter schießt die Waffe, also bewegt sich die Waffe auch nach links und rechts

# Mehrere Waffen können gleichzeitig abgefeurt werden
# Es gibt nicht nur eine Waffe, sondern mehrere, die über eine Liste verwaltet werden
weapons = []

# Waffengeschwindigkeit
weapon_speed = 10

running = True 
while running:
    dt = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Verarbeitung bei Tastatureingaben
        if event.type == pygame.KEYDOWN: # Taste gedrückt

            # Bewegung des Charakters steuern (x-Achse : die rechte Seite = postiv, die linkte Seite = negativ)        
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed # Charakter nach links
            
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed # Charakter nach rechts

            # Waffe abfeuern
            elif event.key == pygame.K_SPACE:
                weapon_x_position = character_x_position + (character_width - weapon_width) / 2
                weapon_y_position = character_y_position
                weapons.append([weapon_x_position, weapon_y_position]) # Neue Position der Waffe in die Liste der Waffen in die Liste der Waffen
        
        if event.type == pygame.KEYUP: # Taste losgelassen
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0 # Charakter hört auf, sich nach links oder rechts zu bewegen
    
    # aktuelle Position des Charakers definieren (Position wird aktualisiert)
    character_x_position += character_to_x
    
    # Charakter darf nicht aus dem Bildschrim laufen
    if character_x_position < 0: # versucht der Charakter, über den linken Rand des Bildschirms hinauszugehen?
        character_x_position = 0
    elif character_x_position > screen_width - character_width: # (Teil vom) Charakter über den rechten Rand hinauszugehen? 
        character_x_position = screen_width - character_width

    # Position der Waffen anpassen
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons ]
        # w = [(weapon_x_position, weapon_y_position)], die aus den x-, y-Koordinaten der Waffen bestehende Liste
        # w[0] = x-position, w[1] = y-position
        # Waffen müssen nach oben abgefeuert werden : x-position nicht geändert, y-position geändert
    
    # Verarbeitung der Waffen, die den oberen Bildschirmrand erreicht haben
    weapons = [ [w[0], w[1] ] for w in weapons if w[1] > 0 ]
        # berücksichtigt wird nur der Fall, dass die Waffen den oberen Rand nicht erreicht haben
    
    screen.blit(bgrd, (0,0))

    # Die Reihenfolge, in der die Ebenen (Layer) geladen werden, beeinflusst, wie Objekte auf dem Bildschirm dargestellt werden.
    # Für ein realistisches Erscheinungsbild, bei dem Waffen scheinbar korrekt vom Charakter abgefeuert werden,
    # ohne mit anderen visuellen Elementen zu kollidieren, ist es entscheidend,
    # die Waffe nach dem Hintergrund, aber vor dem Charakter zu laden.
    for weapon_x_position, weapon_y_position in weapons:
        screen.blit(weapon, (weapon_x_position, weapon_y_position))
    
    screen.blit(platform, (0, screen_height - platform_height))
    screen.blit(character, (character_x_position, character_y_position)) 

    pygame.display.update()

pygame.quit()