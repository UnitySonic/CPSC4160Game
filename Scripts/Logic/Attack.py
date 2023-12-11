
import pygame

from Scripts.Logic import Collision


class  Attack():
    def __init__(self, parentEntity):

        self.parent = parentEntity
        self.hitboxes = {}
        self.cleanUpQueue = []
        self.horiOffset = 0
        self.vertOffset = 0
        self.sound = None
        
        self.soundPlayed = False

    def getAttackType(self):
        return self.attackType
    
    
    

    def recalculateHitbox(self, hitbox):
        attackStartY = self.parent.posY - self.vertOffset
        attackStartX = 0

        self.directionFaced = self.parent.direction

        if self.directionFaced == 1:
            attackStartX = self.parent.posX + self.horiOffset
        else:
            attackStartX = self.parent.posX - self.horiOffset - self.attackWidth

        hitbox.rect.x = attackStartX
        hitbox.rect.y = attackStartY
    
    def update(self):
        if len(self.hitboxes) > 0:
            for hitbox in self.hitboxes.values():
                self.recalculateHitbox(hitbox)  
                hitbox.update()
            self.cleanUp()
        else:
            self.parent.attackEnded()
            




    def clear(self):
        for hitbox in self.hitboxes.values():
            hitbox.forceKillHitBox()
    
    def signal(self, ID):
        self.cleanUpQueue.append(ID)
        

    def cleanUp(self):
        # Assuming self.hitboxes is a dictionary
        for ID in self.cleanUpQueue:
            if ID in self.hitboxes:
                self.hitboxes[ID].forceKillHitBox()
                self.hitboxes.pop(ID)
            self.cleanUpQueue.remove(ID)
        

    
    def __del__ (self):
        print("attackdeconttsuct")
        
        



