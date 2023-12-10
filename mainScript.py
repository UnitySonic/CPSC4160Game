import pygame
import sys
import os
import time
import hp
from Scripts.Logic import gameLogicFunctions
from Scripts.Player import Player
from Scripts.BossScripts.Boss1 import boss1
from Scripts.BossScripts.Boss2 import boss2
from Scripts.Logic import Collision

import subprocess


gameOver = False
stageOver = False

stageSelect = "Boss1"

stageGround = []
stageBackground = []
screen_width    = 1280
screen_height   = 720
screen = pygame.display.set_mode((screen_width, screen_height))






def drawCollisionBoxes():
    for PHitBox in gameLogicFunctions.playerHitBoxGroup:
        BoxSurface = pygame.Surface(PHitBox.rect.size, pygame.SRCALPHA)
        BoxSurface.fill((0,0,255))
        screen.blit(BoxSurface, PHitBox.rect.topleft)


    for PHurtBox in gameLogicFunctions.playerHurtBoxGroup:
        BoxSurface = pygame.Surface(PHurtBox.rect.size, pygame.SRCALPHA)
        BoxSurface.fill((0,255,0))
        screen.blit(BoxSurface, PHurtBox.rect.topleft)

    for EHitBox in gameLogicFunctions.enemyHitBoxGroup:
        BoxSurface = pygame.Surface(EHitBox.rect.size, pygame.SRCALPHA)
        BoxSurface.fill((255,0,0))
        screen.blit(BoxSurface, EHitBox.rect.topleft)

    for EHurtBox in gameLogicFunctions.enemyHurtBoxGroup:
        BoxSurface = pygame.Surface(EHurtBox.rect.size, pygame.SRCALPHA)
        BoxSurface.fill((0,255,0))
        screen.blit(BoxSurface, EHurtBox.rect.topleft)



def collisionDetection():
    detectedCollisions = gameLogicFunctions.detectCollision()

    for collisionType, collisionDict in detectedCollisions.items():
        for playerBox, enemyBoxList in collisionDict.items():

            for enemyBox in enemyBoxList:
                if collisionType == "PHitToEHit":
                    #Hitbox to Hitbox check (Priortize player)
                    playerBox.handleCollision( collisionType, enemyBox)
                    #print("PhitToEHit Detected")
                elif collisionType == "PHitToEHurt":
                    enemyBox.getEntity().handleCollision(collisionType, playerBox)
                    #print("PhitToEHurt Detected")
                elif collisionType == "PHurtToEHit":
                    playerBox.getEntity().handleCollision(collisionType, enemyBox)
                    #print("PHurtToEHit Detected")
                elif collisionType == "PHurtToEHurt":
                    #player priortize
                    playerBox.getEntity().handleCollision(collisionType, enemyBox)
                    #print("PhurtToEHurt Detected")
                else:
                    pass
                playerBox.handleCollision(collisionType, enemyBox)

pygame.init()
while gameOver != True:

    deathCounter = 0
    stageOver = False


    pygame.display.set_caption("The Spell Blade - Milestone 2")

    #set up refresh rate
    clock = pygame.time.Clock()


    #Stage Select

    font = pygame.font.Font(None, 36)

    if stageSelect == "Boss1":
        drawCollision = False
        bgScaleFactorX = 0.75
        bgScaleFactorY = 0.75
        killEntityOutOfScreen = True


        stageBackground.append(pygame.image.load("Assets/Boss_1/sky.png"))
        stageBackground.append(pygame.image.load("Assets/Boss_1/ruins_bg.png"))
        #stageBackground.append(pygame.image.load("Assets/Boss_1/hills&trees.png").convert_alpha())


        #stageBackground.append(pygame.image.load("Assets/Boss_1/ruins2.png").convert_alpha())
        statue = pygame.image.load("Assets/Boss_1/statue.png").convert_alpha()

        groundDimensions = pygame.Rect(-100,600,screen_width + 200, 120)
        groundCollision = Collision.collisionBox(groundDimensions, 0)


        player = Player.Player((300,600))
        boss = boss1.boss_Crimson((800, 600), player)
        playerHP = hp.HP((50,50))
        gameLogicFunctions.addEntity(player)
        gameLogicFunctions.addEntity(boss)
       

        while stageOver != True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    if event.type == pygame.KEYDOWN:
                        pressed = pygame.key.get_pressed()
                        if pressed[pygame.K_h]:
                            drawCollision = not drawCollision
                    player.handle_event(event)
            screen.fill((0,0,0))



            for background in stageBackground:
                new_width = int(background.get_width() * bgScaleFactorX)
                new_height = int(background.get_height() * bgScaleFactorY)

                background = pygame.transform.scale(background, (new_width, new_height))
                screen.blit(background, (0, 0))
            ground = pygame.draw.rect(screen, (128,128,128), groundDimensions)


            currentPlayerHP = player.HP
            collisionDetection()
            if(currentPlayerHP > player.HP and currentPlayerHP > 0):
                playerHP.take_damage(screen)

            screen.blit(playerHP.image, (0, 0))

            for entity in gameLogicFunctions.entityList:
                entity.update()
                if hasattr(entity, "image"):
                    screen.blit(entity.image, entity.rect)
                else:
                    if hasattr(entity, "hitboxes"):
                        for hitbox in entity.hitboxes.values():
                            pygame.draw.rect(screen, (51,0,51), hitbox.rect)
                            if hitbox.rect.x < -10 or hitbox.rect.y > 2000:
                                hitbox.forceKillHitBox()
                    else:
                        pygame.draw.rect(screen, (255,255,255), entity.hurtbox.rect)




            if drawCollision:
                drawCollisionBoxes()
            pygame.display.flip()
            

            if player.HP <= 0:
                deathCounter+= 1
                if deathCounter > 200:
                    command = [sys.executable, "mainScript.py"]

                    # Launch a new process to run the script
                    subprocess.Popen(command)
                    sys.exit()
                    
                
            elif boss.HP <= 0:
                #Display Text
                hint = font.render("Continue right to next level!", True, (255, 255, 255)) 
                hint_rect = hint.get_rect()
                hint_rect.center = (screen_width //2, screen_height//3)

                screen.blit(hint,hint_rect)

                if player.state != "victory" and player.posX > 1100:
                    gameLogicFunctions.clearGroups()
                    import Village2
                    pygame.quit()  
                    raise SystemExit  
            
            pygame.display.flip()
          
            clock.tick(50)
            fps = clock.get_fps()
           












pygame.quit()
