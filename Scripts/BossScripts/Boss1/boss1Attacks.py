import pygame

#from  Scripts.Logic import Attack
from  Scripts.Logic import Collision


class meleeAttack1():
    def __init__(self, parentEntity):
        #xsuper().__init__(parentEntity)

        self.parent = parentEntity
        self.hitboxes = {}
        self.cleanUpQueue = []

        self.attackWidth = 50
        self.attackHeight = 100
        self.attackType = "EHitBox"


        attackStartY = self.parent.posY - 40
        attackStartX = 0


        self.directionFaced = self.parent.direction

        if self.directionFaced == 1:
            attackStartX = self.parent.posX + 60
        else:
            attackStartX = self.parent.posX - 60 - self.attackWidth


        rect1 = pygame.Rect(attackStartX, attackStartY, self.attackWidth, self.attackHeight)
        hitbox1 = Collision.hitbox(1, self, rect1, "None",  0,  10, 3,  0, 200)
        self.hitboxes[1] = hitbox1

    def clear(self):
        for hitbox in self.hitboxes.values():
            del(hitbox)


    def signal(self, ID):
        self.cleanUpQueue.append(ID)

    def cleanUp(self):
        # Assuming self.hitboxes is a dictionary
        for ID in self.cleanUpQueue:
            del self.hitboxes[ID]

    def getAttackType(self):
        return self.attackType




    def update(self):
        if len(self.hitboxes) > 0:
            for hitbox in self.hitboxes.values():
                hitbox.update()
            self.cleanUp()

        else:
            self.parent.attackEnded()

    def __del__ (self):
        pass















