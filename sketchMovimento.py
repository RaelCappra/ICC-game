from graphics import *
import time

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
            print(win._keysDown)
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
