from graphics import *
import time

def checkCollision(p1, p2, p3, p4):
    maxX = max(p2[0], p1[0]);
    minX = min(p2[0], p1[0]);

    maxY = max(p2[1], p1[1]);
    minY = min(p2[1], p1[1]);
    if(p3[0] <= maxX and p3[0] >= minX):
        if (p3[1] <= maxY and p3[1] >= minY):
            return 1;
        
        if (p4[1] <= maxY and p4[1] >= minY):
            return 1;

    if(p4[0] <= maxX and p4[0] >= minX):
        if (p4[1] <= maxY and p4[1] >= minY):
            return 1;
        
        if (p3[1] <= maxY and p3[1] >= minY):
            return 1;
    
    maxX = max(p3[0], p4[0]);
    minX = min(p3[0], p4[0]);

    maxY = max(p3[1], p4[1]);
    minY = min(p3[1], p4[1]);
    if(p1[0] <= maxX and p1[0] >= minX):
        if (p1[1] <= maxY and p1[1] >= minY):
            return 1;
        
        if (p2[1] <= maxY and p2[1] >= minY):
            return 1;

    if(p2[0] <= maxX and p2[0] >= minX):
        if (p2[1] <= maxY and p2[1] >= minY):
            return 1;
        
        if (p1[1] <= maxY and p1[1] >= minY):
            return 1;
    
    return 0;

class Player(object):
    def __init__(self, posX, posY, width, height, velX=0, velY=0, onAir=False):
        self.posX = posX
        self.posY = posY

        self.width = width
        self.height = height

        self.velX = velX
        self.velY = velY
        self.onAir = onAir

        self.hitbox = ((posX - width/2, posY + height), (posX + width/2, posY))
    def move(self, x, y):
        self.posX += x
        self.posY += y
        self.hitbox = ((self.posX - self.width/2, self.posY + self.height), (self.posX + self.width/2, self.posY))


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
    win.setBackground("white")
    
    
    boxes = [Image(Point(x*70,350), "boxes_1.ppm") for x in range(0, 10)]
    for box in boxes:
        box.draw(win)

    enemySprite = Image(Point(300,50), "box.ppm")
    enemy = Player(posX=300, posY=50, width = enemySprite.getWidth(), height=enemySprite.getHeight())
    enemySprite.draw(win)

    playerSprite = Image(Point(100,50), "boxes_1.ppm")
    player = Player(posX=100, posY=50, width=playerSprite.getWidth(), height=playerSprite.getHeight())
    player.posY += player.height / 2

    playerSprite.draw(win)
    velX = 0
    items = win.getItems()
    items.remove(playerSprite)

    camLock = True

    while True:
        
        t = millis()
        win.update()

        if not (t % 17):
            player.onAir = True
            for item in items:
                newHitbox = ((player.hitbox[0][0] + player.velX, player.hitbox[0][1] + player.velY),
                        (player.hitbox[1][0] + player.velX, player.hitbox[1][1] + player.velY))
                if (newHitbox[1][0] > item.getAnchor().getX() - item.getWidth()/2 and
                    newHitbox[0][0] < item.getAnchor().getX() + item.getWidth()/2):

                    #if player.hitbox[1][1] <= item.getAnchor().getY() - item.getHeight()/2 and\
                    if newHitbox[1][1] >= item.getAnchor().getY() - item.getHeight()/2:
                        player.onAir = False
                        break

                #if (player.posX + player.width/2 > item.getAnchor().getX() - item.getWidth()/2 and
                #    player.posX - player.width/2 < item.getAnchor().getX() + item.getWidth()/2):
                #    if player.posY < item.getAnchor().getY() - item.getHeight()/2:
                #        player.onAir = True
                #        break
                

            if player.onAir:
                player.velY += 0.1
            else:
                player.velY = 0

                if ('w' in win._keysDown or 'W' in win._keysDown):
                    player.velY = -3

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
                if ('y' in win._keysDown or 'Y' in win._keysDown):
                    camLock = False
                else:
                    camLock = True

                player.velX *= 0.95
    

            if camLock:
                player.move(player.velX, player.velY)

                playerSprite.move(player.velX, player.velY)
            else:
                player.move(player.velX, player.velY)
                for item in items:
                    item.move(-player.velX, -player.velY)


                
                
            #centralizeCamera(playerSprite, win)

game()
