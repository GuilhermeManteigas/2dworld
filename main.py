import pygame
from worldgenerator import WorldGenerator
from player import Player
import cProfile
import pickle
import threading
import time

Cube_Size = 64#50#25
Game_Tick = 0.1

pygame.init()
clock = pygame.time.Clock()
running = True
screen_width = 1920
screen_height = 1080
camera_x = 0
camera_y = 0
window = pygame.display.set_mode((screen_width, screen_height))
window.fill((255, 255, 255))
#cProfile.run('WorldGenerator(500)')
#world = WorldGenerator(500).get_world()
world = []
world_section = []
player = Player(Cube_Size*14, Cube_Size*7)
camera_width = screen_width * player.x
camera_height = screen_height * player.y
true_scroll = [0, 0]
scroll = [0, 0]


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
    window.blit(player.image, (int(player.x) - scroll[0], int(player.y) - scroll[1]))


def update_world_section():
    global world_section
    radiusx = 2000
    radiusy = 1000
    while running:
        temp_world = []
        for i in world:
            #if i.x*Cube_Size < screen_width and i.y*Cube_Size < screen_height:
            #if (player.x - (screen_width/2)) - Cube_Size * 5 < i.x * Cube_Size < (player.x + (screen_width/2)) + Cube_Size * 5 and (player.y - (screen_height/2)) - Cube_Size * 5 < i.y * Cube_Size < (player.y + (screen_height/2)) + Cube_Size * 5:
            if abs(player.x - i.x*Cube_Size) < radiusx and abs(player.y - i.y*Cube_Size) < radiusy:
                temp_world.append(i)
            #elif i.x - player.x < radius and player.y - i.y < radius:
                #temp_world.append(i)
        world_section = temp_world[:]
        time.sleep(Game_Tick*2)


def draw_world():
    #world[0].id = 1
    counter = 0
    for idx, i in enumerate(world_section):
        #if i.x*Cube_Size < screen_width and i.y*Cube_Size < screen_height:
        if (player.x - (screen_width/2)) - Cube_Size * 5 < i.x * Cube_Size < (player.x + (screen_width/2)) + Cube_Size * 5 and (player.y - (screen_height/2)) - Cube_Size * 5 < i.y * Cube_Size < (player.y + (screen_height/2)) + Cube_Size * 5:
            if i.id != 0:
                #print("drawing")
                #counter += 1
                window.blit(image_resources[i.id], (i.x * Cube_Size - scroll[0], i.y * Cube_Size - scroll[1]))
                #window.blit(image_resources[i.id], (i.x * Cube_Size - int(player.x / Cube_Size), i.y * Cube_Size - int(player.y / Cube_Size)))
                #if idx == 0:
                    #print((i.x * Cube_Size - int(player.x / Cube_Size), i.y * Cube_Size - int(player.y / Cube_Size)))
                    #print("player:")
                    #print(player.x, player.y)
                    #print("block:")
                    #print(i.x, i.y)
        counter = idx
    print(counter)


def player_smooth_movement(px, py):
    smoothness = 15
    counterx = 0
    countery = 0
    if px != 0 and py != 0:
        #for i in range(abs(int(px / smoothness) + int(px % smoothness))):
        for i in range(smoothness):
            player.x += int(px / smoothness)
            player.y += int(py / smoothness)
            time.sleep(Game_Tick/smoothness)
            counterx += int(px / smoothness)
            countery += int(py / smoothness)
    elif px != 0:
        #for i in range(abs(int(px / smoothness) + int(px % smoothness))):
        for i in range(smoothness):
            player.x += int(px / smoothness)
            time.sleep(Game_Tick/smoothness)
            counterx += int(px / smoothness)
        #if counterx < 64:
            #player.x += 64 - counterx
            #counterx += 64 - counterx
        #print(counterx)
    else:
        #for i in range(abs(int(py / smoothness) + int(py % smoothness))):
        for i in range(smoothness):
            player.y += int(py / smoothness)
            time.sleep(Game_Tick / smoothness)
            countery += int(py / smoothness)
        #if counterx < 64:
            #player.y += 64 - countery
            #countery += 64 - countery
    if counterx < 64 and counterx != 0:
        if 0 < counterx < 64:
            player.x += 64 - counterx
            counterx += 64 - counterx
        else:
            player.x += -64 - counterx
            counterx += -64 - counterx
    if countery < 64 and countery != 0:
        if 0 < countery < 64:
            player.y += 64 - countery
            countery += 64 - countery
        else:
            player.y += -64 - countery
            countery += -64 - countery
    print(player.x,player.y)
    #print(countery)



def player_movement_handler():
    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and keys[pygame.K_w]:
            player_smooth_movement(-Cube_Size, -Cube_Size)
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            player_smooth_movement(-Cube_Size, Cube_Size)
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            player_smooth_movement(Cube_Size, -Cube_Size)
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            player_smooth_movement(Cube_Size, Cube_Size)
        elif keys[pygame.K_a]:
            player_smooth_movement(-Cube_Size, 0)
        elif keys[pygame.K_d]:
            player_smooth_movement(+Cube_Size, 0)
        elif keys[pygame.K_w]:
            player_smooth_movement(0, -Cube_Size)
        elif keys[pygame.K_s]:
            player_smooth_movement(0, +Cube_Size)

        time.sleep(Game_Tick/12)

def gravity():
    while running:
        print()
        time.sleep(Game_Tick)


player_movement = threading.Thread(target=player_movement_handler)
player_movement.start()
update_visible_world = threading.Thread(target=update_world_section)
update_visible_world.start()

load_world()

cProfile.run('draw_world()')

while running:

    clock.tick(120)
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

    camera_x = player.x
    camera_y = player.y
    if player.x > screen_width / 4 * 3:
        camera_x += 50

    true_scroll[0] += (player.x - true_scroll[0] - (screen_width/2))/20
    true_scroll[1] += (player.y - true_scroll[1] - (screen_height / 2))/20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    #cProfile.run('draw_world()')
    draw_world()
    #cProfile.run('draw_player()')
    draw_player()
    show_fps(window, clock)
    pygame.display.flip()


save_world()
pygame.quit()




