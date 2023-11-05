import pygame
import sys
from Scripts.Logic import gameLogicFunctions
from Scripts.Player import Player
from Scripts.BossScripts.Boss1 import boss1
from Scripts.Logic import Collision


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
                elif collisionType == "PHitToEHurt":
                    enemyBox.getEntity().handleCollision(collisionType, playerBox)
                elif collisionType == "PHurtToEHit":
                    playerBox.getEntity().handleCollision(collisionType, enemyBox)
                elif collisionType == "PHurtToEHurt":
                    #player priortize
                    playerBox.getEntity().handleCollision(collisionType, enemyBox)
                else:
                    pass
                playerBox.handleCollision(collisionType, enemyBox)

while gameOver != True:


    pygame.display.set_caption("Midterm - Spritesheet character animation")

    #set up refresh rate
    clock = pygame.time.Clock()


    #Stage Select


    if stageSelect == "Boss1":
        bgScaleFactorX = 0.75
        bgScaleFactorY = 0.75
        killEntityOutOfScreen = True


        stageBackground.append(pygame.image.load("Assets/Boss_1/sky.png"))
        stageBackground.append(pygame.image.load("Assets/Boss_1/ruins_bg.png"))
        #stageBackground.append(pygame.image.load("Assets/Boss_1/hills&trees.png").convert_alpha())


        #stageBackground.append(pygame.image.load("Assets/Boss_1/ruins2.png").convert_alpha())
        statue = pygame.image.load("Assets/Boss_1/statue.png").convert_alpha()

        groundDimensions = pygame.Rect(0,600,screen_width, 120)
        groundCollision = Collision.collisionBox(groundDimensions, 0)


        player = Player.Player((300,300))
        boss = boss1.boss_Crimson((400, 400), player)
        gameLogicFunctions.addEntity(player)
        gameLogicFunctions.addEntity(boss)

        while stageOver != True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    player.handle_event(event)
            screen.fill((0,0,0))



            for background in stageBackground:
                new_width = int(background.get_width() * bgScaleFactorX)
                new_height = int(background.get_height() * bgScaleFactorY)

                background = pygame.transform.scale(background, (new_width, new_height))
                screen.blit(background, (0, 0))
            ground = pygame.draw.rect(screen, (128,128,128), groundDimensions)


            collisionDetection()

            for entity in gameLogicFunctions.entityList:
                entity.update()
                if hasattr(entity, "image"):
                    screen.blit(entity.image, entity.rect)
                else:
                    if hasattr(entity, "hitboxes"):
                        for hitbox in entity.hitboxes.values():
                            pygame.draw.rect(screen, (255,255,255), hitbox.rect)
                            if hitbox.rect.x < -10 or hitbox.rect.y > 2000:
                                gameLogicFunctions.removeEntity(entity)
                    else:
                        pygame.draw.rect(screen, (255,255,255), entity.hurtbox.rect)
            print(len(gameLogicFunctions.entityList))





            drawCollisionBoxes()
            pygame.display.flip()

            #gameLogicFunctions.clearGroups()
            clock.tick(60)












pygame.quit()
