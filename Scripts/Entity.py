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
        self.transitionActive = False








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


    def set_animation(self, newAnim, reset = False):
        if reset:
            self.resetAnimation(self.animation)
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

    def updateframe(self, currentAnimation):

       
        #Loading JSON ANIMATION DATA!
        self.transitionActive = self.jsonData["animationData"][currentAnimation]["transition"]
        repeat = self.jsonData["animationData"][currentAnimation]["repeat"]
        frameBound = self.jsonData["animationData"][currentAnimation]["totalFramesBound"]
        repeatBound = self.jsonData["animationData"][currentAnimation]["repeatFramesBound"]
        clipsToUse = self.jsonData["animationData"][currentAnimation]["clips"]

        
        #Time to proceed
        frame_set = self.stateToSpriteDict[clipsToUse]
        animationTime = self.animationDict[currentAnimation]["animationTime"]
        currentFrame = self.animationDict[currentAnimation]["frame"]

        if currentFrame < frameBound[0]:
            currentFrame = self.animationDict[currentAnimation]["frame"] = frameBound[0]
            



        transitionOut = False
        animationTime +=1
        if animationTime > 3:
            currentFrame += 1
            animationTime = 0

        if currentFrame > frameBound[1]:
            if self.transitionActive:
                transitionOut = True
                currentFrame = frameBound[1]
            elif repeat:  
                if currentFrame > repeatBound[1]:
                    currentFrame = repeatBound[0]
            else:
                currentFrame = frameBound[1]


        
        self.currentFrameWidth = self.stateToSpriteDict[clipsToUse][currentFrame][2] 
        self.currentFrameHeight = self.stateToSpriteDict[clipsToUse][currentFrame][3] 
        
        if len(frame_set[currentFrame]) > 4:
            framePosX = self.stateToSpriteDict[clipsToUse][currentFrame][0]
            framePosY = self.stateToSpriteDict[clipsToUse][currentFrame][1]
            pivotX = self.stateToSpriteDict[clipsToUse][currentFrame][4]
            pivotY = self.stateToSpriteDict[clipsToUse][currentFrame][5]

            newPivotX = (pivotX - framePosX) * self.scaleFactor
            newPivotY = (pivotY - framePosY) * self.scaleFactor

            if self.direction == 1:
                newX = self.posX - newPivotX
                newY = self.posY - newPivotY
 
            else:
                scaledWidth = self.currentFrameWidth * self.scaleFactor                
                newPivotX = (((scaledWidth)-1)-newPivotX) 

                newX = self.posX - newPivotX
                newY = self.posY - newPivotY
        
        else:
            newY = self.posY - (self.currentFrameHeight * self.scaleFactor)
            newX = 0

            if self.direction == 1:
                newX = self.posX
            else:
                newX = self.posX - (self.currentFrameWidth * self.scaleFactor)
      

        self.rect = pygame.Rect(newX, newY, self.currentFrameWidth, self.currentFrameHeight)

        if len(frame_set[currentFrame]) <= 4:
            self.stateToSheetDict[clipsToUse].set_clip(pygame.Rect(frame_set[currentFrame]))
        else:
            self.stateToSheetDict[clipsToUse].set_clip(pygame.Rect(frame_set[currentFrame][:4]))

       

        self.animationDict[currentAnimation]["frame"] = currentFrame
        self.animationDict[currentAnimation]["animationTime"] = animationTime
        if transitionOut:
            self.resetAnimation(currentAnimation)
            self.transitionActive = False






    def updateSprite(self):
        sheetName = clipsToUse = self.jsonData["animationData"][self.animation]["clips"]

        self.updateframe(self.animation)
        if self.direction == -1:
            self.image = pygame.transform.flip(self.stateToSheetDict[sheetName].subsurface(self.stateToSheetDict[sheetName].get_clip()), True, False)
        else:
            self.image = self.stateToSheetDict[sheetName].subsurface(self.stateToSheetDict[sheetName].get_clip())
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






