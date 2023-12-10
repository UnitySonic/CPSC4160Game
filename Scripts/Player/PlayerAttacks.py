import pygame

#from  Scripts.Logic import Attack
from  Scripts.Logic import Collision
from  Scripts.Logic import Attack


class meleeAttack1(Attack.Attack):
    def __init__(self, parentEntity):
        super().__init__(parentEntity)
        self.sound = pygame.mixer.Sound("Assets/Sounds/p_saber1.wav")


        self.attackWidth = 63
        self.attackHeight = 85
        self.attackType = "PHitBox"


        hitbox1 = Collision.hitbox(1, self, pygame.Rect(0,0,self.attackWidth, self.attackHeight), "None",  0,  10, 1,  9  , 9)
        self.hitboxes[1] = hitbox1

        self.horiOffset = 20
        self.vertOffset = 80
    
    def canCancel(self):
        if len(self.hitboxes) == 0:
            return True
        else:
            return (self.hitboxes[1].delay <= 0)
    def update(self):
        if len(self.hitboxes) > 0:
            for hitbox in self.hitboxes.values():
                if hitbox.delay == 0 and self.soundPlayed == False:
                    self.sound.play()
                    self.soundPlayed = True
                self.recalculateHitbox(hitbox)  
                hitbox.update()
            self.cleanUp()
        else:
            self.parent.attackEnded()

class meleeAttack2(Attack.Attack):
    def __init__(self, parentEntity):
        super().__init__(parentEntity)
        self.sound = pygame.mixer.Sound("Assets/Sounds/p_saber2.wav")


        self.attackWidth = 63
        self.attackHeight = 85
        self.attackType = "PHitBox"


        hitbox1 = Collision.hitbox(1, self, pygame.Rect(0,0,self.attackWidth, self.attackHeight), "None",  0,  10, 2,  9, 9)
        self.hitboxes[1] = hitbox1
        self.horiOffset = 20
        self.vertOffset = 80
    
    def canCancel(self):
        if len(self.hitboxes) == 0:
            return True
        else:
            return (self.hitboxes[1].delay <= 0)
    def update(self):
        if len(self.hitboxes) > 0:
            for hitbox in self.hitboxes.values():
                if hitbox.delay == 0 and self.soundPlayed == False:
                    self.sound.set_volume(0.5)
                    self.sound.play()
                    self.soundPlayed = True
                self.recalculateHitbox(hitbox)  
                hitbox.update()
            self.cleanUp()
        else:
            self.parent.attackEnded()

class meleeAttack3(Attack.Attack):
    def __init__(self, parentEntity):
        super().__init__(parentEntity)
        self.sound = pygame.mixer.Sound("Assets/Sounds/p_saber3.wav")


        self.attackWidth = 60
        self.attackHeight = 90
        self.attackType = "PHitBox"
        self.horiOffset = 20
        self.vertOffset = 80


        hitbox1 = Collision.hitbox(1, self, pygame.Rect(0,0,self.attackWidth, self.attackHeight), "None",  0,  10, 3,  11, 9)
        self.hitboxes[1] = hitbox1
    def canCancel(self):
        if len(self.hitboxes) == 0:
            return True
        else:
            return (self.hitboxes[1].delay <= 0)
    def update(self):
        if len(self.hitboxes) > 0:
            for hitbox in self.hitboxes.values():
                if hitbox.delay == 0 and self.soundPlayed == False:
                    self.sound.set_volume(0.5)
                    self.sound.play()
                    self.soundPlayed = True
                self.recalculateHitbox(hitbox)  
                hitbox.update()
            self.cleanUp()
        else:
            self.parent.attackEnded()



class crouchAttack(Attack.Attack):
    def __init__(self, parentEntity):
        super().__init__(parentEntity)
        self.sound = pygame.mixer.Sound("Assets/Sounds/p_saber1.wav")


        self.attackWidth = 60
        self.attackHeight = 90
        self.attackType = "PHitBox"
        self.horiOffset = 20
        self.vertOffset = 80


        hitbox1 = Collision.hitbox(1, self, pygame.Rect(0,0,self.attackWidth, self.attackHeight), "None",  0,  10, 0,  11, 9)
        self.hitboxes[1] = hitbox1
    def canCancel(self):
        if len(self.hitboxes) == 0:
            return True
        else:
            return (self.hitboxes[1].delay <= 0)
    def update(self):
        if len(self.hitboxes) > 0:
            for hitbox in self.hitboxes.values():
                if hitbox.delay == 0 and self.soundPlayed == False:
                    self.sound.set_volume(0.5)
                    self.sound.play()
                    self.soundPlayed = True
                self.recalculateHitbox(hitbox)  
                hitbox.update()
            self.cleanUp()
        else:
            self.parent.attackEnded()


class airAttack(Attack.Attack):
    def __init__(self, parentEntity):
        super().__init__(parentEntity)
        self.sound = pygame.mixer.Sound("Assets/Sounds/p_saber1.wav")


        self.attackWidth = 60
        self.attackHeight = 90
        self.attackType = "PHitBox"
        self.horiOffset = 20
        self.vertOffset = 80
        


        hitbox1 = Collision.hitbox(1, self, pygame.Rect(0,0,self.attackWidth, self.attackHeight), "None",  0,  10, 1,  4, 8)
        self.hitboxes[1] = hitbox1
    def canCancel(self):
        if len(self.hitboxes) == 0:
            return True
        else:
            return (self.hitboxes[1].delay <= 0)
    def update(self):
        if len(self.hitboxes) > 0:
            for hitbox in self.hitboxes.values():
                if hitbox.delay == 0 and self.soundPlayed == False:
                    self.sound.set_volume(0.5)
                    self.sound.play()
                    self.soundPlayed = True
                self.recalculateHitbox(hitbox)  
                hitbox.update()
            self.cleanUp()
        else:
            self.parent.attackEnded()

















