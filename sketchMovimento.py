#-*- coding:utf-8 -*-
from pprint import pprint

from graphics import *
import time
from util import *
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3


class Entity(object):
    def __init__(self, posX, posY, width, height, velX=0, velY=0, onAir=False, name="Entity"):
        self.posX = posX
        self.posY = posY

        self.width = width
        self.height = height
        self.collideX = None
        self.collideY = None

        self.velX = velX
        self.velY = velY
        self.onAir = onAir

        self.hitbox = ((posX - width/2, posY - height), (posX + width/2, posY))
        self.name = name

    def getXCenter(self):
        return self.posX

    def getYCenter(self):
        return (self.posY - self.height/2)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def move(self, x, y):
        self.posX += x
        self.posY += y
        self.hitbox = ((self.posX - self.width/2, self.posY - self.height), (self.posX + self.width/2, self.posY))
    
    def update(self):
        self.move(self.velX, self.velY)

    def __str__(self):
        return self.name

    """
    RETORNA: Lista `result` contendo quatro listas, tal que:
    lista[0] contém as colisões por cima (self acima da entidade)
    lista[1] contém as colisões pela esquerda
    lista[2] contém as colisões por baixo 
    lista[3] contém as colisões pela direita
    Cada colisão é uma tupla (d, e), onde `d` é a distância do overlap em pixels e `e` é a entidade
    """
    def detectCollisions(self, entities, withName=False):
        result = [[], [], [], []]
        p1 = self.hitbox[0]
        p2 = self.hitbox[1]
        for entity in entities:
            p3 = entity.hitbox[0]
            p4 = entity.hitbox[1]
            if withName:
                entity = entity.name
            if not checkCollision(p1, p2, p3, p4):
                continue
            if p1[1] <= p3[1]:
                pass # por cima
                d = p3[1] - p1[1]
                result[0].append((d, entity))
            if p1[0] <= p3[0]:
                d = p3[0] - p1[0]
                result[1].append((d, entity))
                pass # pela esquerda
            if p2[1] >= p4[1]:
                d = p2[1] - p4[1]
                result[2].append((d, entity))
                pass # por baixo
            if p2[0] >= p4[0]:
                d = p2[0] - p4[0]
                result[3].append((d, entity))
                pass # pela direita
        return result

class MovingBlock(Entity):
    def __init__(self, posX, posY, width, height, velX=0, velY=0, onAir=False, name="Entity", kills=False):
        super.__init__(self, posX, posY, width, height, velX, velY, onAir, name)
        self.kills = kills
        self.leftBound = self.posX
        self.rightBound = self.posX
        self.upperBound = self.posY
        self.lowerBound = self.posY

    def setBounds(upper, left, lower, right):
        self.leftBound = left
        self.rightBound = right
        self.upperBound = upper
        self.lowerBound = lower


    def update(self):
        if self.posX <= self.leftBound:
            self.velX = abs(self.velX)
        elif self.posX >= self.rightBound:
            self.velX = -abs(self.velX)

        if self.posY >= self.lowerBound:
            self.velY = -abs(self.velY)
        elif self.posY <= self.upperBound:
            self.velY = abs(self.velY)

        self.move(self.velX, self.velY)

class MyGraphWin(GraphWin):
    def _onKeyDown(self, evnt):
        if evnt.keysym not in self._keysDown:
            self._keysDown.append(evnt.keysym)
    def _onKeyUp(self, evnt):
        if evnt.keysym in self._keysDown:
            self._keysDown.remove(evnt.keysym)
        #Gambi para eventos envolvendo maiusculas ( letra com shift pode ficar presa)
        if evnt.keysym.lower() in self._keysDown:
            self._keysDown.remove(evnt.keysym.lower())
        if evnt.keysym.upper() in self._keysDown:
            self._keysDown.remove(evnt.keysym.upper())

    def getItems(self):
        """Return the items of the window"""
        return self.items
    
    def getPosition(self):
        return self.master.winfo_x(), self.master.winfo_y()
    def getDimensions(self):
        return self.master.winfo_width(), self.master.winfo_height()

    def __init__(self, title="Graphics Window",
                 width=200, height=200, autoflush=True):
        GraphWin.__init__(self, title, width, height, autoflush)
        self._keysDown = []
        self.bind_all("<KeyPress>", self._onKeyDown)
        self.bind_all("<KeyRelease>", self._onKeyUp)
        #self.bind_all("<Key>", self._onKey)

millis = lambda: int(round(time.time() * 1000))



def game():

    win = MyGraphWin("Titulo", 600, 400)
    win.setBackground("black")
    quad = Quadtree(0, (0, 0 , 700, 400))
    quad.clear()
    entities = []
    for x in xrange(0,10):
        boxSprite = Image(Point(x*70,350), "boxes_1.ppm")
        boxSprite.draw(win)
        box = Entity(posX = x*70, posY=350 + boxSprite.getHeight() / 2, width=boxSprite.getWidth(), height=boxSprite.getHeight(), name="ground_box_%d" % x)
        entities.append(box)

    #for box in boxes:
    #    box.draw(win)

    enemySprite = Image(Point(300,300), "box.ppm")
    enemy = Entity(posX=300, posY=300 + enemySprite.getHeight() / 2, width=enemySprite.getWidth(), height=enemySprite.getHeight(), name="enemy_box")
    enemySprite.draw(win)
    entities.append(enemy)
    

    playerSprite = Image(Point(100,50), "boxes_1.ppm")
    player = Entity(posX=100, posY=50 + playerSprite.getHeight() / 2, width=playerSprite.getWidth(), height=playerSprite.getHeight())
    #player.move(0, player.height / 2)
    entities.append(player)
    for entity in entities:
        quad.insert(entity)

    playerSprite.draw(win)
    velX = 0

    camLock = True
    sprites = win.getItems()
    sprites.remove(playerSprite)
    lastSide = None
    player.onAir = True
    while True:
        t = millis()
        win.update()

        if not (t % 17):
            returnObjects = []
            quad.retrieve(returnObjects, player)
            returnObjects.remove(player)
            collidedObjects = []
            for obj in returnObjects:
                if checkCollision(player, obj):
                    collidedObjects.append(obj)

            for obj in collidedObjects:
                collision = checkCollisionSide(player, obj)
                if DOWN == collision:
                    player.onAir = False
                elif RIGHT == collision:
                    player.velX = 0
                    player.collideX = "Right"
                elif LEFT == collision:
                    player.velX = 0
                    player.collideX = "Left"
                elif UP == collision:
                    player.collideY = "Up"
            
            if len(collidedObjects) == 0:
                player.onAir = True

            '''
            for entity in returnObjects:
                if entity == player:
                    continue
                newHitbox = ((player.hitbox[0][0] + player.velX, player.hitbox[0][1] + player.velY),
                        (player.hitbox[1][0] + player.velX, player.hitbox[1][1] + player.velY))
                if (player.hitbox[0][0] >= entity.hitbox[0][0] and player.hitbox[0][0] <= entity.hitbox[1][0] or
                player.hitbox[1][0] <= entity.hitbox[1][0] and player.hitbox[1][0] >= entity.hitbox[0][0] or
                player.hitbox[0][0] <= entity.hitbox[0][0] and player.hitbox[1][0] >= entity.hitbox[1][0]):
                    if player.hitbox[1][1] + 1 >= entity.hitbox[0][1]:
                        hasGroundBelow = True

                if (newHitbox[0][0] >= entity.hitbox[0][0] and newHitbox[0][0] <= entity.hitbox[1][0] or
                newHitbox[1][0] <= entity.hitbox[1][0] and newHitbox[1][0] >= entity.hitbox[0][0] or
                newHitbox[0][0] <= entity.hitbox[0][0] and newHitbox[1][0] >= entity.hitbox[1][0]):
                    #if player.hitbox[1][1] <= entity.getAnchor().getY() - entity.getHeight()/2 and\
                    if newHitbox[1][1] >= entity.hitbox[0][1] and \
                    player.hitbox[1][1] < entity.hitbox[0][1]:
                        player.onAir = False
                        hasGroundBelow = True
                        break
            '''
            

            if player.onAir:
                player.velY += 0.1
            else:
                player.velY = 0

                if ('w' in win._keysDown or 'W' in win._keysDown) and\
                    player.collideY != "Up":
                    player.velY = -5
                    player.onAir = True

                if ('d' in win._keysDown or 'D' in win._keysDown) and\
                    player.collideX != "Right":
                    if player.velX < 0:
                        player.velX *= 0.1
                    if player.velX < 2:
                        player.velX += 0.1
                    else:
                        player.velX += player.velX*0.02
                if ('a' in win._keysDown or 'A' in win._keysDown) and\
                    player.collideX != "Left":
                    if player.velX > 0:
                        player.velX *= 0.1
                    if player.velX > -2:
                        player.velX -= 0.1
                    else:
                        player.velX += player.velX*0.02
                player.velX *= 0.95
            if ('y' in win._keysDown or 'Y' in win._keysDown):
                camLock = False
            else:
                camLock = True

            player.collideX = None
            player.collideY = None

            for entity in entities:
                entity.update()
            ####RENDER:
            if camLock:
                playerSprite.move(player.velX, player.velY)
            else:
                for sprite in sprites:
                    sprite.move(-player.velX, -player.velY)

            quad.clear();
            for entity in entities:
                quad.insert(entity)
                
                
            #centralizeCamera(playerSprite, win)

game()
