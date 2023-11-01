from abc import ABC, abstractmethod
import pygame

from Scripts.Logic import hitbox


class Attack(ABC):


    def __init__(self, parentEntity) -> None:
        self.hitboxes = {}
        self.parent = parentEntity

    def clear(self):
        for hitbox in self.hitboxes:
            del(hitbox)


    def signal(self, ID):
        self.hitboxes.pop(ID)



    def update(self):
        if len(self.hitboxes) > 0:
            for ID, hitbox in self.hitboxes:
                hitbox.update()
        else:
            del(self)

    def __del__ (self):
        self.parent.attackEnded()




