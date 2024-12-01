import pickle

class Mapmanager():
    def __init__(self):
        self.model = 'block' # the cube model is in the block.egg file
        self.texture = 'block.png'        
        self.colors = [
            (0.2, 0.2, 0.35, 1), # dark blue
            (0.2, 0.5, 0.2, 1), # dark green
            (0.7, 0.2, 0.2, 1), # dark red
            (0.5, 0.3, 0.0, 1) # brown            
            ]
        # Create a main node
        self.startNew()
        #self.addBlock((0,10, 0))

    def startNew(self):
        self.land = render.attachNewNode('land')   

    def getColor(self, z): # z is the height of the block
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[len(self.colors) -1]

    def addBlock(self, position):
        # building initial blocks
        self.block = loader.loadModel(self.model) # load the model
        self.block.setTexture(loader.loadTexture(self.texture)) # load the texture
        self.block.setPos(position) # set the position
        self.color = self.getColor(int(position[2])) # get the color
        self.block.setColor(self.color) # set the color

        self.block.setTag("at", str(position))    

        self.block.reparentTo(self.land) # reparent the block to the land node

    def clear(self):
        self.land.removeNode() # remove the land node
        self.startNew() # create a new land node

    def loadLand(self, filename):
        self.clear() # clear the land
        with open(filename) as file:
            y = 0 # y is the height
            for line in file:
                x = 0 # x is the width
                line = line.split(" ")
                for z in line: # z is the depth
                    for z0 in range(int(z) + 1): # add blocks from 0 to z
                        block = self.addBlock((x, y, z0)) # add a block
                    x += 1 # increase x
                y += 1

        return (x,y) # return the width and height of the land
    
    def findBlocks(self, pos): #find blocks at a given position
        return self.land.findAllMatches('=at=' + str(pos))
    
    def isEmpty(self, pos): #check if a position is empty
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True
        
    def findHighestEmpty(self, pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)
    
    def buildBlock(self, pos):
        # when building a block, add a block to the highest empty position. consider gravity
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)

    def deleteBlock(self, position):
        #remove blocks at a specific position
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()

    def deleteBlockFrom(self, position):
        x, y, z = self.findHighestEmpty(position)
        pos = x, y, z - 1
        for block in self.findBlocks(pos):
            block.removeNode()

    def saveMap(self):
        blocks = self.land.getChildren()
        # open a binary file
        with open('my_map.dat', 'wb') as fout:
                pickle.dump(len(blocks), fout)
                for block in blocks:
                    x, y, z = block.getPos()
                    pos = (int(x), int(y), int(z))
                    pickle.dump(pos, fout)

    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as fin:
            length = pickle.load(fin)
            for i in range(length):
                pos = pickle.load(fin)
                self.addBlock(pos)
