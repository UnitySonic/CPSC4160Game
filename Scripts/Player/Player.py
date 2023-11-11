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
        self.jumpForwardSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["jumpForwardSheet"])
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


        #In adobe, I used a bounding box of width 10 to help set pivot points for Cyline
        self.hurtbox = Collision.hurtBox(self, "PHurtBox", pygame.Rect(self.posX, self.posY, 40, 70), 10)
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
        self.airDashPhysicsOn = False




        self.currentSprite = 0
        self.originalposY = self.posY
        self.dashCooldown = 1000
        self.timeDashPressed = 0
        self.isJumping = False

        self.state = "idle"
        self.animation = "idle"

        self.ForwardAirborneSet = ["jumpForwardUp", "jumpForwardDown", "jumpForwardTransition"]
        self.NeutralAirborneSet = ["jumpNeutralUp", "jumpNeutralDown", "jumpNeutralTransition"]

        self.refToAirborneSet = None

        self.image = self.idleSheet.subsurface(self.idleSheet.get_clip())
        self.rect = self.image.get_rect()

        self.rect.topleft = position

        


        #states
        self.idleClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["idleClips"].items()}
        self.runClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["runClips"].items()}
        self.jumpNeutralClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["jumpNeutralClips"].items()}
        self.jumpForwardClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["jumpForwardClips"].items()}
        self.dashClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["dashClips"].items()}


        self.stateToSpriteDict =  {"idle": self.idleClips,
                                   "run": self.runClips,
                                   "jumpNeutral": self.jumpNeutralClips,
                                   "jumpForward": self.jumpForwardClips,
                                   "dash": self.dashClips
                                  }
        self.stateToSheetDict =   {"idle": self.idleSheet,
                                   "run": self.runSheet,
                                   "jumpNeutral": self.jumpNeutralSheet,
                                   "jumpForward": self.jumpForwardSheet,
                                   "dash": self.dashSheet
                                  }
        self.stateToFunctionDict = {"idle": self.idleState,
                                    "run": self.runState,
                                    "air": self.airBorneState,
                                    "dash" : self.dashState
                                   }




        for key in self.jsonData["animationData"].keys():
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
        
        self.elapsedFramesInState += 1
        
        self.stateToFunctionDict[self.state]()
        self.updateSprite()
        self.hurtbox.update()

        if self.state == "atk1":
            if self.commitedToAttack != True:
                self.refToCurrentAttack = PlayerAttacks.meleeAttack1(self)
                self.commitedToAttack = True
        if self.commitedToAttack == True:
                self.refToCurrentAttack.update()


    def idleState(self):
        if not self.transitionActive:
            self.set_animation("idle")


        
        if self.dashPressed:
            self.set_state("dash")
            self.set_animation("dash", True)

        elif self.jumpPressed:

            self.isJumping = True
            self.set_state("air")
            if self.leftPressed or self.rightPressed:
                self.refToAirborneSet = self.ForwardAirborneSet
            else:
                self.refToAirborneSet = self.NeutralAirborneSet
            self.set_animation(self.refToAirborneSet[0])

        elif self.leftPressed or self.rightPressed:
            self.set_state("run")
            self.set_animation("run", True)

    def isGrounded(self):
        collide = pygame.sprite.spritecollide(self.hurtbox, gameLogicFunctions.collisionGroup, False)
        if collide:
            return True
        else:
            return False



    def continueGravity(self):
        maxJumpingFrames = 30
    

        if self.isJumping == True:
            self.set_animation(self.refToAirborneSet[0])

            self.yVelocity = self.jumpHeight

            if self.jumpPressed == False:
                self.yVelocity = 0
                self.isJumping = False
                self.set_animation(self.refToAirborneSet[1], True)

            if self.elapsedFramesInState < maxJumpingFrames:
                self.posY -= self.yVelocity
            elif self.elapsedFramesInState >= maxJumpingFrames:
                self.isJumping = False
                self.set_animation(self.refToAirborneSet[1], True)

        else:

            self.posY -= self.yVelocity
            self.yVelocity -= self.yGravity

            if self.isGrounded():
                self.set_animation(self.refToAirborneSet[2], True)
                return False
        return True



    def airBorneState(self):
        if self.continueGravity() == False:
            self.jumpPressed = False
            self.set_state("idle")
            self.airDashPhysicsOn = False
            self.dashPressed = False

        airSpeed = 5 if self.airDashPhysicsOn == False else 10
        
        
        
        if self.leftPressed:
            self.direction = -1
            self.posX += airSpeed * self.direction
        elif self.rightPressed:
            self.direction = 1
            self.posX += airSpeed * self.direction




    def runState(self):


        #Moving left and Right
        if self.leftPressed:
            self.direction = -1
            self.posX += 5 * self.direction
        elif self.rightPressed:
            self.direction = 1
            self.posX += 5 * self.direction
        else:
            self.set_state("idle")
            self.set_animation("idle",True)
        

        if self.dashPressed:
            self.set_state("dash")
            self.set_animation("dash", True)
            
        elif self.jumpPressed:
            self.isJumping = True
            self.set_state("air")
            if self.leftPressed or self.rightPressed:
                self.refToAirborneSet = self.ForwardAirborneSet
            else:
                self.refToAirborneSet = self.NeutralAirborneSet
            self.set_animation(self.refToAirborneSet[0])

    def dashState(self):
        dashDuration = 40

        if self.elapsedFramesInState > dashDuration:
            self.set_animation("dashTransition", True)
            self.set_state("idle")
            self.dashPressed = False
            return
        

        if self.leftPressed:
            self.direction = -1
        elif self.rightPressed:
            self.direction = 1 
        
        
        self.posX += 10 * self.direction
        self.set_animation("dash")


        if self.jumpPressed:
            self.airDashPhysicsOn = True
            self.refToAirborneSet = self.ForwardAirborneSet
            self.set_state("air")
            self.set_animation(self.refToAirborneSet[1])
            self.isJumping = True
