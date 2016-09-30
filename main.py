#-*- coding:utf-8 -*-
from pprint import pprint

import time

from util import *
from model import *
from window import *
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

def killPlayer(win):
    text = Image(Point(300, 200), "death.png")
    text.draw(win)
    time.sleep(1)
def victory(win):
    text = Image(Point(300, 200), "win.png")
    text.draw(win)
    time.sleep(1)

def game():

    win = MyGraphWin("Titulo", 630, 400)
    win.setBackground("grey")
    texto = "(W,A,S,D) to move \n Don't touch the red blocks\n Press any key to start"
    textoCanvas = Text(Point(315,200), texto)
    textoCanvas.draw(win)
    while len(win._keysDown) == 0:
        win.update()

    bg = Image(Point(300, 200), "bg.png")
    bg.draw(win)
    quad = Quadtree(0, (0, 0 , 750, 450))
    quad.clear()

    reader = LevelReader("testlevel")
    level = reader.readLevel()
    entities = []
    for entity in level["wall"]:
        quad.insert(entity)
        entity.sprite.draw(win)
        entities.append(entity)
    for entity in level["player"]:
        quad.insert(entity)
        entity.sprite.draw(win)
        entities.append(entity)
    for entity in level["death"]:
        quad.insert(entity)
        entity.sprite.draw(win)
        entities.append(entity)
    for entity in level["win"]:
        quad.insert(entity)
        entity.sprite.draw(win)
        entities.append(entity)

    player = level["player"][0]

    camLock = True
    playerLooking = [0, 0]
    player.onAir = True
    while True:
        t = millis()
        win.update()

        if not (t % 17):
            player.collideX = ""
            player.collideY = ""
            returnObjects = []

            quad.retrieve(returnObjects, player)
            if player in returnObjects:
                returnObjects.remove(player)
            
            collidedObjects = []
            playerClone = Entity(posX=player.posX+player.velX, posY=player.posY+player.velY, width=player.width, height=player.height)
                        
            for obj in returnObjects:
                if checkCollision(playerClone, obj):
                    collidedObjects.append(obj)
            sides = []
            for obj in collidedObjects:
                if(obj.kills):
                    killPlayer(win)
                    return
                elif obj in level["win"]:
                    victory(win)
                    return
                collisions = checkCollisionSide(playerClone, obj)
                for collision in collisions:
                    sides.append(collision)
            
            if not (playerLooking[0] == "Right" and player.collideX == "Right") and\
                not (playerLooking[0] == "Left" and player.collideX == "Left"):
                player.collideX = ""
            if not (playerLooking[1] == "Up" and player.collideY == "Up"):
                player.collideY = ""
            if DOWN in sides:
                player.onAir = False
            
            elif RIGHT in sides and playerLooking[0] == "Right":
                player.velX = 0
                player.collideX = "Right"
            elif LEFT in sides and playerLooking[0] == "Left":
                player.velX = 0
                player.collideX = "Left"
            elif UP in sides and playerLooking[1] == "Up":
                player.collideY = "Up"
                player.velY = 0

            
            if DOWN not in sides:
                player.onAir = True

            


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
                    player.velX += player.velX*0.03
            player.velX *= 0.95
            if ('y' in win._keysDown or 'Y' in win._keysDown):
                camLock = False
            else:
                camLock = True

            if player.velX > 0:
                playerLooking[0] = "Right"
            elif player.velX < 0:
                playerLooking[0] = "Left"

            if player.velY > 0:
                playerLooking[1] = "Down"
            elif player.velY < 0:
                playerLooking[1] = "Up"
            

            for entity in entities:
                entity.update()
            ####RENDER:
            if camLock:
                player.sprite.move(player.velX, player.velY)
            else:
                for entity in entities:
                    entity.sprite.move(-player.velX, -player.velY)

            quad.clear();
            for entity in entities:
                quad.insert(entity)
                
                
            #centralizeCamera(playerSprite, win)

game()
