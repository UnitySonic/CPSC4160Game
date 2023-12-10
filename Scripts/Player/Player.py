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
        self.atk1Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["attack1Sheet"])
        self.atk2Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["attack2Sheet"])
        self.atk3Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["attack3Sheet"])
        self.crouchAttackSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["crouchAttackSheet"])
        self.airAttackSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["airAttackSheet"])
        self.magic1Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["magic1Sheet"])
        self.magic2Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["magic2Sheet"])
        self.magic3Sheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["magic3Sheet"])
        self.deathSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["deathSheet"])
        self.hitBackSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["hitBackSheet"])
        self.hitForwardSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["hitForwardSheet"])
        self.hitForwardSheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["hitForwardSheet"])
        self.victorySheet = pygame.image.load(self.jsonData["spriteSheetDirectory"]["victorySheet"])


        self.rect = pygame.Rect(self.posX, self.posY, 20, 32)


        #In adobe, I used a bounding box of width 10 to help set pivot points for Cyline
        self.hurtbox = Collision.hurtBox(self, "PHurtBox", pygame.Rect(self.posX, self.posY, 40, 70), 0)
        self.groundCheckBox = Collision.groundCheckBox(self,pygame.Rect(self.posX, self.posY, 20, 1))
        self.HP = 100


        self.refToCurrentAttack = None
        self.leftPressed = False
        self.rightPressed = False
        self.crouchPressed = False
        self.jumpPressed = False
        self.dashPressed = False
        self.attackPressed = False


        self.commitedToAttack = False
        self.jumping = False
        self.falling = False
        self.scaleFactor = 2.5
        self.yGravity = 1
        self.jumpHeight = 9
        
        self.yVelocity = 0
        self.airDashPhysicsOn = False
        self.invinFrames = 0

        




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

        self.atk1Clips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["atk1Clips"].items()}
        self.atk2Clips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["atk2Clips"].items()}
        self.atk3Clips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["atk3Clips"].items()}
        self.airAtkClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["airAtkClips"].items()}
        
        self.crouchClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["crouchClips"].items()}
        self.crouchAtkClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["crouchAtkClips"].items()}
        self.hitBackClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["hitBackClips"].items()}
        self.hitForwardClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["hitForwardClips"].items()}
        self.deathClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["deathClips"].items()}
        self.victoryClips = {int(key): value for key, value in self.jsonData["spriteSheetClips"]["victoryClips"].items()}


        self.stateToSpriteDict =  {"idle": self.idleClips,
                                   "run": self.runClips,
                                   "jumpNeutral": self.jumpNeutralClips,
                                   "jumpForward": self.jumpForwardClips,
                                   "dash": self.dashClips,
                                   "atk1" : self.atk1Clips,
                                   "atk2" : self.atk2Clips,
                                   "atk3" : self.atk3Clips,
                                   "airAtk" : self.airAtkClips,
                                   "crouch" : self.crouchClips,
                                   "crouchAtk" : self.crouchAtkClips,
                                   "death" : self.deathClips,
                                   "hitBack" : self.hitBackClips,
                                   "hitForward": self.hitForwardClips,
                                   "victory" : self.victoryClips
                                  }
        self.stateToSheetDict =   {"idle": self.idleSheet,
                                   "run": self.runSheet,
                                   "jumpNeutral": self.jumpNeutralSheet,
                                   "jumpForward": self.jumpForwardSheet,
                                   "dash": self.dashSheet,
                                   "atk1" : self.atk1Sheet,
                                   "atk2" : self.atk2Sheet,
                                   "atk3" : self.atk3Sheet,
                                   "crouch" : self.crouchSheet,
                                   "crouchAtk" : self.crouchAttackSheet,
                                   "airAtk" : self.airAttackSheet,
                                   "hitBack": self.hitBackSheet,
                                   "hitForward": self.hitForwardSheet,
                                   "death" : self.deathSheet,
                                   "victory" : self.victorySheet
                                  }
        self.stateToFunctionDict = {"idle": self.idleState,
                                    "run": self.runState,
                                    "air": self.airBorneState,
                                    "dash" : self.dashState,
                                    "groundatk" : self.groundAttackState,
                                    "crouch" : self.crouchState,
                                    "death" : self.deathState,
                                    "hurt" : self.hurtState,
                                    "victory" : self.victoryState

                                   }




        for key in self.jsonData["animationData"].keys():
            self.animationDict[key] = {
                "frame" : 0,
                "animationTime": 0,
                "transition" : False
            }





    def set_state(self, new_state):

        if new_state == "air":
            pygame.mixer.Sound('Assets/Sounds/p_jump.wav')

        self.state = new_state
        self.elapsedFramesInState = 0



    def handleCollision(self, CollisionType, Box):
        if CollisionType == "PHurtToEHit" or CollisionType == "PHurtToEHurt":
            if self.invinFrames <= 0:
                self.invinFrames = 40
                
                self.HP -= Box.damage
                if self.HP <= 0:
                    self.set_state("death")
                else:
                    self.set_state("hurt")
                    sound = pygame.mixer.Sound("Assets/Sounds/p_hurt.wav")
                    sound.play()
                    
                
                if self.refToCurrentAttack is not None:
                    self.refToCurrentAttack.clear()
                    self.refToCurrentAttack = None


                posXToCheck = None
                if Box.getEntity() == None:
                    posXToCheck = Box.rect.centerx
                else:
                    posXToCheck = Box.getEntity().posX


                if self.posX < posXToCheck:
                    if self.direction == 1:
                        self.set_animation("hitBack", True)
                    else:
                        self.set_animation("hitForward", True)
                else:
                    if self.direction == 1:
                        self.set_animation("hitForward", True)
                    else:
                        self.set_animation("hitBack", True)
                    



    def handle_event(self, event):

        if event.type == pygame.KEYUP:
            #movement
            if event.key == pygame.K_LEFT:
                self.leftPressed = False
            elif event.key == pygame.K_RIGHT:
                self.rightPressed = False
            
            if event.key == pygame.K_DOWN:
                self.crouchPressed = False

            #jumping
            if event.key == pygame.K_z:
                self.jumpPressed = False
            if event.key == pygame.K_c:
                self.dashPressed = False
            if event.key == pygame.K_x:
                self.attackPressed = False



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
            if pressed[pygame.K_x]:
                self.attackPressed = True
            if pressed[pygame.K_DOWN]:
                self.crouchPressed = True


    def update(self):
        self.rect.x = self.posX
        self.rect.y = self.posY
        
        self.elapsedFramesInState += 1

        if self.invinFrames > 0:
            self.invinFrames -= 1
        
        


        self.stateToFunctionDict[self.state]()

        
        self.updateSprite()
        self.hurtbox.update()
        self.groundCheckBox.update()

      


  
    
    
        
    

    def attackEnded(self):
        del self.refToCurrentAttack
        self.refToCurrentAttack = None



    def continueGravity(self):
        maxJumpingFrames = 15
    

        if self.isJumping == True:
            if self.refToCurrentAttack == None:
                self.set_animation(self.refToAirborneSet[0])

            self.yVelocity = self.jumpHeight

            if self.jumpPressed == False:
                self.yVelocity = 0
                self.isJumping = False

                if self.refToCurrentAttack == None:
                    self.set_animation(self.refToAirborneSet[1], True)

            if self.elapsedFramesInState < maxJumpingFrames:
                self.posY -= self.yVelocity
            elif self.elapsedFramesInState >= maxJumpingFrames:
                self.isJumping = False
                if self.refToCurrentAttack == None:
                    self.set_animation(self.refToAirborneSet[1], True)

        else:

            self.posY -= self.yVelocity
            self.yVelocity -= self.yGravity

            if self.isGrounded():
                print("grounded")
                self.set_animation(self.refToAirborneSet[2], True)
                return False
        return True



    def airBorneState(self):
        if self.continueGravity() == False:
            self.jumpPressed = False
            self.resetAllAnimation()
            
            if self.refToCurrentAttack is not None:
                self.refToCurrentAttack.clear()
                self.refToCurrentAttack = None

            self.set_state("idle")
            self.airDashPhysicsOn = False
            self.dashPressed = False
            return

        airSpeed = 5 if self.airDashPhysicsOn == False else 10
        
        
        
        if self.leftPressed:
            self.direction = -1
            self.posX += airSpeed * self.direction
        elif self.rightPressed:
            self.direction = 1
            self.posX += airSpeed * self.direction
        
        if self.refToCurrentAttack == None:
            if self.attackPressed:
                self.set_animation("airAtk")
                self.refToCurrentAttack = PlayerAttacks.airAttack(self)
                self.refToAirborneSet = self.ForwardAirborneSet
                self.attackPressed = False
        else:
            self.refToCurrentAttack.update()
            if self.refToCurrentAttack == None:
                self.resetAllAnimation()
                self.animationDict["jumpForwardDown"]["frame"] = 4
                self.set_animation("jumpForwardDown")

        




    def idleState(self):
        if not self.transitionActive:
            self.set_animation("idle")


        
        if self.dashPressed:
            self.set_state("dash")
            self.set_animation("dash", True)
            pygame.mixer.Sound('Assets/Sounds/p_dash.wav').play()
        
        elif self.attackPressed:
            self.set_state("groundatk")
            self.set_animation("atk1", True)
            self.refToCurrentAttack = PlayerAttacks.meleeAttack1(self)
            self.attackPressed = False

        elif self.jumpPressed:

            self.isJumping = True
            self.set_state("air")
            if self.leftPressed or self.rightPressed:
                self.refToAirborneSet = self.ForwardAirborneSet
            else:
                self.refToAirborneSet = self.NeutralAirborneSet
            self.set_animation(self.refToAirborneSet[0])
        
        elif self.crouchPressed:
            self.set_state("crouch")
            self.set_animation("crouch", True)

        elif self.leftPressed or self.rightPressed:
            self.set_state("run")
            self.set_animation("run", True)

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
            pygame.mixer.Sound('Assets/Sounds/p_dash.wav').play()
            
        elif self.jumpPressed:
            self.isJumping = True
            self.set_state("air")
            if self.leftPressed or self.rightPressed:
                self.refToAirborneSet = self.ForwardAirborneSet
            else:
                self.refToAirborneSet = self.NeutralAirborneSet
            self.set_animation(self.refToAirborneSet[0])
        elif self.crouchPressed:
            self.set_state("crouch")
            self.set_animation("crouch", True)

    def dashState(self):
        dashDuration = 40

        if self.elapsedFramesInState > dashDuration or not self.dashPressed:
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
    
    def crouchState(self):    

        #In, Or Not in Attack

        if self.refToCurrentAttack == None:
            self.set_animation("crouch")
            if self.rightPressed:
                self.direction = 1
            elif self.leftPressed:
                self.direction = -1

            if self.jumpPressed:
                self.isJumping = True
                self.set_state("air")
                if self.leftPressed or self.rightPressed:
                    self.refToAirborneSet = self.ForwardAirborneSet
                else:
                    self.refToAirborneSet = self.NeutralAirborneSet
                self.set_animation(self.refToAirborneSet[0], True)
            elif self.attackPressed:
                self.set_animation("crouchAtk")
                self.refToCurrentAttack = PlayerAttacks.crouchAttack(self)
                self.attackPressed = False
            elif self.crouchPressed == False:
                self.set_animation("idle", True)
                self.set_state("idle")

        
        else:
            self.refToCurrentAttack.update()
            if self.refToCurrentAttack == None:
                self.set_animation("crouch", True)

            


    def groundAttackState(self):
        
        self.refToCurrentAttack.update()
        if self.refToCurrentAttack == None:
            self.set_state("idle")
            return
        

            

        if(self.attackPressed):

            canCancel = self.refToCurrentAttack.canCancel()
            if self.animation == "atk1" and canCancel: 
                self.set_animation("atk2", True)
                self.refToCurrentAttack.clear()
                self.refToCurrentAttack = PlayerAttacks.meleeAttack2(self)
            elif self.animation == "atk2" and canCancel:  
                self.set_animation("atk3", True)
                self.refToCurrentAttack.clear()
                self.refToCurrentAttack = PlayerAttacks.meleeAttack3(self)
            self.attackPressed = False
        
    
    def hurtState(self):
        
            
        hurtStateTime = 20

        
        self.invinFrames = 40     
        if self.elapsedFramesInState > hurtStateTime:

            if self.isGrounded():
                self.set_state("idle")
                self.set_animation("idle", True)
            else:
                self.set_state("air")
            self.priorityLastHitBy = -1
        
        if self.animation == "hitBack":
            self.posX -= 2 * self.direction
        else:
            self.posX += 2 * self.direction
        

        if self.isGrounded():
            pass
        else:
            if self.yVelocity > 0:
                self.yVelocity = 0 
            self.posY -= self.yVelocity
            self.yVelocity -= self.yGravity



    
    def deathState(self):
        self.set_animation("death")  
        self.hurtbox.disableHurtBox()
        if self.isGrounded():
            pass
        else:
            if self.yVelocity > 0:
                self.yVelocity = 0 
            self.posY -= self.yVelocity
            self.yVelocity -= self.yGravity 
    

    def victoryState(self):
        self.hurtbox.disableHurtBox()
        poseTime = 150 
        if self.isGrounded():
            self.set_animation("victory")

            if(self.elapsedFramesInState > poseTime):
                self.resetAllAnimation()
                self.hurtbox.enableHurtBox()
                self.set_state("idle")
        else:
            if self.yVelocity > 0:
                self.yVelocity = 0 
            self.posY -= self.yVelocity
            self.yVelocity -= self.yGravity 

     
            


