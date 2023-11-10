import pygame
from Scripts.Logic import gameLogicFunctions
from Scripts.Logic import Collision
from Scripts.Player import PlayerAttacks
from Scripts import Entity
import json


class Player(Entity.Entity):

    def __init__(self, position):
        #load all spritesheets

        super().__init__(position)

        directory = "Scripts/Player/playerData.json"

        with open(directory, "r") as file:
            self.jsonData = json.load(file)




        self.idleSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["idleSheet"])
        self.runSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["runSheet"])
        self.jumpNeutralSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["jumpNeutralSheet"])
        self.fallNeutralSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["fallNeutralSheet"])
        self.jumpForwardSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["jumpForwardSheet"])
        self.fallForwardSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["fallForwardSheet"])
        self.crouchSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["crouchSheet"])
        self.dashSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["dashSheet"])
        self.attack1Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["attack1Sheet"])
        self.attack2Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["attack2Sheet"])
        self.attack3Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["attack3Sheet"])
        self.crouchAttackSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["crouchAttackSheet"])
        self.jumpAttackSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["jumpAttackSheet"])
        self.magic1Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["magic1Sheet"])
        self.magic2Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["magic2Sheet"])
        self.magic3Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["magic3Sheet"])
        self.deathSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["deathSheet"])


        self.rect = pygame.Rect(self.posX, self.posY, 20, 32)
        self.hurtbox = Collision.hurtBox(self, "PHurtBox", self.rect, 0)
        self.HP = 100


        self.refToCurrentAttack = None
        self.leftPressed = False
        self.rightPressed = False
        self.jumpPressed = False
        self.dashPressed = False
        self.commitedToAttack = False
        self.jumping = False
        self.falling = False
        self.scaleFactor = 2.5
        self.yGravity = 1
        self.jumpHeight = 8
        self.yVelocity = 15
        self.currentSprite = 0
        self.originalposY = self.posY
        self.dashCooldown = 1000
        self.timeDashPressed = 0
        self.isJumping = False

        self.state = "idle"
        self.animation = "idle"

        self.ForwardAirborneSet = ["jumpForward", "fallForward"]
        self.NeutralAirborneSet = ["jumpNeutral", "fallNeutral"]

        self.refToAirborneSet = None

        self.image = self.idleSheet.subsurface(self.idleSheet.get_clip())
        self.rect = self.image.get_rect()

        self.rect.topleft = position


        #states
        self.idleStates = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["idleStates"].items()}
        self.runStates = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["runStates"].items()}
        self.jumpNeutralStates = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["jumpNeutralStates"].items()}
        self.fallNeutralStates = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["fallNeutralStates"].items()}
        self.jumpForwardStates = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["jumpForwardStates"].items()}
        self.fallforwardStates = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["fallForwardStates"].items()}
        self.dashStates = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["dashStates"].items()}


        self.stateToSpriteDict =  {"idle": self.idleStates,
                                   "run": self.runStates,
                                   "jumpNeutral": self.jumpNeutralStates,
                                   "jumpForward": self.jumpForwardStates,
                                   "fallNeutral": self.fallNeutralStates,
                                   "fallForward": self.fallforwardStates,
                                   "dash": self.dashStates
                                  }
        self.stateToSheetDict =   {"idle": self.idleSheet,
                                   "run": self.runSheet,
                                   "jumpNeutral": self.jumpNeutralSheet,
                                   "jumpForward": self.jumpForwardSheet,
                                   "fallNeutral": self.fallNeutralSheet,
                                   "fallForward": self.fallForwardSheet,
                                   "dash": self.dashSheet
                                  }
        self.stateToFunctionDict = {"idle": self.idleState,
                                    "run": self.runState,
                                    "air": self.airBorneState
                                   }




        for key in self.stateToSpriteDict.keys():
            self.animationDict[key] = {
                "frame" : 0,
                "animationTime": 0,
                "transition" : False
            }








    def attackEnded(self):
        self.refToCurrentAttack = None
        self.commitedToAttack = False

    def handleCollision(self, CollisionType, Box):
        if CollisionType == "PHurtToEHit":

            self.HP - Box.damage

        elif CollisionType == "PHurtToEHurt":
            self.HP - Box.damage

    def handle_event(self, event):

        if event.type == pygame.KEYUP:
            #movement
            if event.key == pygame.K_LEFT:
                self.leftPressed = False
            elif event.key == pygame.K_RIGHT:
                self.rightPressed = False

            #jumping
            if event.key == pygame.K_z:

                self.jumpPressed = False
            if not self.jumpPressed:
                self.falling = True



        if event.type == pygame.KEYDOWN:

            pressed = pygame.key.get_pressed()

            #movement
            if pressed[pygame.K_LEFT]:
                self.leftPressed = True
            if pressed[pygame.K_RIGHT]:
                self.rightPressed = True
            if pressed[pygame.K_z]:

                self.jumpPressed = True
            if pressed[pygame.K_c]:
                self.dashPressed = True
                self.timeDashPressed = pygame.time.get_ticks()



    def update(self):
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.hurtbox.update()
        self.elapsedFramesInState += 1
        self.stateToFunctionDict[self.state]()
        self.updateSprite()

        if self.state == "atk1":
            if self.commitedToAttack != True:
                self.refToCurrentAttack = PlayerAttacks.meleeAttack1(self)
                self.commitedToAttack = True
        if self.commitedToAttack == True:
                self.refToCurrentAttack.update()


    def idleState(self):
        #self.updateSprite()

        if self.jumpPressed:

            self.isJumping = True
            self.set_state("air")
            if self.leftPressed or self.rightPressed:
                self.refToAirborneSet = self.ForwardAirborneSet
            else:
                self.refToAirborneSet = self.NeutralAirborneSet
            self.set_animation(self.refToAirborneSet[0])

        if self.leftPressed or self.rightPressed:
            self.set_state("run")
            self.set_animation("run")

    def isGrounded(self):
        collide = pygame.sprite.spritecollide(self.hurtbox, gameLogicFunctions.collisionGroup, False)
        if collide:
            return True
        else:
            return False



    def continueGravity(self):
        maxJumpingFrames = 30

        if self.isJumping == True:

            self.yVelocity = self.jumpHeight

            if self.jumpPressed == False:
                self.yVelocity = 0
                self.isJumping = False
                self.set_animation(self.refToAirborneSet[1])

            if self.elapsedFramesInState < maxJumpingFrames:
                self.posY -= self.yVelocity
            elif self.elapsedFramesInState >= maxJumpingFrames:
                self.isJumping = False
                self.set_animation(self.refToAirborneSet[1])

        else:

            self.posY -= self.yVelocity
            self.yVelocity -= self.yGravity

            if self.isGrounded():
                return False
        return True



    def airBorneState(self):
        if self.continueGravity() == False:
            self.jumpPressed = False
            self.set_state("idle")
            self.set_animation('idle')
        if self.leftPressed:
            self.direction = -1
            self.posX += 5 * self.direction
        elif self.rightPressed:
            self.direction = 1
            self.posX += 5 * self.direction




    def runState(self):
        if self.leftPressed:
            self.direction = -1
            self.posX += 5 * self.direction
        elif self.rightPressed:
            self.direction = 1
            self.posX += 5 * self.direction
        else:
            self.set_state("idle")
            self.set_animation("idle")

        if self.jumpPressed:
            self.isJumping = True
            self.set_state("air")
            if self.leftPressed or self.rightPressed:
                self.refToAirborneSet = self.ForwardAirborneSet
            else:
                self.refToAirborneSet = self.NeutralAirborneSet
            self.set_animation(self.refToAirborneSet[0])

    def dashState(self):
        self.posX += 15 * self.direction
        self.updateSprite("dash")
