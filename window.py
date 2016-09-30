#-*- coding:utf-8 -*-
from graphics import *
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

