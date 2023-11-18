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


        rect1 = pygame.Rect(attackStartX, attackStartY, self.attackWidth, self.attackHeight)
        hitbox1 = Collision.hitbox(1, self, rect1, "None",  0,  10, 3,  10, 32)
        self.hitboxes[1] = hitbox1






class meleeAttack2(Attack.Attack):
    def __init__(self, parentEntity):

        super().__init__(parentEntity)

        

        self.attackWidth = 200
        self.attackHeight = 200
        self.attackType = "EHitBox"

        attackStartY = self.parent.posY - 220
        attackStartX = 0


        self.directionFaced = self.parent.direction

        if self.directionFaced == 1:
            attackStartX = self.parent.posX + 60
        else:
            attackStartX = self.parent.posX - 100 - self.attackWidth


        rect1 = pygame.Rect(attackStartX, attackStartY, self.attackWidth, self.attackHeight)
        hitbox1 = Collision.hitbox(1, self, rect1, "None",  0,  10, 3,  11, 32)
        self.hitboxes[1] = hitbox1




    def update(self):
        if len(self.hitboxes) > 0:
            for hitbox in self.hitboxes.values():
                hitbox.update()
            self.cleanUp()

        else:
            self.parent.attackEnded()



class Fireball(Attack.Attack):
    def __init__(self, rise, run, split, parentEntity = None, position = None, attackWidth = None, attackHeight = None):

        super().__init__(parentEntity)



        self.attackType = "EHitBox"
        self.split = split

        self.rise = rise
        self.run = run
        self.framesTillSplit = 0
        self.timer = 20

        if self.split == True:
            self.framesTillSplit = 60

        if parentEntity != None:

            self.parent = parentEntity


            self.attackWidth = 50
            self.attackHeight = 50

            self.autoMode = False

            attackStartY = self.parent.posY - 40
            attackStartX = self.parent.posX

            if self.run <= 0:
                attackStartX = self.parent.posX + 60
            else:
                attackStartX = self.parent.posX - 60 - self.attackWidth

        else:
            self.attackWidth = attackWidth
            self.attackHeight = attackHeight
            self.position = position
            attackStartX = position[0]
            attackStartY = position[1]
            self.autoMode = True
        

        if self.split:
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

        if self.split == True and self.framesTillSplit <= 0:


            Fireball1 = Fireball(8, self.run, False,None, (self.hitboxes[0].rect.x, self.hitboxes[0].rect.y), self.attackWidth/2, self.attackHeight/2)
            Fireball2 = Fireball(0, self.run, False,None, (self.hitboxes[0].rect.x, self.hitboxes[0].rect.y), self.attackWidth/2, self.attackHeight/2)
            Fireball3 = Fireball(-8, self.run, False,None, (self.hitboxes[0].rect.x, self.hitboxes[0].rect.y), self.attackWidth/2, self.attackHeight/2)



            self.hitboxes[0].forceKillHitBox()
            gameLogicFunctions.removeEntity(self)
            del self
        else:
            hitbox = self.hitboxes[0]
            hitbox.rect = pygame.Rect(hitbox.rect.left + self.run, hitbox.rect.top + self.rise, hitbox.rect.width, hitbox.rect.height)
            hitbox.update()



























