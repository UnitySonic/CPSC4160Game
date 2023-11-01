import pygame
from Scripts.Logic import gameLogicFunctions


class hitbox(pygame.sprite.Sprite):

    def __init__(self, ID,  Attack, rect, status, knockback, damage, priority,  startDelayInFrames, totalFrames) -> None:
        super().__init__()

        self.ID = ID
        self.rect = rect

        self.remainingFrames = totalFrames
        self.delay = startDelayInFrames
        self.attackRef = Attack
        self.damage = damage

        self.statuses = status
        self.knockback = knockback
        self.priority = priority
        self.type = self.attackRef.getAttackType()

        if self.delay <= 0:
            gameLogicFunctions.addBoxToGroup(self.attackRef.getAttackType(), self)


    def getEntity(self):
        return self.attackRef.parent

    def update(self):
        if self.delay > 0:
            if self.delay == 1:
                gameLogicFunctions.addBoxToGroup(self.attackRef.getAttackType(), self)
            self.delay -= 1
        elif self.remainingFrames > 0:
            self.remainingFrames -= 1
        else:
           self.killHitBox()

    def killHitBox(self):
        gameLogicFunctions.removeBoxFromGroup(self.attackRef.getAttackType(), self)
        self.attackRef.signal(self.ID)



    def handleCollision(self, CollisionType, OffendingHitbox):
        if CollisionType == "PHitToEHit":
            if self.priority > OffendingHitbox.priority:
                OffendingHitbox.killHitBox()
            elif self.priority < OffendingHitbox.priority:
                self.killHitBox()
            else:
                #Do Nothing
                pass





    def __del__ (self):
        pass


class hurtBox(pygame.sprite.Sprite):

    def __init__(self, parentEntity, type, rect, damage) -> None:
        super().__init__()

        self.parent = parentEntity
        self.rect = rect
        self.damage = damage
        self.type = type
        gameLogicFunctions.addBoxToGroup(type, self)

    def getEntity(self):
        return self.parent

    def update(self):
        self.rect.update((self.parent.posX, self.parent.posY), (self.rect.width, self.rect.height))







    def __del__ (self):
        pass


