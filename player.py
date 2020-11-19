import pygame
import threading
import time
from inventory import Inventory


Game_Tick = 0.1


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('player.png').convert_alpha()
        self.health = 100
        self.falling_speed = 1
        self.mining_delay = 5
        self.mining_strength = 1
        self.inventory = Inventory()
        #self.inventory_size = 6
        #self.inventory = []
    #    self.animation = False
    #   self.image_list = []

    #    player_animation = threading.Thread(target=self.animate)
    #    player_animation.start()

    #def animate(self):
    #    while True:
    #        if self.animation:
    #            for i in self.image_list:
    #                self.image = i
    #                print(i)
    #        time.sleep(Game_Tick / 12)

    #def set_animation(self, num):
    #    if num == 1:
    #        li = [pygame.image.load('player.png'), pygame.image.load('playerdrill.png')]
    #        self.image_list = li
    #    if num == 2:
    #        li = [pygame.image.load('player.png'), pygame.image.load('playerfan.png')]
    #        self.image_list = li

