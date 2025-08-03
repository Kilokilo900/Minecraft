from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from hero import Hero

class Game(ShowBase):
    def __init__(self):
        super().__init__()
        self.land = Mapmanager(self.loader, self.render, 'block.egg', 'block.png')
        self.land.loadLand('land2.txt')
    
        x,y = self.land.loadLand('land.txt')
        self.hero = Hero(pos=(x//2, y//2, 2), land=self.land)
        self.camLens.setFov(100)



game = Game()
game.run()
