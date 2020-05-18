import pygame
from worldgenerator import WorldGenerator
from player import Player
import cProfile
import pickle
import threading
import time

Cube_Size = 25
Game_Tick = 0.1

pygame.init()
clock = pygame.time.Clock()
running = True
screen_width = 1980
screen_height = 1080
window = pygame.display.set_mode((screen_width, screen_height))
window.fill((255, 255, 255))
#cProfile.run('WorldGenerator(500)')
#world = WorldGenerator(500).get_world()
world = []
player = Player(Cube_Size*20, Cube_Size*8)


def load_image_resources():
    images = []
    ########## index 0 reserved for future use ##########
    images.append(pygame.image.load('dirt.png'))
    #####################################################
    images.append(pygame.image.load('dirt.png').convert())  # id = 1
    images.append(pygame.image.load('stone.png').convert())  # id = 2
    images.append(pygame.image.load('grass.png').convert())  # id = 3

    return images


image_resources = load_image_resources()


def save_world():
    with open('world.txt', 'wb') as fp:
        pickle.dump(world, fp)
        print("world saved")


def load_world():
    try:
        with open('world.txt', 'rb') as fp:
            global world
            world = pickle.load(fp)
            print("world loaded")
    except:
        if world == []:
            world = WorldGenerator(500).get_world()
            print("world created")


def show_fps(window, clock):
    FPS_FONT = pygame.font.SysFont("Verdana", 15)
    black = pygame.Color("black")
    fps_overlay = FPS_FONT.render(str(int(clock.get_fps())), True, black)
    window.blit(fps_overlay, (0, 0))

def draw_player():
    #print(player.x)
    window.blit(player.image, (player.x, player.y))


def draw_world():
    counter = 0
    for i in world:
        if i.x*Cube_Size < screen_width and i.y*Cube_Size < screen_height:
            #print("drawing")
            counter += 1
            window.blit(image_resources[i.id], (i.x * Cube_Size, i.y * Cube_Size))
    #print(counter)


def player_smooth_movement(px, py):
    print(px, py)
    if px != 0 and py != 0:
        for i in range(abs(int(px/5))):
            player.x += px / 5
            player.y += py / 5
            time.sleep(Game_Tick/5)
    elif px != 0:
        for i in range(abs(int(px/5))):
            player.x += px / 5
            time.sleep(Game_Tick/5)
    else:
        for i in range(abs(int(py / 5))):
            player.y += py / 5
            time.sleep(Game_Tick / 5)


def player_movement_handler():
    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and keys[pygame.K_w]:
            #player.x -= Cube_Size
            player_smooth_movement(-Cube_Size, -Cube_Size)
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            #player.x -= Cube_Size
            player_smooth_movement(-Cube_Size, Cube_Size)
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            #player.x -= Cube_Size
            player_smooth_movement(Cube_Size, -Cube_Size)
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            #player.x -= Cube_Size
            player_smooth_movement(Cube_Size, Cube_Size)
        elif keys[pygame.K_a]:
            #player.x -= Cube_Size
            player_smooth_movement(-Cube_Size, 0)
        elif keys[pygame.K_d]:
            #player.x += Cube_Size
            player_smooth_movement(+Cube_Size, 0)
        elif keys[pygame.K_w]:
            #player.y -= Cube_Size
            player_smooth_movement(0, -Cube_Size)
        elif keys[pygame.K_s]:
            #player.y += Cube_Size
            player_smooth_movement(0, +Cube_Size)
        #time.sleep(Game_Tick)


player_movement = threading.Thread(target=player_movement_handler)
player_movement.start()

load_world()

while running:

    clock.tick(160)
    window.fill((255, 255, 255))
    #keys = pygame.key.get_pressed()
    #if keys[pygame.K_DOWN]:
    #    print()
    #if keys[pygame.K_a]:
    #    player.x -= Cube_Size
    #elif keys[pygame.K_d]:
    #    player.x += Cube_Size
    #elif keys[pygame.K_w]:
    #    player.y -= Cube_Size
    #elif keys[pygame.K_s]:
    #    player.y += Cube_Size
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
           running = False


    #cProfile.run('draw_world()')
    draw_world()
    draw_player()
    show_fps(window, clock)
    pygame.display.flip()


save_world()
pygame.quit()




