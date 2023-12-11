import pygame

#from  Scripts.Logic import Attack
from  Scripts.Logic import Collision
from Scripts.Logic import gameLogicFunctions

from Scripts.Logic import Attack





class meleeAttack1(Attack.Attack):
    def __init__(self, parentEntity):

        super().__init__(parentEntity)

      

        self.attackWidth = 200
        self.attackHeight = 320
        self.attackType = "EHitBox"


        attackStartY = self.parent.posY - self.attackHeight
        attackStartX = 0


        self.directionFaced = self.parent.direction

        if self.directionFaced == 1:
            attackStartX = self.parent.posX + 60
        else:
            attackStartX = self.parent.posX - 60 - self.attackWidth
        
        self.attackStartX = attackStartX
        self.attackStartY = attackStartY
        
        self.delay = 10


        rect1 = pygame.Rect(attackStartX, attackStartY, self.attackWidth, self.attackHeight)
        hitbox1 = Collision.hitbox(1, self, rect1, "None",  0,  20, 3,  self.delay, 32)
        self.hitboxes[1] = hitbox1
    
    def update(self):
        if len(self.hitboxes) > 0:
            for hitbox in self.hitboxes.values():
                
                hitbox.update()
                self.delay -= 1
                
                if self.delay == 0:
                    self.createFireBall()
            self.cleanUp()
        else:
            self.parent.attackEnded()
    
    def createFireBall(self):
        if self.directionFaced == 1:
            positionX = self.attackStartX + self.attackWidth
        else:
            positionX = self.attackStartX
        newBall = Fireball("fireball2", None, None, (positionX, self.attackStartY+ self.attackHeight//3) , None)






class meleeAttack2(Attack.Attack):
    def __init__(self, parentEntity):

        super().__init__(parentEntity)

        

        self.attackWidth = 180
        self.attackHeight = 200
        self.attackType = "EHitBox"

        attackStartY = self.parent.posY - self.attackHeight
        attackStartX = 0


        self.directionFaced = self.parent.direction

        if self.directionFaced == 1:
            attackStartX = self.parent.posX
        else:
            attackStartX = self.parent.posX - self.attackWidth


        rect1 = pygame.Rect(attackStartX, attackStartY, self.attackWidth, self.attackHeight)
        hitbox1 = Collision.hitbox(1, self, rect1, "None",  0,  20, 3,  11, 27)
        self.hitboxes[1] = hitbox1




    def update(self):
        if len(self.hitboxes) > 0:
            for hitbox in self.hitboxes.values():
                hitbox.update()
            self.cleanUp()

        else:
            self.parent.attackEnded()


##Time to rewrite this a bit lol(I think it's time for a boss attack json :skull:)
class Fireball(Attack.Attack):
    def __init__(self, fireBallID  ,fireBallData,  parentEntity , position, direction ):


        super().__init__(parentEntity)
        self.attackType = "EHitBox"
        self.fireBallID = fireBallID


        if fireBallData == None:
            self.fireBallData = gameLogicFunctions.boss1Data["attackData"][fireBallID]
        else:
            self.fireBallData = fireBallData
        
        self.direction = direction


        self.rise = self.fireBallData["rise"]
        self.run = self.fireBallData["run"]
        if self.fireBallID == "fireball1":
                self.run = abs(self.run) * self.direction

        self.attackWidth = self.fireBallData["attackWidth"]
        self.attackHeight = self.fireBallData["attackHeight"]


        self.framesTillSplit = 0
        self.timer = 20

        if self.fireBallData["children"] is not None :
            self.framesTillSplit = self.fireBallData["framesTillSplit"]

        
        
        
        if parentEntity != None:

            self.parent = parentEntity
            self.autoMode = False

            attackStartY = self.parent.posY - 80
            attackStartX = self.parent.posX


            if self.run <= 0:
                attackStartX = self.parent.posX + 60
            else:
                attackStartX = self.parent.posX - 60 - self.attackWidth

        else:
            self.position = position
            attackStartX = position[0]
            attackStartY = position[1]
            self.autoMode = True
        

        if self.fireBallData["children"] is not None:
            priority = 3
        else:
            priority = 0

        rect1 = pygame.Rect(attackStartX, attackStartY, self.attackWidth, self.attackHeight)
        hitbox1 = Collision.hitbox(0, self, rect1, "None",  0,  10, priority,  0, 9999)
        self.hitboxes[0] = hitbox1

        gameLogicFunctions.addEntity(self)
        






    #In this function it should run a timer for X frames and when that's over the attack "ends" and the Fireball
    #is just an  entity that flies around

    def update(self):
        self.timer -=1
        self.framesTillSplit -=1

        if self.timer <= 0 and self.autoMode == False:
            self.parent.attackEnded()
            self.autoMode = True

        if self.fireBallData["children"] is not None and self.framesTillSplit <= 0:
            for child in self.fireBallData["children"].keys():
                    newFireball = Fireball(self.fireBallID, self.fireBallData["children"][child], None, (self.hitboxes[0].rect.x, self.hitboxes[0].rect.y), self.direction)
                    splitSound = pygame.mixer.Sound("Assets/Sounds/e_fireballsplit.wav")
                    splitSound.set_volume(0.25)
                    splitSound.play()

            self.hitboxes[0].forceKillHitBox()
            gameLogicFunctions.removeEntity(self)
            del self
        else:
            hitbox = self.hitboxes[0]
            hitbox.rect = pygame.Rect(hitbox.rect.left + self.run, hitbox.rect.top + self.rise, hitbox.rect.width, hitbox.rect.height)
            hitbox.update()



























