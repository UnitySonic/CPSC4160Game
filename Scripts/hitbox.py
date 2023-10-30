import pygame

class hitbox:

    def __init__(self,rect, time, startDelayInFrames) -> None:
        self.sprite = pygame.sprite.Sprite()
        self.sprite.rect = rect

        self.remainingFrames = time
        self.delay = startDelayInFrames


    def update(self):
        if delay != 0:
            delay -=1
        elif self.remainingFrames > 0:
            self.remainingFrames -= 1
        else:
            del self


    def __del__ (self):
        pass
