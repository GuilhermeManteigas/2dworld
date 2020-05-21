import random
from block import Block


class WorldGenerator:

    surface_level = 50
    dirt_depth = 30

    def __init__(self, width, height, seed=random.randint(1, 1000)):
        self.height = height
        self.width = width
        self.seed = seed
        self.world = []
        self.generate()

    def generate(self):
        for i in range(self.height):
            #if i > 10:
            for j in range(self.width):
                self.world.append(Block(self.get_id(i), j, i))

    def get_world(self):
        print(self.world)
        return self.world

    def get_id(self, height):
        if height < self.surface_level:
            #ran = random.randint(0, 3)
            #if ran == 2:
            #    return 2
            #else:
                return 0
        elif height == self.surface_level:
            return 3
        elif height <= self.surface_level + self.dirt_depth:
            return 1
        else:
            return 2
