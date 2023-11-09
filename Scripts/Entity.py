import pygame
from Scripts.Logic import gameLogicFunctions
from Scripts.Logic import Collision



class Entity:

    def __init__(self, position):
        #load all spritesheets


        self.posX = position[0]
        self.posY = position[1]
        self.direction = 1


        self.currentSprite = 0
        self.isJumping = False

        self.elapsedFramesInPhase = 0


        self.frame = 0
        self.animationTime = 0




        self.currentFrameWidth = 0
        self.currentFrameHeight = 0
        self.scaleFactor = 1

        self.stateToSheetDict = {}
        self.stateToSpriteDict = {}
        self.stateToFunctionDict = {}

        self.state = None

    def set_state(self, new_state):
        self.state = new_state
        self.frame = 0
        self.animationTime = 0
        self.elapsedFramesInPhase = 0

    def getCurrentSpriteWidth(self):
        return self.currentFrameWidth

    def getCurrentSpriteHeight(self):
        return self.currentFrameHeight

    def getSpriteScale(self):
        return self.scaleFactor

    def get_frame(self, frame_set, state):

        self.animationTime += 1

        if self.animationTime > 3:
            self.frame += 1
            self.animationTime = 0

        if self.frame > (len(frame_set) - 1):
            self.frame = 0

        self.currentFrameWidth = self.stateToSpriteDict[state][self.frame][2]
        self.currentFrameHeight = self.stateToSpriteDict[state][self.frame][3]
        newY = self.posY - (self.currentFrameHeight * self.scaleFactor)
        newX = 0

        if self.direction == 1:
            newX = self.posX
        else:
            newX = self.posX - (self.currentFrameWidth * self.scaleFactor)

        self.rect = pygame.Rect(newX, newY, self.currentFrameWidth, self.currentFrameHeight)

        return frame_set[self.frame]


    def clip(self, clipped_rect, state):
            if type(clipped_rect) is dict:
                self.stateToSheetDict[state].set_clip(pygame.Rect(self.get_frame(clipped_rect,state)))
            else:
                self.stateToSheetDict[state].set_clip(pygame.Rect(clipped_rect))

            return clipped_rect

    def updateSprite(self, stateToUse, transition = False):

        if transition:
            self.frame = 0

        self.clip(self.stateToSpriteDict[stateToUse], stateToUse)
        if self.direction == -1:
            self.image = pygame.transform.flip(self.stateToSheetDict[stateToUse].subsurface(self.stateToSheetDict[stateToUse].get_clip()), True, False)
        else:
            self.image = self.stateToSheetDict[stateToUse].subsurface(self.stateToSheetDict[stateToUse].get_clip())
        #Scaling
        scaledX = int(self.rect.width * self.scaleFactor)
        scaledY = int(self.rect.height * self.scaleFactor)
        self.image = pygame.transform.scale(self.image, (scaledX,scaledY))


    def handleCollision(self, CollisionType, Box):
        if CollisionType == "PHurtToEHit":

            self.HP - Box.damage

        elif CollisionType == "PHurtToEHurt":
            self.HP - Box.damage




    def update(self):
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.hurtbox.update()
        self.elapsedFramesInPhase += 1
        self.stateToFunctionDict[self.state]()



    def isGrounded(self):
        collide = pygame.sprite.spritecollide(self.hurtbox, gameLogicFunctions.collisionGroup, False)
        if collide:
            return True
        else:
            return False

    def isGrounded(self):
        collide = pygame.sprite.spritecollide(self.hurtbox, gameLogicFunctions.collisionGroup, False)
        if collide:
            return True
        else:
            return False






