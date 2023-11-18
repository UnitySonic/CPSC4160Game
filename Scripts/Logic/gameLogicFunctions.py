import pygame
playerHitBoxGroup = pygame.sprite.Group()
playerHurtBoxGroup = pygame.sprite.Group()

enemyHitBoxGroup = pygame.sprite.Group()
enemyHurtBoxGroup = pygame.sprite.Group()

collisionGroup = pygame.sprite.Group()

entityList = []


def addEntity(entity):
    entityList.append(entity)
def removeEntity(entity):
    entityList.remove(entity)

def clearGroups():
    playerHitBoxGroup.empty()
    playerHurtBoxGroup.empty()
    enemyHitBoxGroup.empty()
    enemyHurtBoxGroup.empty()
    collisionGroup.empty()
    entityList.clear()

def addBoxToGroup(type, sprite):
    if type == "PHitBox":
        playerHitBoxGroup.add(sprite)
    elif type == "PHurtBox":
        playerHurtBoxGroup.add(sprite)

    elif type == "EHitBox":
        enemyHitBoxGroup.add(sprite)
    elif type == "EHurtBox":
        enemyHurtBoxGroup.add(sprite)
    else:
        collisionGroup.add(sprite)




def removeBoxFromGroup(type, sprite):
    if type == "PHitBox":
        playerHitBoxGroup.remove(sprite)
    elif type == "PHurtBox":
        playerHurtBoxGroup.remove(sprite)

    elif type == "EHitBox":
        enemyHitBoxGroup.remove(sprite)
    elif type == "EHurtBox":
        enemyHurtBoxGroup.remove(sprite)
    else:
        pass



def detectCollision():
    collisionsPHitToEHit = pygame.sprite.groupcollide(playerHitBoxGroup, enemyHitBoxGroup, False, False)
    collisionsPHitToEHurt = pygame.sprite.groupcollide(playerHitBoxGroup, enemyHurtBoxGroup, False, False)

    collisionsPHurtToEHit = pygame.sprite.groupcollide(playerHurtBoxGroup, enemyHitBoxGroup, False, False)
    collisionsPHurtToEHurt = pygame.sprite.groupcollide(playerHurtBoxGroup, enemyHurtBoxGroup, False, False)

    returnDictionary = {}

    returnDictionary["PHitToEHit"] = collisionsPHitToEHit
    returnDictionary["PHitToEHurt"] = collisionsPHitToEHurt

    returnDictionary["PHurtToEHit"] = collisionsPHurtToEHit
    returnDictionary["PHurtToEHurt"] = collisionsPHurtToEHurt



    return returnDictionary



