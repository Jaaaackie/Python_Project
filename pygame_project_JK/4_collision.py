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

character_to_x = 0

character_speed = 5

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []

weapon_speed = 10

ball_images = [
    pygame.image.load(os.path.join(image_path, "ball1.png")),
    pygame.image.load(os.path.join(image_path, "ball2.png")),
    pygame.image.load(os.path.join(image_path, "ball3.png")),
    pygame.image.load(os.path.join(image_path, "ball4.png"))]

ball_speed_y = [-18, -15, -12, -9]

balls = []

balls.append({
    "ball_position_x" : 50,
    "ball_position_y" : 50,
    "ball_image_idx" : 0,
    "ball_to_x" : 3,
    "ball_to_y" : -6,
    "ball_init_speed_y": ball_speed_y[0]
})

# Definition der Variablen für Waffen und Bälle, die bei Kollision verschwinden
# Wenn sie kollidieren und verschwinden, ist das das Ende, also werden sie aus der Liste der zu ladenden Waffen/Bälle entfernt
weapon_to_remove = -1
ball_to_remove = -1

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

    for ball_idx, ball_val in enumerate(balls):
        ball_position_x = ball_val["ball_position_x"]
        ball_position_y = ball_val["ball_position_y"]
        ball_image_idx = ball_val["ball_image_idx"]

        ball_size = ball_images[ball_image_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_position_x < 0 or ball_position_x > screen_width - ball_width:
            ball_val["ball_to_x"] = ball_val["ball_to_x"] * -1

        if ball_position_y >= screen_height - platform_height - ball_height:
            ball_val["ball_to_y"] = ball_val["ball_init_speed_y"]

        else: 
            ball_val["ball_to_y"] += 0.5
        
        ball_val["ball_position_x"] += ball_val["ball_to_x"]
        ball_val["ball_position_y"] += ball_val["ball_to_y"]

    # Kollision zwischen Bildern verarbeiten
    # rect-Info für Charakter aktualisieren
    character_rect = character.get_rect()
    character_rect.left = character_x_position
    character_rect.right = character_y_position

    for ball_idx, ball_val in enumerate(balls): 
        ball_position_x = ball_val["ball_position_x"]
        ball_position_y = ball_val["ball_position_y"]
        ball_image_idx = ball_val["ball_image_idx"]

        # rect-Info für Bälle aktualisieren
        ball_rect = ball_images[ball_image_idx].get_rect()
        ball_rect.left = ball_position_x
        ball_rect.top = ball_position_y

        # Kollision zwischen Ball und Charakter prüfen
        if character_rect.colliderect(ball_rect):
            running = False
            break # for-Schleife verlassen 

        # Da mehrere Bälle aus dem Waffe gleichzeitig abgefeuert werden können,
        # kann dies nicht mit einer einzigen if-Bedingung behandelt werden,
        # sondern jeder Wert in der Waffenliste muss einzeln überprüft werden
        # Kollision zwischen Ball und Waffe behandeln
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_position_x = weapon_val[0]
            weapon_position_y = weapon_val[1]

            # rect-Info für Waffen aktualisieren
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_position_x
            weapon_rect.top = weapon_position_y

            # Kollisionsprüfung 
            if weapon_rect.colliderect(ball_rect):
                # Waffe und Ball entfernen : Angenommen, es gibt mehrere Bälle, welcher Ball soll entfernt werden?
                weapon_to_remove = weapon_idx # Wert festlegen, um die betreffende Waffe zu entfernen
                ball_to_remove = ball_idx # Wert festlegen, um den betreffenden Ball zu entfernen
                break # if-Schleife verlassen wergen Kollision

    # Kollidierte Bälle/Waffen entfernen
    if ball_to_remove > -1: # Da es sich um einen Index handelt, muss er immer größer oder gleich 0 sein
        del balls[ball_to_remove]
        ball_to_remove = -1 # Damit im nächsten Frame wieder -1 aktualisiert wird

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    screen.blit(bgrd, (0,0))

    for weapon_x_position, weapon_y_position in weapons:
        screen.blit(weapon, (weapon_x_position, weapon_y_position))
    
    for idx, val in enumerate(balls):
        ball_position_x = val["ball_position_x"]
        ball_position_y = val["ball_position_y"]
        ball_image_idx = val["ball_image_idx"]
        screen.blit(ball_images[ball_image_idx], (ball_position_x, ball_position_y)) 
        

    screen.blit(platform, (0, screen_height - platform_height))
    screen.blit(character, (character_x_position, character_y_position))
    
    
    pygame.display.update()

pygame.quit()