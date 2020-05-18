import pygame


class Block:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.image = self.set_image()

    def set_image(self):
        if self.id == 1:
            return pygame.image.load('dirt.png')
        elif self.id == 2:
            return pygame.image.load('stone.png')
        if self.id == 3:
            return pygame.image.load('grass.png')

