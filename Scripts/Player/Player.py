import pygame
from Scripts.Logic import gameLogicFunctions
from Scripts.Logic import Collision
from Scripts.Player import PlayerAttacks
from Scripts import Entity


class Player(Entity.Entity):

    def __init__(self, position):
        #load all spritesheets

        super().__init__(position)


        self.idleSheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Idle/Battlemage Idle.png")
        self.runSheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Running/Battlemage Run.png")
        self.jumpNeutralSheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Jump Neutral/Battlemage Jump Neutral.png")
        self.fallNeutralSheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Jump Neutral/Battlemage Jump Neutral.png")
        self.jumpForwardSheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Jump Foward/Battlemage Jump Foward.png")
        self.fallForwardSheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Jump Foward/Battlemage Jump Foward.png")
        self.crouchSheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Crouch/Battlemage Crouch.png")
        self.dashSheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Dash/Battlemage Dash.png")
        self.attack1Sheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Attack 1/Battlemage Attack 1.png")
        self.attack2Sheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Attack 2/Battlemage Attack 2.png")
        self.attack3Sheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Attack 3/Battlemage Attack 3.png")
        self.crouchAttackSheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Crouch Attack/Crouch Attack.png")
        self.jumpAttackSheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Jump Attack/Jump Foward Attack.png")
        self.magic1Sheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Fast Magic/Battlemage Fast magic.png")
        self.magic2Sheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Sustain Magic/Battlemage Sustain Magic.png")
        self.magic3Sheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Spin Attack/Battlemage Spin Attack.png")
        self.deathSheet = pygame.image.load("Assets/Player/Battlemage Complete (Sprite Sheet)/Death/Battlemage Death.png")


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

        self.ForwardAirborneSet = ["jumpForward", "fallForward"]
        self.NeutralAirborneSet = ["jumpNeutral", "fallNeutral"]

        self.refToAirborneSet = None

        self.image = self.idleSheet.subsurface(self.idleSheet.get_clip())
        self.rect = self.image.get_rect()

        self.rect.topleft = position




        #states
        self.idleStates =   {0: (20,19,17,29),
                             1: (20,67,16,29),
                             2: (20,115,16,29),
                             3: (19,161,17,31),
                             4: (18,209,19,31),
                             5: (18,257,18,31),
                             6: (19,305,17,31),
                             7: (18,355,18,29)
                            }

        self.runStates =    {0: (19,19,17,29),
                             1: (18,66,18,30),
                             2: (16,113,21,31),
                             3: (15,161,23,31),
                             4: (14,211,26,29),
                             5: (16,259,21,29),
                             6: (16,306,20,30),
                             7: (16,353,20,31),
                             8: (16,401,20,31),
                             9: (18,451,18,29)
                            }

        self.jumpNeutralStates =    {0: (20,161,14,31),
                                     1: (20,211,14,29),
                                     2: (20,259,14,29),
                                     3: (18,307,17,28),
                                     4: (16,350,19,32),
                                     5: (17,395,18,36),
                                     6: (16,449,19,31),
                                     7: (16,499,18,29)
                                    }

        self.fallNeutralStates =    {0: (16,350,19,32),
                                     1: (17,395,18,36),
                                     2: (16,449,19,31),
                                     3: (16,499,18,29)
                                    }

        self.jumpForwardStates =    {0: (20,65,15,30),
                                     1: (17,114,20,29),
                                     2: (16,162,16,26),
                                     3: (13,153,23,32),
                                     4: (13,209,22,27),
                                     5: (17,298,19,37),
                                     6: (17,344,19,39),
                                     7: (19,402,19,30),
                                     8: (18,451,19,29),
                                     9: (18,498,18,30),
                                     10: (20,546,16,30)
                                    }

        self.fallforwardStates =    {0: (13,153,23,32),
                                     1: (17,298,19,37),
                                     #2: (17,344,19,39),
                                     2: (19,402,19,30),
                                     3: (18,451,19,29)
                                    }

        self.dashStates =           {0: (17,21,29,27),
                                     1: (17,67,29,29),
                                     2: (17,115,29,29),
                                     3: (17,164,29,28)
                                    }

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
        self.elapsedFramesInPhase += 1
        self.stateToFunctionDict[self.state]()

        if self.state == "atk1":
            if self.commitedToAttack != True:
                self.refToCurrentAttack = PlayerAttacks.meleeAttack1(self)
                self.commitedToAttack = True
        if self.commitedToAttack == True:
                self.refToCurrentAttack.update()


    def idleState(self):
        self.updateSprite("idle")

        if self.jumpPressed:

            self.isJumping = True
            self.set_state("air")
            if self.leftPressed or self.rightPressed:
                self.refToAirborneSet = self.ForwardAirborneSet
            else:
                self.refToAirborneSet = self.NeutralAirborneSet

        if self.leftPressed or self.rightPressed:
            self.set_state("run")

    def isGrounded(self):
        collide = pygame.sprite.spritecollide(self.hurtbox, gameLogicFunctions.collisionGroup, False)
        if collide:
            return True
        else:
            return False



    def continueGravity(self):
        maxJumpingFrames = 30

        if self.isJumping == True:
            self.updateSprite(self.refToAirborneSet[0])
            self.yVelocity = self.jumpHeight

            if self.jumpPressed == False:
                self.yVelocity = 0
                self.isJumping = False
                self.updateSprite(self.refToAirborneSet[1], True)

            if self.elapsedFramesInPhase < maxJumpingFrames:
                self.posY -= self.yVelocity
            elif self.elapsedFramesInPhase >= maxJumpingFrames:
                self.isJumping = False
                self.updateSprite(self.refToAirborneSet[1], True)

        else:
            self.updateSprite(self.refToAirborneSet[1])
            self.posY -= self.yVelocity
            self.yVelocity -= self.yGravity

            if self.isGrounded():
                return False
        return True



    def airBorneState(self):
        if self.continueGravity() == False:
            self.jumpPressed = False
            self.set_state("idle")
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
        self.updateSprite("run")
        if self.jumpPressed:
            self.isJumping = True
            self.set_state("air")
            if self.leftPressed or self.rightPressed:
                self.refToAirborneSet = self.ForwardAirborneSet
            else:
                self.refToAirborneSet = self.NeutralAirborneSet

    def dashState(self):
        self.posX += 15 * self.direction
        self.updateSprite("dash")
