from graphics import *

def game():
	win = GraphWin("Titulo", 600, 400)
	win.setBackground("black")
	player = Circle(Point(300,200), 20)
	player.setFill("white")
	player.draw(win)
	
	while True:
		key = win.checkKey()

		if key == "w":
			player.move(0, -5)
		elif key == "s":
			player.move(0, 5)
		elif key == "d":
			player.move(5, 0)
		elif key == "a":
			player.move(-5, 0)

game()
