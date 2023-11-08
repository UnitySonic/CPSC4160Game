import pygame
from Scripts.Logic import gameLogicFunctions
from Scripts.Logic import Collision
from Scripts.Player import PlayerAttacks


class Player:

    def __init__(self, position):
        #load all spritesheets
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

        self.posX = position[0]
        self.posY = position[1]
        self.rect = pygame.Rect(self.posX, self.posY, 20, 32)
        self.hurtbox = Collision.hurtBox(self, "PHurtBox", self.rect, 0)
        self.HP = 100
        self.direction = 1
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
        self.jumpHeight = 15
        self.yVelocity = 15
        self.currentSprite = 0
        self.originalposY = self.posY
        self.dashCooldown = 1000
        self.timeDashPressed = 0

        self.state = "idle"

        self.image = self.idleSheet.subsurface(self.idleSheet.get_clip())
        self.rect = self.image.get_rect()

        self.rect.topleft = position

        self.frame = 0
        self.animationTime = 0


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
                                     3: (13,209,22,27),
                                     4: (13,153,23,32),
                                     5: (17,298,19,37),
                                     6: (17,344,19,39),
                                     7: (19,402,19,30),
                                     8: (18,451,19,29),
                                     9: (18,498,18,30),
                                     10: (20,546,16,30)
                                    }
        
        self.fallforwardStates =    {0: (13,153,23,32),
                                     1: (17,298,19,37),
                                     2: (17,344,19,39),
                                     3: (19,402,19,30),
                                     4: (18,451,19,29)
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

        self.currentFrameWidth = 0
        self.currentFrameHeight = 0

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
    
    def updateSprite(self, stateToUse):

        self.clip(self.stateToSpriteDict[stateToUse], stateToUse)
        if self.direction == -1:
            self.image = pygame.transform.flip(self.stateToSheetDict[stateToUse].subsurface(self.stateToSheetDict[stateToUse].get_clip()), True, False)
        else:
            self.image = self.stateToSheetDict[stateToUse].subsurface(self.stateToSheetDict[stateToUse].get_clip())
        #Scaling
        scaledX = int(self.rect.width * self.scaleFactor)
        scaledY = int(self.rect.height * self.scaleFactor)
        self.image = pygame.transform.scale(self.image, (scaledX,scaledY))

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
            if not self.jumping or not self.falling:
                if self.rightPressed and not self.leftPressed:
                    self.set_state("run")
                elif self.leftPressed and not self.rightPressed:
                    self.set_state("run")
                elif self.leftPressed and self.rightPressed:
                    self.set_state("idle")
                elif not self.leftPressed and not self.rightPressed:
                    self.set_state("idle")

            #jumping
            if event.key == pygame.K_z:
                self.jumpPressed = False
            if not self.jumpPressed:
                self.falling = True
                if self.rightPressed and not self.leftPressed:
                    self.set_state("fallForward")
                elif not self.rightPressed and self.leftPressed:
                    self.set_state("fallForward")
                elif not self.rightPressed and not self.leftPressed:
                    self.set_state("fallNeutral")
                elif self.rightPressed and self.leftPressed:
                    self.set_state("fallNeutral")
            if self.jumpPressed:
                self.falling = True
                if self.rightPressed and not self.leftPressed:
                    self.set_state("jumpForward")
                elif not self.rightPressed and self.leftPressed:
                    self.set_state("jumpForward")
                elif not self.rightPressed and not self.leftPressed:
                    self.set_state("jumpNeutral")
                elif self.rightPressed and self.leftPressed:
                    self.set_state("jumpNeutral")
        
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
            if self.rightPressed and not self.leftPressed:
                self.set_state("run")
            elif self.leftPressed and not self.rightPressed:
                self.set_state("run")
            elif self.leftPressed and self.rightPressed:
                self.set_state("idle")
            elif not self.leftPressed and not self.rightPressed:
                self.set_state("idle")
            
            #jumping
            if self.jumpPressed:
                if self.rightPressed and not self.leftPressed:
                    self.jumping = True
                    self.set_state("jumpForward")
                elif not self.rightPressed and self.leftPressed:
                    self.jumping = True
                    self.set_state("jumpForward")
                elif not self.rightPressed and not self.leftPressed:
                    self.jumping = True
                    self.set_state("jumpNeutral")
                elif self.rightPressed and self.leftPressed:
                    self.set_state("jumpNeutral")
            if self.falling:
                if self.rightPressed and not self.leftPressed:
                    self.set_state("fallForward")
                elif not self.rightPressed and self.leftPressed:
                    self.set_state("fallForward")
                elif not self.rightPressed and not self.leftPressed:
                    self.set_state("fallNeutral")
                elif self.rightPressed and self.leftPressed:
                    self.set_state("fallNeutral")
                    
            if self.dashPressed:
                now = pygame.time.get_ticks()
                if now - self.timeDashPressed >= self.dashCooldown:
                    self.set_state("dash")
            
            
            
    def update(self):
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.hurtbox.update()

        if self.state == "idle":
            self.idleState()
        elif self.state == "run":
            self.runState()
        elif self.state == "jumpNeutral":
            self.jumpNeutralState()
        elif self.state == "fallNeutral":
            self.fallNeutralState()
        elif self.state == "jumpForward":
            self.jumpForwardState()
        elif self.state == "fallForward":
            self.fallForwardState()
        elif self.state == "dash":
            self.fallForwardState()

        if self.state == "atk1":
            if self.commitedToAttack != True:
                self.refToCurrentAttack = PlayerAttacks.meleeAttack1(self)
                self.commitedToAttack = True
        if self.commitedToAttack == True:
                self.refToCurrentAttack.update()

    def isGrounded(self):
        collide = pygame.sprite.spritecollide(self.hurtbox, gameLogicFunctions.collisionGroup, False)
        if collide:
            return True
        else:
            return False

    def idleState(self):
        self.updateSprite("idle")

    def runState(self):
        if self.leftPressed:
            self.direction = -1
            self.posX += 5 * self.direction
        elif self.rightPressed:
            self.direction = 1
            self.posX += 5 * self.direction
        self.updateSprite("run")

    def jumpNeutralState(self):
        if self.jumping:
            self.updateSprite("jumpNeutral")
            self.posY -= self.yVelocity
            self.yVelocity -= self.yGravity
            if self.yVelocity < 0:
                self.falling = True
                self.set_state("fallNeutral")
            if self.yVelocity < -self.jumpHeight:
                self.jumping = False
                self.yVelocity = self.jumpHeight
                self.set_state("idle")
                self.idleState()
                
    def fallNeutralState(self):
        if not self.posY == self.originalposY:
            self.updateSprite("fallNeutral")
            self.yVelocity += self.yGravity
            self.posY += self.yVelocity
        if self.posY == self.originalposY:
            self.jumping = False
            self.falling = False
            self.yVelocity = self.jumpHeight
            self.set_state("idle")
            self.idleState()
            
    def jumpForwardState(self):
        if self.jumping:
            self.updateSprite("jumpForward")
            self.posY -= self.yVelocity
            self.yVelocity -= self.yGravity
            if self.leftPressed:
                self.direction = -1
                self.posX += 5 * self.direction
            elif self.rightPressed:
                self.direction = 1
                self.posX += 5 * self.direction
            if self.yVelocity < 0:
                self.falling = True
                self.set_state("fallForward")
            if self.yVelocity < -self.jumpHeight:
                self.jumping = False
                self.yVelocity = self.jumpHeight
                self.set_state("run")
                self.runState()
                
    def fallForwardState(self):
        if not self.posY == self.originalposY:
            self.updateSprite("fallForward")
            self.yVelocity += self.yGravity
            self.posY += self.yVelocity
            if self.leftPressed:
                self.direction = -1
                self.posX += 5 * self.direction
            elif self.rightPressed:
                self.direction = 1
                self.posX += 5 * self.direction
        if self.posY == self.originalposY:
            self.jumping = False
            self.falling = False
            self.yVelocity = self.jumpHeight
            self.set_state("run")
            self.runState()
            
    def dashState(self):
        self.posX += 15 * self.direction
        self.updateSprite("dash")
        