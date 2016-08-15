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
    sWin = MyGraphWin("Titulo", 200, 200)
    sWin.setBackground("white")
    sWin.master.geometry('+1000+1000')

    win = MyGraphWin("Titulo", 600, 400)
    win.setBackground("white")

    boxes = [Image(Point(x*70,350), "box.png") for x in range(0, 10)]
    for box in boxes:
        box.draw(win)

    player = Image(Point(300,200), "p1_duck.png")
    player.draw(win)
    velY = 0
    items = win.getItems()
    items.remove(player)

    while True:
        
        t = millis()
        win.update()
        #print (t)
        if not (t % 17):
            #print(win._keysDown)
            dimMain = win.getDimensions()
            dimSec = sWin.getDimensions()
            posMain = win.getPosition()
            posSec = sWin.getPosition()

            if checkCollision((posMain[0], posMain[1]),
                    (posMain[0] + dimMain[0], posMain[1] + dimMain[1]),
                    (posSec[0], posSec[1]),
                    (posSec[0] + dimSec[0], posSec[1] + dimSec[1])):
                print("colidiu")
            else:
                print("")
            
            #key = win.checkKey()
            #if key == "w":
            #    player.move(0, -5)
            #elif key == "s":
            #    player.move(0, 5)
            #elif key == "d":
            #    player.move(5, 0)
            #elif key == "a":
            #    player.move(-5, 0)
            onAir = True
            for item in items:
                if (player.getAnchor().getY() < item.getAnchor().getY() + item.getHeight() and
                   player.getHeight() + player.getAnchor().getY() > item.getAnchor().getY()):
                    onAir = False
                    break
            if onAir:
                velY *= 0.9
            if onAir and velY < 0.5:
                player.move(0, 5)
            else:
                if 'w' in win._keysDown or 'W' in win._keysDown:
                    player.move(0, -velY)
                    velY = 3
            
            if 'd' in win._keysDown or 'D' in win._keysDown:
                player.move(5, 0)
            if 'a' in win._keysDown or 'A' in win._keysDown:
                player.move(-5, 0)

game()
