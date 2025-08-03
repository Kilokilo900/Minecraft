import pickle

class Mapmanager:
    def __init__(self, loader, render, map_model='block.egg', map_texture='block.png'): 
        self.loader = loader
        self.render = render
        self.map_model = map_model
        self.map_texture = map_texture

        self.colors = [
            (0.2, 0.2, 0.35, 1),
            (0.2, 0.5, 0.2, 1),
            (0.7, 0.2, 0.2, 1),
            (0.5, 0.3, 0.0, 1)
        ]

        self.land = self.render.attachNewNode("Land")
        self.blocks = []

    def getColor(self, z):
        if z < len(self.colors):
            return self.colors[z]
        else:
            return self.colors[-1]

    def addBlock(self, position):
        block = self.loader.loadModel(self.map_model)
        block.setTexture(self.loader.loadTexture(self.map_texture))
        block.setPos(position)
        block.setColor(self.getColor(int(position[2])))
        block.setTag('at', str(position))  # <-- tag for finding later
        block.reparentTo(self.land)
        self.blocks.append(block)

    def clear(self):
        self.land.removeNode()

    def loadLand(self, filename):
        self.clear()
        self.land = self.render.attachNewNode("Land")
        self.blocks.clear()

        with open(filename) as file:
            y = 0
            for line in file:
                x = 0
                line = line.strip().split()
                for z_str in line:
                    height = int(z_str)
                    for z in range(height + 1):
                        self.addBlock((x, y, z))
                    x += 1
                y += 1

        return x, y

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True
    
    def findBlocks(self, pos):
        return self.land.findAllMatches("=at=" + str(pos))

    def findHighestEmpty(self, pos):
        x, y, _ = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)
    def delBlock(self, position):
        blocks = self.findBlocks(position)
        for block in blocks:
            block.removeNode()
    def buildBlock(self, pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)
    def delBlockFrom(self, position):
        x, y, z = position
        pos = x, y, z - 1
        blocks = self.findBlocks(pos)
        for block in blocks:
                block.removeNode()
    def SaveData(self):
        blocks = self.land.getChildren()

        with open('my_map.dat','wb') as  file:
            pickle.dump(len(blocks),file)

            for block in blocks:
                x,y,z=block.getPos()
                pos = int(x),int(y),int(z)
                pickle.dump(pos,file)
    def loadMap(self):
        
        self.clear()

        with open('my_map.dat', 'rb') as fin:
            

            length = pickle.load(fin)

            for i in range(length):

                pos = pickle.load(fin)


                self.addBlock(pos)