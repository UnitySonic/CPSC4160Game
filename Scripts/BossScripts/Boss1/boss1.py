

import pygame
import random
from Scripts.BossScripts.Boss1 import boss1Attacks
from Scripts.Logic import Collision
from Scripts.Logic import gameLogicFunctions








class boss_Crimson(pygame.sprite.Sprite):
    def __init__(self, position, Player):

        self.posX = position[0]
        self.posY = position[1]
        self.HP = 100


        self.playerRef = Player

        self.commitToAttack = False
        self.refToCurrentAttack = None
        self.elapsedFramesInPhase = 0


        self.state = "runAround"
        self.direction = 1

        self.animationTime = 0


        self.hurtbox = Collision.hurtBox(self, "EHurtBox", pygame.Rect(self.posX, self.posY, 50, 100), 10)


        spriteSheetAttack1 = "Assets/Boss_1/Attack1.png"
        spriteSheetAttack2 = "Assets/Boss_1/Attack2.png"
        spriteSheetDeath = "Assets/Boss_1/Death.png"
        spriteSheetFall = "Assets/Boss_1/Fall.png"
        spriteSheetIdle = "Assets/Boss_1/Idle.png"
        spriteSheetJump = "Assets/Boss_1/Jump.png"
        spriteSheetRun = "Assets/Boss_1/Run.png"
        spriteSheetHit = "Assets/Boss_1/Take hit.png"

        #load images
        self.sheetAtk1 = pygame.image.load(spriteSheetAttack1)
        self.sheetAtk2 = pygame.image.load(spriteSheetAttack2)
        self.sheetDeath = pygame.image.load(spriteSheetDeath)
        self.sheetFall = pygame.image.load(spriteSheetFall)
        self.sheetIdle = pygame.image.load(spriteSheetIdle)
        self.sheetJump = pygame.image.load(spriteSheetJump)
        self.sheetRun = pygame.image.load(spriteSheetRun)
        self.sheetHit = pygame.image.load(spriteSheetHit)

        #defines area of a single sprite of an image
        #self.sheet.set_clip(pygame.Rect(0, 0, 0, 0))

        #loads spritesheet images
        self.image = self.sheetAtk1.subsurface(self.sheetAtk1.get_clip())
        self.rect = self.image.get_rect()

        #position image in the screen surface
        self.rect.topleft = position

        #variable for looping the frame sequence
        self.frame = 0

        self.scaleFactor = 2

        self.atk1_states = {0: (74,107,58,60), 1: (328,98,55,69), 2: (584,91,52,76), 3: (859,88,120,79),4: (1109,52,127,115), 5: (1359,47,127,120), 6: (1609,26,127,141), 7: (1859,47,79,120)}
        self.atk2_states = {0: (109,58,72,109),1: (334,60,72,107),2: (581,53,75,114),3: (832,45,75, 122),4: (1083,39,160,129), 5: (1338,43,148,131),6: (1592,45,141,135),7: (1859, 81, 66,87)}

        self.death_states = {0: (108,84,45,83), 1: (358,74,52,93), 2: (608,72,66,95), 3: (858,64,96,103), 4: (1108,57,105,110), 5: (1358,45,96,122), 6: (1608,154,105,13)}
        self.fall_states = {0: (107,81,65,86), 1: (357,74,64,93)}
        self.idle_states = {0: (108,72, 57, 95), 1: (358,67,56,100), 2: (608,64,56,103), 3: (858,64,56,103), 4: (1108,67,57,100), 5: (1358,63,55,104), 6: (1608,70,54,97), 7: (1858,70,56,97)}
        self.jump_states = {0: (91,86,69,81), 1: (332,87,78,80)}
        self.run_states = {0: (94,106,65,61), 1: (342,105,67,62), 2: (592,102,67,65), 3: (839,99,70,68), 4: (1092,106,67,61), 5: (1343,100,66,67), 6: (1594,102,65,65), 7: (1846,100,63,64)}
        self.hit_states = {0: (106,80,45,87), 1: (358,81,34,86), 2: (608,87,35,80)}

        self.stateToSpriteDict = {"runAround" : self.run_states, "atk1" : self.atk1_states, "atk2" : self.atk2_states}
        self.stateToSheetDict = {"runAround" : self.sheetRun, "atk1" : self.sheetAtk1, "atk2" : self.sheetAtk2}





    def set_state(self, new_state):
        self.state = new_state


    def get_frame(self, frame_set, state):
        #looping the sprite sequences.q q

        self.animationTime +=1

        if self.animationTime > 3:
            self.frame +=1
            self.animationTime = 0


        #if loop index is higher that the size of the frame return to the first frame
        if self.frame > (len(frame_set) - 1):
            self.frame = 0




        currentFrameWidth = self.stateToSpriteDict[state][self.frame][2]
        currentFrameHeight = self.stateToSpriteDict[state][self.frame][3]
        newY =  self.posY - (currentFrameHeight * self.scaleFactor)
        newX = self.posX - currentFrameWidth * self.scaleFactor


        self.rect.update((newX, newY), (currentFrameWidth, currentFrameHeight))


        return frame_set[self.frame]

    def clip(self, clipped_rect, state):
        if type(clipped_rect) is dict:
            self.stateToSheetDict[state].set_clip(pygame.Rect(self.get_frame(clipped_rect,state)))
        else:
            self.stateToSheetDict[state].set_clip(pygame.Rect(clipped_rect))

        return clipped_rect

    def updateSprite(self, stateToUse):

        self.clip(self.stateToSpriteDict[stateToUse], stateToUse)
        if self.direction == -1:
            self.image = pygame.transform.flip(self.stateToSheetDict[stateToUse].subsurface(self.stateToSheetDict[stateToUse].get_clip()), True, False)
        else:
            self.image = self.stateToSheetDict[stateToUse].subsurface(self.stateToSheetDict[stateToUse].get_clip())
        #Scaling
        scaledX = int(self.rect.width * self.scaleFactor)
        scaledY = (self.rect.height * self.scaleFactor)
        self.image = pygame.transform.scale(self.image, (scaledX,scaledY))






    def runAroundState(self):

        MAXTIMEINPHASE = 600

        self.updateSprite("runAround")
        if self.posX <= 5 or self.posX >= 1200:
            self.direction *= -1
        self.posX += 4 * self.direction
        self.elapsedFramesInPhase +=1

        if self.elapsedFramesInPhase >= MAXTIMEINPHASE:
            self.elapsedFramesInPhase = 0
            self.set_state("atk1")





    def atk1State(self):
        #Move toward player, and then hit them when in range (60 units)

        if self.commitToAttack == False:
            distance = self.rect.centerx - self.playerRef.rect.centerx
            print(f"distance : {distance}")

            print(f"centerXBoss: {self.rect.centerx}")
            print(f"centerXPlayer2 : {self.playerRef.rect.centerx}")

            if abs(distance) > 60:
                if (distance < 0):
                    self.direction = 1
                if(distance > 0):
                    self.direction = -1

                self.posX += 4 * self.direction
                self.updateSprite("runAround")
            else:

                self.commitToAttack = True
                self.refToCurrentAttack = boss1Attacks.meleeAttack1(self)
        else:
            if (self.refToCurrentAttack == None):
                self.elapsedFramesInPhase = 0
                self.commitToAttack = False
                self.set_state("runAround")

            else:
                self.updateSprite("atk1")
                self.refToCurrentAttack.update()







    def attackEnded(self):
        del self.refToCurrentAttack
        self.refToCurrentAttack = None



    def jumpState(self, elapsedTime, MAXTIMEINPHASE):
        pass




        #Two Aspects of this Phase, Running Left and Right, and Jumping


    def handleCollision(self, CollisionType, Box):

        if CollisionType  == "PHitToEHurt":
            self.HP = self.HP - Box.damage




    def update(self):
        self.hurtbox.update()
        if self.state == "runAround":
            self.runAroundState()
        elif self.state == "atk1":
            self.atk1State()
        self.elapsedFramesInPhase +=1

    #Start of State functions





