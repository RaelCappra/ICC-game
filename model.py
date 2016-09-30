#-*- coding:utf-8 -*-
from graphics import *
class LevelReader():
    def __init__(self, filename):
        self.filename = filename
    def readLevel(self):
        result = {"wall": [], "player": [], "death": [], "win": []}
        with open(self.filename, "r") as f:
            linhas = f.readlines()
            for i in range(len(linhas)):
                linha = linhas[i]
                for j in range(len(linha)):
                    x = 70*j + 30
                    y = 70*i
                    if linha[j] == 'o':
                        sprite = Image(Point(x,y), "box.ppm")
                        entity = Entity(posX=x, posY=y+35, width=70, height=70, name="wall_%d,%d" % (i,j), sprite=sprite)
                        result["wall"].append(entity)
                    elif linha[j] == 'x':
                        sprite = Image(Point(x,y), "deathbox.ppm")
                        entity = Entity(posX=x, posY=y+35, width=70, height=70, name="death_%d,%d" % (i,j), sprite=sprite, kills=True)
                        result["death"].append(entity)
                    elif linha[j] == 'p':
                        sprite = Image(Point(x,y), "smallp1.png")
                        entity = Entity(posX=x, posY=y+25, width=50, height=50, name="player%d,%d" % (i,j), sprite=sprite)
                        result["player"].append(entity)
                    elif linha[j] == 'w':
                        sprite = Image(Point(x,y), "flagGreen.png")
                        entity = Entity(posX=x, posY=y+35, width=70, height=70, name="win%d,%d" % (i,j), sprite=sprite)
                        result["win"].append(entity)
        return result

class Entity(object):
    def __init__(self, posX, posY, width, height, velX=0, velY=0, onAir=False, name="Entity", kills=False, sprite=None):
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
        self.kills = kills
        self.sprite = sprite

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

