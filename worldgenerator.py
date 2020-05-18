import random
from block import Block


class WorldGenerator:
    def __init__(self, width, seed=random.randint(1, 1000)):
        self.height = 100
        self.width = width
        self.seed = seed
        self.world = []
        self.generate()

    def generate(self):
        for i in range(self.height):
            if i > 10:
                for j in range(self.width):
                    self.world.append(Block(self.get_id(i), j, i))

    def get_world(self):
        print(self.world)
        return self.world

    def get_id(self, height):
        if height == 11:
            return 3
        elif height <= 14:
            return 1
        else:
            return 2
