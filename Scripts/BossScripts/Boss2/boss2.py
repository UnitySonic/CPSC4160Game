

import pygame
import random
from Scripts.BossScripts.Boss1 import boss1Attacks
from Scripts.Logic import Collision
from Scripts.Logic import gameLogicFunctions








class boss_Demon(pygame.sprite.Sprite):
    def __init__(self, position, Player):

        self.posX = position[0]
        self.posY = position[1]
        self.HP = 100


        self.playerRef = Player

        self.commitToAttack = False
        self.refToCurrentAttack = None
        self.attackIDCounter = 0


        self.elapsedFramesInPhase = 0


        self.state = "idle"
        self.direction = 1

        self.canJump = True
        self.yVelocity = 0
        self.xVelocity = 0




        self.hurtbox = Collision.hurtBox(self, "EHurtBox", pygame.Rect(self.posX, self.posY, 100, 100), 10)



        #Sprite Sheet CONTENT

        
        spriteSheetIdle = "Assets/Boss_2/demon-idle.png"


        #load images
   
        self.sheetIdle = pygame.image.load(spriteSheetIdle)
        


        #loads spritesheet images
        self.image = self.sheetIdle.subsurface(self.sheetIdle.get_clip())
        self.rect = self.image.get_rect()

        #position image in the screen surface
        self.rect.topleft = position

        #variable for looping the frame sequence
        self.frame = 0
        self.animationTime = 0

        self.scaleFactor = 1

        
        self.idle_states = {0: (18,3, 134, 124), 1: (164,35,156,93), 2: (332,35,140,91), 3: (498,33,100,93), 4: (652,35,140,91), 5: (804,35,156,91)}
        
        self.stateToSpriteDict = {"idle" : self.idle_states}
        self.stateToSheetDict = {"idle": self.sheetIdle}
        self.currentFrameWidth = 0
        self.currentFrameHeight = 0





    def set_state(self, new_state):
        self.state = new_state
        self.frame = 0
        self.animationTime = 0
        self.elapsedFramesInPhase = 0
        self.xVelocity = 0
        self.yVelocity = 0




    def getCurrentSpriteWidth(self):
        return self.currentFrameWidth


    def getCurrentSpriteHeight(self):
        return self.currentFrameHeight

    def getSpriteScale(self):
        return self.scaleFactor



    def get_frame(self, frame_set, state):
        #looping the sprite sequences.q q

        self.animationTime +=1

        if self.animationTime > 3:
            self.frame +=1
            self.animationTime = 0
       

        #if loop index is higher that the size of the frame return to the first frame
        if self.frame > (len(frame_set) - 1):
            self.frame = 0


        self.currentFrameWidth =  currentFrameWidth = self.stateToSpriteDict[state][self.frame][2]
        self.currentFrameHeight = currentFrameHeight = self.stateToSpriteDict[state][self.frame][3]
        newY =  self.posY - (currentFrameHeight * self.scaleFactor)
        newX = 0

        if self.direction == 1:
            newX = self.posX
        else:
            newX = self.posX - (currentFrameWidth * self.scaleFactor)



        self.rect = pygame.Rect(newX, newY, currentFrameWidth, currentFrameHeight)


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



   


    def idleState(self):
        self.updateSprite("idle")



        #Two Aspects of this Phase, Running Left and Right, and Jumping
    def handleCollision(self, CollisionType, Box):

        if CollisionType  == "PHitToEHurt":
            self.HP = self.HP - Box.damage




    def update(self):
        self.hurtbox.update()

        self.posX += self.xVelocity
        self.posY += self.yVelocity


        if self.state == "idle":
            self.idleState()
        

        self.elapsedFramesInPhase +=1

    #Start of State functions
