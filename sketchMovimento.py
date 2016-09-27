#-*- coding:utf-8 -*-
from pprint import pprint

from graphics import *
import time
from util import *

class Entity(object):
    def __init__(self, posX, posY, width, height, velX=0, velY=0, onAir=False, name="Entity"):
        self.posX = posX
        self.posY = posY

        self.width = width
        self.height = height

        self.velX = velX
        self.velY = velY
        self.onAir = onAir

        self.hitbox = ((posX - width/2, posY - height), (posX + width/2, posY))
        self.name = name

    def move(self, x, y):
        self.posX += x
        self.posY += y
        self.hitbox = ((self.posX - self.width/2, self.posY - self.height), (self.posX + self.width/2, self.posY))

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

def centralizeCamera(player, window):
    #lower left point
    p1 = (player.getAnchor().getX() - window.getWidth()/2, 
          player.getAnchor().getY() + window.getHeight()/2)

    #upper right
    p2 = (player.getAnchor().getX() + window.getWidth()/2, 
          player.getAnchor().getY() - window.getHeight()/2)
    window.setCoords(p1[0], p1[1], p2[0], p2[1])

def game():

    win = MyGraphWin("Titulo", 600, 400)
    win.setBackground("black")
    
    
    boxes = [Image(Point(x*70,350), "boxes_1.ppm") for x in xrange(0, 10)]
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

    playerSprite.draw(win)
    velX = 0

    camLock = True
    sprites = win.getItems()
    sprites.remove(playerSprite)

    player.onAir = True
    while True:
        
        t = millis()
        win.update()

        if not (t % 17):
            collisions = player.detectCollisions(entities[:-1])
            if collisions[0] or collisions[1] or collisions[2] or collisions[3]:
                pprint(player.detectCollisions(entities[:-1], withName=True))
            
            hasGroundBelow = False
            #for entity in entities:
            #    if entity == player:
            #        continue
            #    newHitbox = ((player.hitbox[0][0] + player.velX, player.hitbox[0][1] + player.velY),
            #            (player.hitbox[1][0] + player.velX, player.hitbox[1][1] + player.velY))
            #    if (player.hitbox[0][0] >= entity.hitbox[0][0] and player.hitbox[0][0] <= entity.hitbox[1][0] or
            #    player.hitbox[1][0] <= entity.hitbox[1][0] and player.hitbox[1][0] >= entity.hitbox[0][0] or
            #    player.hitbox[0][0] <= entity.hitbox[0][0] and player.hitbox[1][0] >= entity.hitbox[1][0]):
            #        if player.hitbox[1][1] + 1 >= entity.hitbox[0][1]:
            #            hasGroundBelow = True

            #    if (newHitbox[0][0] >= entity.hitbox[0][0] and newHitbox[0][0] <= entity.hitbox[1][0] or
            #    newHitbox[1][0] <= entity.hitbox[1][0] and newHitbox[1][0] >= entity.hitbox[0][0] or
            #    newHitbox[0][0] <= entity.hitbox[0][0] and newHitbox[1][0] >= entity.hitbox[1][0]):
            #        #if player.hitbox[1][1] <= entity.getAnchor().getY() - entity.getHeight()/2 and\
            #        if newHitbox[1][1] >= entity.hitbox[0][1] and \
            #        player.hitbox[1][1] < entity.hitbox[0][1]:
            #            player.onAir = False
            #            hasGroundBelow = True
            #            break
            if not hasGroundBelow:
                player.onAir = True

            if player.onAir:
                player.velY += 0.1
            else:
                player.velY = 0

                if ('w' in win._keysDown or 'W' in win._keysDown):
                    player.velY = -5
                    player.onAir = True

                if 'd' in win._keysDown or 'D' in win._keysDown:
                    if player.velX < 0:
                        player.velX *= 0.1
                    if player.velX < 2:
                        player.velX += 0.1
                    else:
                        player.velX += player.velX*0.02
                if 'a' in win._keysDown or 'A' in win._keysDown:
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

    


            for entity in entities:
                entity.move(entity.velX, entity.velY)
            ####RENDER:
            if camLock:
                playerSprite.move(player.velX, player.velY)
            else:
                for sprite in sprites:
                    sprite.move(-player.velX, -player.velY)


                
                
            #centralizeCamera(playerSprite, win)

game()
