import pygame


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('player.png')
        self.health = 100
        self.falling_speed = 1
        self.mining_speed = 1
        self.mining_strength = 1


