import pygame
import sys
import os
import time
import json

class HP():

    def __init__(self, position):

        self.directory = "ui.json"

        with open(self.directory, "r") as file:
            self.uiData = json.load(file)

        self.hpBar = pygame.image.load(self.uiData["hpSheet"])
        self.y = 16
        self.hpBar.set_clip(pygame.Rect(0,self.y,64,16))
        self.image = self.hpBar.subsurface(self.hpBar.get_clip())
        self.rect = self.image.get_rect()
        self.hpBarClips = {int(key): value for key, value in self.uiData["hpBarClips"].items()}
        scaledX = int(self.rect.width * 5)
        scaledY = int(self.rect.height * 5)
        self.image = pygame.transform.scale(self.image, (scaledX, scaledY))
        
    def get_health(self):
        # Calculate health based on the y position of the health bar
        num_states = len(self.uiData["hpBarClips"])
        max_health = num_states * self.uiData["healthBarHeightRatio"]
        current_health = max(0, max_health - self.y / (self.uiData["healthBarHeightRatio"] / num_states))
        return current_health

    def take_damage(self, screen):
        self.y = min(self.y + 96, len(self.uiData["hpBarClips"]) * self.uiData["healthBarHeightRatio"])
        scaledX = int(self.rect.width * 5)
        scaledY = int(self.rect.height * 5)
        self.hpBar.set_clip(pygame.Rect(0, self.y, 64, 16))
        self.image = self.hpBar.subsurface(self.hpBar.get_clip())
        self.image = pygame.transform.scale(self.image, (scaledX, scaledY))
        screen.blit(self.image, (0, 0))