

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


        self.elapsedFramesInState = 0


        self.state = "idle"
        self.animation = "idle"


        self.direction = 1
        self.canJump = True
        self.yVelocity = 1
        self.xVelocity = 0

        self.priorityLastHitBy = -1



        ##Usually used a box of width 24/26 for setting crimson pivots in adobe
        self.hurtbox = Collision.hurtBox(self, "EHurtBox", pygame.Rect(self.posX, self.posY, 50, 100), 10)
        self.groundCheckBox = Collision.groundCheckBox(self, pygame.Rect(self.posX, self.posY, 25, 5))



        #load images
        self.sheetAtk1 = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetAtk1"])
        self.sheetAtk2 = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetAtk2"])
        self.sheetDeath = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetDeath"])
        self.sheetFall = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetFall"])
        self.sheetIdle = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetIdle"])
        self.sheetJump = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetJump"])
        self.sheetRun = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetRun"])
        self.sheetHit = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetHit"])
        self.sheetTeleport = pygame.image.load(self.jsonData["spriteSheetDirectory"]["spriteSheetTeleport"])



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
        self.teleportClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["teleportClips"].items()}
        

        self.stateToSpriteDict = {"runAround" : self.runClips, "atk1" : self.atk1Clips, "atk2" : self.atk2Clips, "death" : self.deathClips, "fall" : self.fallClips, "idle" : self.idleClips,
                                  "jump" : self.jumpClips, "hit" : self.hitClips, "teleport" : self.teleportClips}
        self.stateToSheetDict = {"runAround" : self.sheetRun, "atk1" : self.sheetAtk1, "atk2" : self.sheetAtk2, "death" : self.sheetDeath, "fall" : self.sheetFall, "idle": self.sheetIdle,
                                 "jump" : self.sheetJump, "hit" : self.sheetHit, "teleport" : self.sheetTeleport}
        
        self.stateToFunctionDict = {"idle": self.idleState,
                                    "runAround": self.runAroundState,
                                    "jump": self.jumpState,
                                    "atk1": self.atk1State,
                                    "atk2": self.atk2State,
                                    "fireball": self.fireballState,
                                    "hit" : self.hurtState,
                                    "death" : self.deathState,
                                    "teleport" : self.teleportState
                                   }
                                 
        

        for key in self.jsonData["animationData"].keys():
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
        self.moveEntity(4*self.direction, 0)
        

        if self.elapsedFramesInState >= MAXTIMEINPHASE:
            self.elapsedFramesInState = 0
            self.xVelocity = 0
            self.set_state("idle")





    def atk1State(self):
        #Move toward player, and then hit them when in range (60 units)

        if self.commitToAttack == False:
            distance = self.rect.centerx - self.playerRef.rect.centerx

            if (distance < 0):
                self.direction = 1
            if(distance > 0):
                self.direction = -1

            self.commitToAttack = True
            self.refToCurrentAttack = boss1Attacks.meleeAttack1(self)
            self.set_animation("atk1")
            self.xVelocity = 0
        else:
            if (self.refToCurrentAttack == None):
                self.elapsedFramesInState = 0
                self.commitToAttack = False
                self.set_state("idle")
                self.set_animation("idle", True)

            else:
                self.refToCurrentAttack.update()

    def atk2State(self):
        if self.refToCurrentAttack == None:
            distance = self.rect.centerx - self.playerRef.rect.centerx
            if (distance < 0):
                self.direction = 1
            if(distance >= 0):
                self.direction = -1

            self.refToCurrentAttack = boss1Attacks.meleeAttack2(self)
            self.set_animation("atk2")
        else:
            self.refToCurrentAttack.update()
            if (self.refToCurrentAttack == None):
                self.set_state("idle")
                self.set_animation("idle", True)
    
    def teleportState(self):
        VANISHTIMER = 120
        self.set_animation("teleport")
        self.hurtbox.disableHurtBox()

        if self.elapsedFramesInState > VANISHTIMER:
            self.hurtbox.enableHurtBox()
            self.direction *= -1


            self.moveEntityPosition(self.playerRef.posX - 150 * self.direction, self.posY)

            choice = random.randint(0,2)

            if choice == 2:
                self.set_state("atk2")
            else:
                self.set_state("atk1")
            self.resetAnimation("teleport")
            










    def fireballState(self):

        if(self.commitToAttack == False):
            self.refToCurrentAttack = boss1Attacks.Fireball("fireball1", None, self, None, self.direction)
            self.set_animation("fireball", True)
            self.commitToAttack = True
        else:
            if(self.refToCurrentAttack == None):
                self.set_state("idle")
                self.set_animation("idle", True)
                self.commitToAttack = False
            else:
                self.refToCurrentAttack.update()



    def attackEnded(self):
        del self.refToCurrentAttack
        self.refToCurrentAttack = None



    def jumpState(self, beginFall = False):
         if beginFall == True:
             self.elapsedFramesInState = 40


         if self.posX <= 15 and self.direction == -1 or self.posX >= 1200 and self.direction == 1:
            self.direction *= -1

         self.moveEntity(4 * self.direction, 0)
         if self.elapsedFramesInState >= 40:
             if self.isGrounded():
                 self.elapsedFramesInState = 0
                 self.set_state("atk2")
                 self.set_animation("atk2", True)
                 
             else:
                self.moveEntity(0, 3)
                self.set_animation("fall", False)
         else:
             self.moveEntity(0, -3)
             self.set_animation("jump", False)


    


    def idleState(self):
        IDLESTATETIME = 120
        self.set_animation("idle")
        
       

        if self.elapsedFramesInState >= IDLESTATETIME:

            choice = random.randint(0,4)
            
        
           
            if choice == 0:
                self.set_state("runAround")
                self.set_animation("runAround", True)
            elif choice == 1:
                self.set_state("atk1")
            elif choice == 2:
                self.set_state("fireball")
            elif choice == 3:
                self.set_state("jump")
            elif choice == 4:
                self.set_state("teleport")
                self.set_animation("teleport", True)
            


    def hurtState(self):
        hurtStateTime = 100

        self.xVelocity = 0

        if self.elapsedFramesInState > hurtStateTime:
            self.set_state("idle")
            self.set_animation("idle", True)
            self.priorityLastHitBy = -1
    
    
    
    def deathState(self):
        self.xVelocity = 0

       



        #Two Aspects of this Phase, Running Left and Right, and Jumping
    def handleCollision(self, CollisionType, Box):

        if CollisionType  == "PHitToEHurt":
            if self.refToCurrentAttack == None and self.state is not "hit":
                self.set_state("hit")
                self.set_animation("hit", True)

            if Box.priority > self.priorityLastHitBy:
                self.HP = self.HP - Box.damage
                self.priorityLastHitBy = Box.priority
                if self.HP <= 0:
                    self.set_state("death")
                    self.set_animation("death")
                
                


            




    def update(self):
        self.updateSprite()

        if self.isGrounded() == False and self.yVelocity>0:
            self.set_state("jump")
            self.jumpState(True)

        self.stateToFunctionDict[self.state]()



        self.elapsedFramesInState +=1

    #Start of State functions
