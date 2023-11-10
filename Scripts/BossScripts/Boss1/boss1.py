

import pygame
import random
from Scripts.BossScripts.Boss1 import boss1Attacks
from Scripts.Logic import Collision
from Scripts.Logic import gameLogicFunctions
from Scripts import Entity
import json








class boss_Crimson(Entity.Entity):
    def __init__(self, position, Player):


        super().__init__(position)

        directory = "Scripts/BossScripts/Boss1/boss1Data.json"

        with open(directory, "r") as file:
            self.jsonData = json.load(file)

        self.HP = 100


        self.playerRef = Player

        self.commitToAttack = False
        self.refToCurrentAttack = None
        self.attackIDCounter = 0


        self.elapsedFramesInPhase = 0


        self.state = "idle"
        self.animation = "idle"


        self.direction = 1
        self.canJump = True
        self.yVelocity = 1
        self.xVelocity = 0




        self.hurtbox = Collision.hurtBox(self, "EHurtBox", pygame.Rect(self.posX, self.posY, 50, 100), 10)



        #load images
        self.sheetAtk1 = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetAtk1"])
        self.sheetAtk2 = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetAtk2"])
        self.sheetDeath = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetDeath"])
        self.sheetFall = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetFall"])
        self.sheetIdle = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetIdle"])
        self.sheetJump = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetJump"])
        self.sheetRun = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetRun"])
        self.sheetHit = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetHit"])



        #loads spritesheet images
        self.image = self.sheetAtk1.subsurface(self.sheetAtk1.get_clip())
        self.rect = self.image.get_rect()

        #position image in the screen surface
        self.rect.topleft = position

        #variable for looping the frame sequence
        self.frame = 0
        self.animationTime = 0

        self.scaleFactor = 2

        self.atk1Clips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["atk1Clips"].items()}
        self.atk2Clips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["atk2Clips"].items()}

        self.deathClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["deathClips"].items()}
        self.fallClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["fallClips"].items()}
        self.idleClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["idleClips"].items()}
        self.jumpClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["jumpClips"].items()}
        self.runClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["runClips"].items()}
        self.hitClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["hitClips"].items()}

        self.stateToSpriteDict = {"runAround" : self.runClips, "atk1" : self.atk1Clips, "atk2" : self.atk2Clips, "death" : self.deathClips, "fall" : self.fallClips, "idle" : self.idleClips,
                                  "jump" : self.jumpClips, "hit" : self.hitClips}
        self.stateToSheetDict = {"runAround" : self.sheetRun, "atk1" : self.sheetAtk1, "atk2" : self.sheetAtk2, "death" : self.sheetDeath, "fall" : self.sheetFall, "idle": self.sheetIdle,
                                 "jump" : self.sheetJump, "hit" : self.sheetHit}
        
        self.stateToFunctionDict = {"idle": self.idleState,
                                    "runAround": self.runAroundState,
                                    "jump": self.jumpState,
                                    "atk1": self.atk1State,
                                    "atk2": self.atk2State,
                                    "fireball": self.fireballState
                                   }
                                 
        

        for key in self.stateToSpriteDict.keys():
            self.animationDict[key] = {
                "frame" : 0,
                "animationTime": 0,
                "transition" : False
            }
        self.currentFrameWidth = 0
        self.currentFrameHeight = 0





    



    

    def runAroundState(self):

        MAXTIMEINPHASE = 300

        #self.updateSprite("runAround")
        if self.posX <= 15 or self.posX >= 1200:
            self.direction *= -1
        self.xVelocity = 4 * self.direction

        if self.elapsedFramesInPhase >= MAXTIMEINPHASE:
            self.elapsedFramesInPhase = 0
            self.xVelocity = 0
            self.set_state("idle")





    def atk1State(self):
        #Move toward player, and then hit them when in range (60 units)

        if self.commitToAttack == False:
            distance = self.rect.centerx - self.playerRef.rect.centerx


            if abs(distance) > 60:
                if (distance < 0):
                    self.direction = 1
                if(distance > 0):
                    self.direction = -1

                self.xVelocity = 4 * self.direction
                self.set_animation("runAround", False)
            else:

                self.commitToAttack = True
                self.refToCurrentAttack = boss1Attacks.meleeAttack1(self)
                self.set_animation("atk1")
                self.xVelocity = 0
        else:
            if (self.refToCurrentAttack == None):
                self.elapsedFramesInPhase = 0
                self.commitToAttack = False
                self.set_state("idle")

            else:
                
                self.refToCurrentAttack.update()

    def atk2State(self):
        if self.commitToAttack == False:
            distance = self.rect.centerx - self.playerRef.rect.centerx


            if abs(distance) > 60:
                if (distance < 0):
                    self.direction = 1
                if(distance > 0):
                    self.direction = -1

                self.xVelocity = 4 * self.direction
                self.set_animation("runAround", False)
            else:

                self.commitToAttack = True
                self.refToCurrentAttack = boss1Attacks.meleeAttack2(self)
                self.set_animation("atk2")
                self.xVelocity = 0
        else:
            if (self.refToCurrentAttack == None):
                self.commitToAttack = False
                self.set_state("idle")
            else:
                
                self.refToCurrentAttack.update()



    def fireballState(self):

        if(self.commitToAttack == False):
            self.refToCurrentAttack = boss1Attacks.Fireball(0, 8 *self.direction, True, self)
            self.commitToAttack = True
        else:
            if(self.refToCurrentAttack == None):
                self.set_state("idle")
                self.commitToAttack = False
            else:
                self.refToCurrentAttack.update()



    def attackEnded(self):
        del self.refToCurrentAttack
        self.refToCurrentAttack = None



    def jumpState(self, beginFall = False):
         if beginFall == True:
             self.elapsedFramesInPhase = 40


         if self.posX <= 15 or self.posX >= 1200:
            self.direction *= -1
         self.xVelocity = 4 * self.direction
         if self.elapsedFramesInPhase >= 40:
             if self.isGrounded():
                 self.yVelocity = 0
                 self.elapsedFramesInPhase = 0
                 self.set_state("runAround")
                 self.set_animation("runAround")
             else:
                self.yVelocity = 5
                self.set_animation("fall", False)
         else:
             self.yVelocity = -5
             self.set_animation("jump", False)


    def isGrounded(self):
        collide = pygame.sprite.spritecollide(self.hurtbox, gameLogicFunctions.collisionGroup, False)
        if collide:
            return True
        else:
            return False


    def idleState(self):
        IDLESTATETIME = 120
        self.set_animation("idle")
        


        if self.elapsedFramesInPhase >= IDLESTATETIME:

            choice = random.randint(0,4)
           

            if choice == 0:
                self.set_state("runAround")
            elif choice == 1:
                self.set_state("atk1")
            elif choice == 2:
                self.set_state("atk2")
            elif choice == 3:
                self.set_state("fireball")
            elif choice == 4:
                self.set_state("jump")



        #Two Aspects of this Phase, Running Left and Right, and Jumping
    def handleCollision(self, CollisionType, Box):

        if CollisionType  == "PHitToEHurt":
            self.HP = self.HP - Box.damage




    def update(self):
        self.hurtbox.update()
        self.updateSprite()

        self.posX += self.xVelocity
        self.posY += self.yVelocity



        if self.isGrounded() == False and self.yVelocity>0:
            self.set_state("jump")
            self.jumpState(True)

        self.stateToFunctionDict[self.state]()



        self.elapsedFramesInPhase +=1

    #Start of State functions
