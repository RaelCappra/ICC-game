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
    player = Circle(Point(300,200), 20)
    player.setFill("white")
    player.draw(win)
    while True:
        t = millis()
        print (t)
        if not (t % 17):
            print(win._keysDown)
            key = win.checkKey()
            #if key == "w":
            #    player.move(0, -5)
            #elif key == "s":
            #    player.move(0, 5)
            #elif key == "d":
            #    player.move(5, 0)
            #elif key == "a":
            #    player.move(-5, 0)
            if 'w' in win._keysDown or 'W' in win._keysDown:
                player.move(0, -5)
            if 's' in win._keysDown or 'S' in win._keysDown:
                player.move(0, 5)
            if 'd' in win._keysDown or 'D' in win._keysDown:
                player.move(5, 0)
            if 'a' in win._keysDown or 'A' in win._keysDown:
                player.move(-5, 0)

game()
