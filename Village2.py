import pygame
import os
import time
import sys
from Scripts.Player.Player import Player
from npc import NPC
from Scripts.Logic import gameLogicFunctions
from Scripts.Logic import Collision

pygame.init()

clock = pygame.time.Clock()

FPS = 50

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Starter Village")

#define game variables
scroll = 0

# Load a single background image
background_image_path = os.path.join("Assets", "nature_3", "origbig.png")
background_image = pygame.image.load(background_image_path).convert_alpha()
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Draw ground image
ground_image_path = os.path.join("Assets", "nature_3", "ground.png")
ground_image = pygame.image.load(ground_image_path).convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()
ground_image = pygame.transform.scale(ground_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Character initialization with starting position and correct image paths
main_character = Player((200, 650))

# Define the new width and height for the player
new_width = 200
new_height = 200

# Resize the player's image
main_character.image = pygame.transform.scale(main_character.image, (new_width, new_height))

# Update the player's rect to match the new dimensions
main_character.rect = main_character.image.get_rect()
main_character.rect.topleft = (400, 350)


groundDimensions = pygame.Rect(-100,600,SCREEN_WIDTH + 200, 120)
groundCollision = Collision.collisionBox(groundDimensions, 0)



# adds in the NPC instances
npc1 = NPC(650, 350, 250, 150, move_range=1, speed=.2)

# defines npc boundaries to clamp them in a location
npc1_x_min = 650
npc1_x_max = 750

# creates sprite group for all sprites to load them in
npc_sprites = pygame.sprite.Group()
npc_sprites.add(npc1)

# Define fonts for the title and start message
title_font = pygame.font.Font(None, 64)
message_font = pygame.font.Font(None, 36)
dialogue_font = pygame.font.Font(None, 24)

# Create the title and start message surfaces
title_text = title_font.render("The Spellblade", True, (153, 102, 204))
message_text = message_font.render("Press Space to Start", True, (153, 102, 204))

# Initialize the show_title
show_title = False

# Index to track dialogue progress
show_dialogue = True
dialogue_index = 0
# tracks the timing between dialogue
dialogue_timer = time.time()

# Define the background for dialogue
dialogue_background = pygame.Surface((800, 200))
dialogue_background.fill((0, 0, 0))
dialogue_background.set_alpha(150)

dialogue_texts = [

    "I sensed that you were able to defeat Crimson, Cyline.",
    "Taking him down was no small feat. Well done.",
    "There are still other fallen mages that we must deal with.",
    "I wish I could give you your next target...but...",
    "I still don't have any intelligence on their wherabouts.",
    "For now though, you should take some time to relax and celebrate your victory",
    "When they make their prescene known, I'll contact you"
]

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # respond to player events
        main_character.handle_event(event)

    # Input data: Left and right keys to move
    character_speed = 6

    key = pygame.key.get_pressed()
    main_character.update()

    

    # Limit the character's movement to stay within screen bounds
    if scroll < 0:
        scroll = 0

    elif scroll > 1200:
        scroll = 1200

    # npc movement in designated bounds
    npc1.update(FPS)

    screen.blit(background_image, (0, 0))
    screen.blit(ground_image, (0, SCREEN_HEIGHT - ground_height))
    screen.blit(main_character.image, main_character.rect)

    # Draw title and start message in the middle of the screen
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 50))
    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50))

    # Draw the current dialogue text
    if show_dialogue:
        if dialogue_index < len(dialogue_texts):
            # Display the background behind the dialogue text
            screen.blit(dialogue_background, (SCREEN_WIDTH // 2 - 400, SCREEN_HEIGHT // 3 - 100))
            dialogue_text = dialogue_font.render(dialogue_texts[dialogue_index], True, (255, 255, 255))
            dialogue_rect = dialogue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 - 50))
            screen.blit(dialogue_text, dialogue_rect)

            # Display "Press T to Continue" hint
            hint_text = dialogue_font.render("Press T to Continue", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 75))
            screen.blit(hint_text, hint_rect)
        else:
            # Display "Continue Right to next level -->" hint
            hint_text = dialogue_font.render("Continue Right to next level -->", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 75))
            screen.blit(hint_text, hint_rect)

    # checks if text or title screen is shown
    if show_title:
        screen.blit(title_text, title_rect)
        screen.blit(message_text, message_rect)

    # Handle visibility of text after pressing space
    key = pygame.key.get_pressed()
    if show_title:
        if key[pygame.K_SPACE]:
            show_title = False
            show_dialogue = True

    #text delay before they can press T again
    elif show_dialogue:
        if dialogue_index < len(dialogue_texts):
            if key[pygame.K_t] and time.time() - dialogue_timer > 1:
                dialogue_index += 1
                dialogue_timer = time.time()

    # draws npcs
    npc_sprites.update(FPS)
    npc_sprites.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
    
    

    if main_character.rect.right > 1100:

        # Transition to the new file (testvill.py)
        import credits

        # closes the current game window
        pygame.quit()  

        # quits the current script
        raise SystemExit  


# Close the current game window and script
pygame.quit()
raise SystemExit