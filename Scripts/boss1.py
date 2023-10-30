# -*- coding: utf-8 -*-

import pygame

class boss_Crimson(pygame.sprite.Sprite):
    def __init__(self, position, Player):

        self.pos_x = position[0]
        self.pos_y = position[1]

        spriteSheetAttack1 = "../Assets/Boss_1/Attack1.png"
        spriteSheetAttack2 = "../Assets/Boss_1/Attack2.png"
        spriteSheetDeath = "../Assets/Boss_1/Death.png"
        spriteSheetFall = "../Assets/Boss_1/Fall.png"
        spriteSheetIdle = "../Assets/Boss_1/Idle.png"
        spriteSheetJump = "../Assets/Boss_1/Jump.png"
        spriteSheetRun = "../Assets/Boss_1/Run.png"
        spriteSheetHit = "../Assets/Boss_1/Take hit.png"



        #load images
        self.sheetAtk1 = pygame.image.load(spriteSheetAttack1)
        self.sheetAtk2 = pygame.image.load(spriteSheetAttack2)
        self.sheetDeath = pygame.image.load(spriteSheetDeath)
        self.sheetFall = pygame.image.load(spriteSheetFall)
        self.sheetIdle = pygame.image.load(spriteSheetIdle)
        self.sheetJump = pygame.image.load(spriteSheetJump)
        self.sheetRun = pygame.image.load(spriteSheetRun)
        self.sheetHit = pygame.image.load(spriteSheetHit)

        #defines area of a single sprite of an image
        #self.sheet.set_clip(pygame.Rect(0, 0, 0, 0))

        #loads spritesheet images
        self.image = self.sheetAtk1.subsurface(self.sheetAtk1.get_clip())
        self.rect = self.image.get_rect()

        #position image in the screen surface
        self.rect.topleft = position

        #variable for looping the frame sequence
        self.frame = 0

        self.rectWidth = 100
        self.rectHeight = 220


        self.atk1_states = {0: (74,107,58,60), 1: (328,98,55,69), 2: (584,91,52,76), 3: (859,88,120,79),4: (1109,52,127,115), 5: (1359,47,127,120), 6: (1609,26,127,141), 7: (1859,47,79,120)}
        self.atk2_states = {0: (109,58,72,109),1: (334,60,72,107),2: (581,53,75,114),3: (832,45,75, 122),4: (1083,39,160,129), 5: (1338,43,148,131),6: (1592,45,141,135),7: (1859, 81, 66,87)}

        self.death_states = {0: (108,84,45,83), 1: (358,74,52,93), 2: (608,72,66,95), 3: (858,64,96,103), 4: (1108,57,105,110), 5: (1358,45,96,122), 6: (1608,154,105,13)}
        self.fall_states = {0: (107,81,65,86), 1: (357,74,64,93)}
        self.idle_states = {0: (108,72, 57, 95), 1: (358,67,56,100), 2: (608,64,56,103), 3: (858,64,56,103), 4: (1108,67,57,100), 5: (1358,63,55,104), 6: (1608,70,54,97), 7: (1858,70,56,97)}
        self.jump_states = {0: (91,86,69,81), 1: (332,87,78,80)}
        self.run_states = {0: (94,106,65,61), 1: (342,105,67,62), 2: (592,102,67,65), 3: (839,99,70,68), 4: (1092,106,67,61), 5: (1343,100,66,67), 6: (1594,102,65,65), 7: (1846,100,63,64)}
        self.hit_states = {0: (106,80,45,87), 1: (358,81,34,86), 2: (608,87,35,80)}


    def get_frame(self, frame_set):
        #looping the sprite sequences.

        self.frame += 1



        #if loop index is higher that the size of the frame return to the first frame
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        currentAttackHeight = self.atk1_states[self.frame][3]
        self.rect.y = self.pos_y - currentAttackHeight

        #print(frame_set[self.frame])
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheetAtk1.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheetAtk1.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def update(self, direction):
        if direction == 'atk1':
            self.clip(self.atk1_states)
            #animate rect coordinates
            #self.rect.x -= 5
            self.image = self.sheetAtk1.subsurface(self.sheetAtk1.get_clip())
        if direction == 'atk2':
            self.clip(self.atk2_states)
            self.image = self.sheetAtk2.subsurface(self.sheetAtk1.get_clip())
            #self.rect.x += 5

        if self.pos_x < 500:
            self.pos_x += 1
            self.rect.x +=1



    #Start of State functions

    def runAroundState(self):
        elapsedTime = 0
        MAXTIMEINPHASE = 10

        #Two Aspects of this Phase, Running Left and Right, and Jumping




