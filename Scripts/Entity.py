import pygame
from Scripts.Logic import gameLogicFunctions
from Scripts.Logic import Collision
import json



class Entity:

    def __init__(self, position):
        #load all spritesheets
        self.jsonData = None


        self.posX = position[0]
        self.posY = position[1]
        self.direction = 1


        self.currentSprite = 0
        self.isJumping = False

        self.elapsedFramesInState = 0







        self.currentFrameWidth = 0
        self.currentFrameHeight = 0
        self.scaleFactor = 1

        self.stateToSheetDict = {}
        self.stateToSpriteDict = {}
        self.stateToFunctionDict = {}
        self.animationDict = {}

        self.state = None
        self.animation = None





    def set_state(self, new_state):

        self.state = new_state
        self.elapsedFramesInState = 0


    def set_animation(self, newAnim):
        self.animationDict[self.animation]["frame"] = 0
        self.animationDict[self.animation]["animationTime"] = 0
        self.animationDict[self.animation]["transition"] = False

        self.animation = newAnim



    def resetAnimation(self, animID):
        #animID 0 is frames
        #animIDD0 is activeFrame

        self.animationDict[animID]["frame"] = 0
        self.animationDict[animID]["animationTime"] = 0
        self.animationDict[animID]["transition"] = False


    def getCurrentSpriteWidth(self):
        return self.currentFrameWidth

    def getCurrentSpriteHeight(self):
        return self.currentFrameHeight

    def getSpriteScale(self):
        return self.scaleFactor

    def get_frame(self, frame_set, state):

        repeat = self.jsonData["animationData"][state]["repeat"]
        transitionOutBound = self.jsonData["animationData"][state]["transitionOutBound"]
        repeatBound = self.jsonData["animationData"][state]["repeatFramesBound"]

        animationTime = self.animationDict[state]["animationTime"]
        currentFrame = self.animationDict[state]["frame"]


        animationTime +=1

        if animationTime > 3:
            currentFrame += 1

            animationTime = 0

        #print("before")
        #print(self.animationDict[state]["frame"])



        if repeat:
            if currentFrame > repeatBound[1]:
                currentFrame = repeatBound[0]
        elif currentFrame > (int(len(frame_set)) -1):
            currentFrame= int(len(self.stateToSpriteDict[state] )- 1)


        #print("after")
        #print(self.animationDict[state]["frame"])



        self.currentFrameWidth = self.stateToSpriteDict[state][currentFrame][2]
        self.currentFrameHeight = self.stateToSpriteDict[state][currentFrame][3]
        newY = self.posY - (self.currentFrameHeight * self.scaleFactor)
        newX = 0

        if self.direction == 1:
            newX = self.posX
        else:
            newX = self.posX - (self.currentFrameWidth * self.scaleFactor)

        self.rect = pygame.Rect(newX, newY, self.currentFrameWidth, self.currentFrameHeight)


        self.stateToSheetDict[state].set_clip(pygame.Rect(frame_set[currentFrame]))

        self.animationDict[state]["frame"] = currentFrame
        self.animationDict[state]["animationTime"] = animationTime






    def updateSprite(self):


        stateToUse = self.animation


        self.get_frame(self.stateToSpriteDict[stateToUse], stateToUse)
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
        self.elapsedFramesInState += 1
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






