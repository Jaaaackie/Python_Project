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
image_path = os.path.join( curr_path, "images")

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

character_to_x = 0 

character_speed = 5

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []

weapon_speed = 10

# Bälle mit verschiedenen Größen erstellen
ball_images = [
    pygame.image.load(os.path.join(image_path, "ball1.png")),
    pygame.image.load(os.path.join(image_path, "ball2.png")),
    pygame.image.load(os.path.join(image_path, "ball3.png")),
    pygame.image.load(os.path.join(image_path, "ball4.png"))]

# Anfangsgeschwindigkeit der Bälle
ball_speed_y = [-18, -15, -12, -9] # Jeweilige Werte entsprechen dem Index 0, 1, 2, 3 
    # Die negativen Werte : der Ball fliegt erst nach oben und dann wieder nach unten (parabolische Flugbahn)

# Bälle initialisieren
balls = []

# Da wir mehrere Eigenschaften für Bälle haben, verwalten wir sie als Dictionary
# der zuerst abgefeuerte größte Ball hinzufügen
balls.append({
    "ball_position_x" : 50, # x-Koordinate
    "ball_position_y" : 50, # y-Koordinate
    "ball_image_idx" : 0, # Der Index des Ballbildes (Je nach der Größe wird ein entsprechendes Bild verwendet)
    "ball_to_x" : 3, # Bewegungsrichtung auf der x-Achse (-3 : nach links, +3 : nach rechts)
    "ball_to_y" : -6, # Bewegungsrichtung auf der y-Achse (für den Effekt des Aufsteigens und dann Fallens)
    "ball_init_speed_y": ball_speed_y[0] # Anfangsgeschwindigkeit des Balls in y-Richtung
})

running = True 
while running:
    dt = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed

            elif event.key == pygame.K_SPACE:
                weapon_x_position = character_x_position + (character_width - weapon_width) / 2
                weapon_y_position = character_y_position
                weapons.append([weapon_x_position, weapon_y_position])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
    
    character_x_position += character_to_x
    
    if character_x_position < 0:
        character_x_position = 0
    elif character_x_position > screen_width - character_width:
        character_x_position = screen_width - character_width

    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons ]
    
    weapons = [ [w[0], w[1] ] for w in weapons if w[1] > 0 ]

    # Position des Balls definieren
    # zwar Bälle in der Liste, aber da Bälle viele Eigenschaften haben, mit for-Schleife verwalten
    for ball_idx, ball_value in enumerate(balls): # Gibt ein n-ter Index zurück, der dem Wert in der Ball-Liste entspricht
        ball_position_x = ball_value["ball_position_x"] # x-Koordinate des Balls
        ball_position_y = ball_value["ball_position_y"] # y-Koordinate des Balls
        ball_image_idx = ball_value["ball_image_idx"] # Index des Ballbildes (Welches Bild wird verwendet?)

        ball_size = ball_images[ball_image_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # Abprallen-Effekte anwenden, falls Bälle mit den Randen getroffen werden
        # Abprallen von den horizontalen Wänden
        if ball_position_x < 0 or ball_position_x > screen_width - ball_width:
            ball_value["ball_to_x"] = ball_value["ball_to_x"] * -1 # mit -1 multiplizieren : die Richtung umkehren

        # vertikale Position
        # Wenn der Ball den Platform berührt, springt er nach oben
        # da er mit dem Platform getroffen ist, Anfangsgeschwindigkietswert anwenden
        if ball_position_y >= screen_height - platform_height - ball_height:
            ball_value["ball_to_y"] = ball_value["ball_init_speed_y"]
        
        # In allen anderen Fällen, die nicht das Berühren des Platforms sind, erhöht die Geschwindigkeit der Bällen 
            # (Startwert < 0) Die Höhe, die der Ball im Laufe der Zeit erreicht, verringert sich,
            # damit er in einer Parabel aufsteigt und dann fällt
        else: 
            ball_value["ball_to_y"] += 0.5
        
        ball_value["ball_position_x"] += ball_value["ball_to_x"]
        ball_value["ball_position_y"] += ball_value["ball_to_y"]

    screen.blit(bgrd, (0,0))

    for weapon_x_position, weapon_y_position in weapons:
        screen.blit(weapon, (weapon_x_position, weapon_y_position))
    
    # Bälle zeichnen
    for idx, val in enumerate(balls):
        ball_position_x = val["ball_position_x"]
        ball_position_y = val["ball_position_y"]
        ball_image_idx = val["ball_image_idx"]
        screen.blit(ball_images[ball_image_idx], (ball_position_x, ball_position_y)) 
        

    screen.blit(platform, (0, screen_height - platform_height))
    screen.blit(character, (character_x_position, character_y_position))
    
    
    pygame.display.update()

pygame.quit()

