import pygame
playerHitBoxGroup = pygame.sprite.Group()
playerHurtBoxGroup = pygame.sprite.Group()

enemyHitBoxGroup = pygame.sprite.Group()
enemyHurtBoxGroup = pygame.sprite.Group()



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
        pass


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

    returnDictionary["PHitToEhit"] = collisionsPHitToEHit
    returnDictionary["PHitToEHurt"] = collisionsPHitToEHurt

    returnDictionary["PHurtToEHit"] = collisionsPHurtToEHit
    returnDictionary["PHurtToEHurt"] = collisionsPHurtToEHurt

    return returnDictionary



