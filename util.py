#Collision constants
UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

#QuadTree constants
MAX_OBJECTS = 10
MAX_LEVELS = 5

def checkCollision(p1, p2, p3, p4):
    sides = []
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

class Quadtree():
    #cada object é uma tupla que contém (xcentro, ycentro, width, height)
    def __init__(self, pLevel, pBounds):
        self.level = pLevel
        self.objects = []
        self.bounds = pBounds
        self.nodes = [None, None, None, None]

    def clear(self): 
        self.objects = []
 
        for node in self.nodes:
            if node != None:
                node.clear()
                node = None

    def split(self): 
        subWidth = int((self.bounds[2] / 2));
        subHeight = int((self.bounds[3] / 2));
        x = int(self.bounds[0]);
        y = int(self.bounds[1]);
 
        self.nodes[0] = Quadtree(self.level+1, (x + subWidth, y, subWidth, subHeight));
        self.nodes[1] = Quadtree(self.level+1, (x, y, subWidth, subHeight));
        self.nodes[2] = Quadtree(self.level+1, (x, y + subHeight, subWidth, subHeight));
        self.nodes[3] = Quadtree(self.level+1, (x + subWidth, y + subHeight, subWidth, subHeight));
 
    def getIndex(self, pRect):
        index = -1;
        verticalMidpoint = self.bounds[0] + (self.bounds[2] / 2);
        horizontalMidpoint = self.bounds[1] + (self.bounds[3] / 2);
 
   # Object can completely fit within the top quadrants
        topQuadrant = (pRect[1] < horizontalMidpoint and pRect[1] + pRect[3] < horizontalMidpoint);
   # Object can completely fit within the bottom quadrants
        bottomQuadrant = (pRect[1] > horizontalMidpoint);
 
   # Object can completely fit within the left quadrants
        if (pRect[0] < verticalMidpoint and pRect[0] + pRect[2] < verticalMidpoint):
            if (topQuadrant):
                index = 1;
            
            elif (bottomQuadrant):
                index = 2;
            
        
    # Object can completely fit within the right quadrants
        elif (pRect[0] > verticalMidpoint):
            if (topQuadrant):
                index = 0;
            
            elif (bottomQuadrant):
                index = 3;
            
        
 
        return index;

    def insert(self, pRect):
        if (self.nodes[0] != None):
            index = self.getIndex(pRect);
     
            if (index != -1):
                self.nodes[index].insert(pRect);
                return
            
        
     
        self.objects.append(pRect);
     
        if (len(self.objects) > MAX_OBJECTS and self.level < MAX_LEVELS):
            if (self.nodes[0] == None):
                self.split(); 
            
     
            i = 0;
            while (i < len(self.objects)):
                index = self.getIndex(self.objects[i]);
                if (index != -1):
                    self.nodes[index].insert(self.objects.pop(i));            
                else:
                    i += 1
                    
    def retrieve(self, returnObjects, pRect):
        index = self.getIndex(pRect);
        if (index != -1 and self.nodes[0] != None):
            self.nodes[index].retrieve(returnObjects, pRect);
        
     
        returnObjects.extend(self.objects);
     
        return returnObjects;

'''
Example of usage
def game():
    #Creates quadTree
    quad = Quadtree(0, (0,0,600,600))
    win = GraphWin("title", 600, 600)
    objRect = []
    
    for x in range(0, 25):
        rect = Rectangle(Point(x, x), Point(x*10 + 70, x*10 + 10))
        objRect.append(((x + x*10 + 70)/2, (x + x*10 + 10)/2, x*9 + 70, x*9 + 10))
        rect.draw(win)
    
    quad.clear();
    for obj in objRect:
        quad.insert(obj)
    
    while True:
        time.sleep(2)

        
        returnObjects = [];
        quad.retrieve(returnObjects, obj);
        for obj in returnObjects:
            print obj

        key = win.checkKey()
        if key == "Escape":
            win.close()


        quad.clear();
        for obj in objRect:
            quad.insert(obj)

    win.getMouse()
    win.close()
'''