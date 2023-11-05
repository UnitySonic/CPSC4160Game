import pygame
from Scripts.Logic import gameLogicFunctions
from Scripts.Logic import Collision
from Scripts.Player import PlayerAttacks


class Player:

    def __init__(self, position):
        self.posX = position[0]
        self.posY = position[1]
        self.rect = pygame.Rect(self.posX, self.posY, 100, 100)
        self.hurtbox = Collision.hurtBox(self, "PHurtBox", self.rect, 0)
        self.HP = 100
        self.direction = 1
        self.refToCurrentAttack = None
        self.leftPressed = False
        self.rightPressed = False
        self.commitedToAttack = False
        self.scaleFactor =1



    def update(self, event = None):
        self.rect.x = self.posX
        self.rect.y = self.posY
        self.hurtbox.update()

        if self.leftPressed:
            self.direction = -1
            self.posX += 3 * self.direction
        elif self.rightPressed:
            self.direction = 1
            self.posX += 3 * self.direction
        if event == "atk1":
            if self.commitedToAttack != True:
                self.refToCurrentAttack = PlayerAttacks.meleeAttack1(self)
                self.commitedToAttack = True
        if self.commitedToAttack == True:
                self.refToCurrentAttack.update()

    def attackEnded(self):
        self.refToCurrentAttack = None
        self.commitedToAttack = False

    def getSpriteScale(self):
        return self.scaleFactor


    def getCurrentSpriteWidth(self):
        return self.rect.width

    def getCurrentSpriteHeight(self):
        return self.rect.height







    def handleCollision(self, CollisionType, Box):
        if CollisionType == "PHurtToEHit":

            self.HP - Box.damage

        elif CollisionType == "PHurtToEHurt":
            self.HP - Box.damage

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.leftPressed = True
            elif event.key == pygame.K_RIGHT:
                    self.rightPressed = True
            elif event.key == pygame.K_z:
                self.update("atk1")

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.leftPressed = False
            elif event.key == pygame.K_RIGHT:
                self.rightPressed = False


