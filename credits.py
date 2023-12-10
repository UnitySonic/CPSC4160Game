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



# Define the new width and height for the player
new_width = 200
new_height = 200



groundDimensions = pygame.Rect(-100,600,SCREEN_WIDTH + 200, 120)
groundCollision = Collision.collisionBox(groundDimensions, 0)





# Define fonts for the title and start message
title_font = pygame.font.Font(None, 64)
message_font = pygame.font.Font(None, 48)
dialogue_font = pygame.font.Font(None, 24)

# Create the title and start message surfaces
title_text = title_font.render("The Spellblade", True, (0, 0, 0))
message_text = message_font.render("CREATED BY: MICHAEL MERRITT, ISAIAH PICHARDO, ORRIN VALDEZ", True, (0, 0, 0))

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



run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
      

    

    screen.blit(background_image, (0, 0))
    screen.blit(ground_image, (0, SCREEN_HEIGHT - ground_height))
    

    # Draw title and start message in the middle of the screen
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    message_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

  
       
    # checks if text or title screen is shown
    
    screen.blit(title_text, title_rect)
    screen.blit(message_text, message_rect)



    pygame.display.flip()
    clock.tick(FPS)
    


  
# Close the current game window and script
pygame.quit()
raise SystemExit