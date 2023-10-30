

import pygame
import boss1

pygame.init()

screen_width    = 800
screen_height   = 800

posx = 400
posy = 400


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Midterm - Spritesheet character animation")

#set up refresh rate
clock = pygame.time.Clock()

#character position
player = boss1.boss_Crimson((posx, posy))

#game loop boolean
game_over = False
player.update("stand_right")

left_pressed = False
right_pressed= False

while game_over == False:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_pressed = True
            elif event.key == pygame.K_RIGHT:
                right_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_pressed = False
                player.update('stand_left')
            elif event.key == pygame.K_RIGHT:
                right_pressed = False
                player.update('stand_right')
        player.handle_event(event)


    if(left_pressed):
        player.update("atk1")
    if(right_pressed):
        player.update("atk2")
    screen.fill((0,0,0))
    screen.blit(player.image, player.rect)
    #player.update("right")

    pygame.display.flip()
    clock.tick(15)

pygame.quit ()
