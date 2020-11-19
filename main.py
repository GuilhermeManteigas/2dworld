import pygame
from worldgenerator import WorldGenerator
from player import Player
import cProfile
import pickle
import threading
import time

Cube_Size = 64
Game_Tick = 0.1
World_width = 200
World_height = 500

pygame.init()
clock = pygame.time.Clock()
running = True
screen_width = 1920
screen_height = 1080
map_min_x = 0 + screen_width/2
map_max_x = World_width * Cube_Size - screen_width/2
map_min_y = 0 + screen_height/2
map_max_y = World_height * Cube_Size - screen_height/2
camera_x = 0
camera_y = 0
window = pygame.display.set_mode((screen_width, screen_height))
window.fill((255, 255, 255))
world = []
world_section = []
blocks_around_p = []
player = Player(Cube_Size*World_width/2, Cube_Size * (WorldGenerator.surface_level - 1))
camera_width = screen_width * player.x
camera_height = screen_height * player.y
true_scroll = [0, 0]
scroll = [0, 0]
inventory_img = pygame.image.load('inventory.png')
show_inventory = True


def load_image_resources():
    ############### Blocks ##############################
    images = []
    ########## index 0 reserved for future use ##########
    images.append(pygame.image.load('dirt.png').convert())
    #####################################################
    images.append(pygame.image.load('dirt.png').convert())  # id = 1
    images.append(pygame.image.load('stone.png').convert())  # id = 2
    images.append(pygame.image.load('grass.png').convert())  # id = 3

    return images


image_resources = load_image_resources()


def save_world():
    with open('world.pkl', 'wb') as fp:
        pickle.dump(world, fp)
        print("world saved")


def load_world():
    try:
        with open('world.pkl', 'rb') as fp:
            global world
            world = pickle.load(fp)
            print("world loaded")
    except:
        if world == []:
            world = WorldGenerator(World_width, World_height).get_world()
            print("world created")


def show_fps(window, clock):
    FPS_FONT = pygame.font.SysFont("Verdana", 15)
    black = pygame.Color("black")
    fps_overlay = FPS_FONT.render(str(int(clock.get_fps())), True, black)
    window.blit(fps_overlay, (0, 0))
    #Coords on screen
    coors_overlay = FPS_FONT.render(str((int(player.x / Cube_Size), int(player.y / Cube_Size))), True, black)
    window.blit(coors_overlay, (0, 20))


def draw_player():
    window.blit(player.image, (int(player.x) - scroll[0], int(player.y) - scroll[1]))


def draw_inventory():
    #print("inventory")
    if show_inventory:
        window.blit(inventory_img, (screen_width - 308 - 100, 100))
    #window.blit(inventory_img, (500, 500))


def update_world_section():
    global world_section
    radiusx = 2000
    radiusy = 1000
    while running:
        temp_world = []
        for i in world:
            if abs(player.x - i.x*Cube_Size) < radiusx and abs(player.y - i.y*Cube_Size) < radiusy:
                temp_world.append(i)
        world_section = temp_world[:]
        time.sleep(Game_Tick*5)


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
    #print(counter)


def player_smooth_movement(px, py, delay = 0):
    smoothness = 15
    counterx = 0
    countery = 0
    if not (map_min_x < player.x + px < map_max_x):
        px = 0
    if not (map_min_y < player.y + py < map_max_y):
        py = 0
    if px != 0 and py != 0:
        for i in range(smoothness):
            player.x += int(px / smoothness)
            player.y += int(py / smoothness)
            time.sleep(Game_Tick/smoothness)
            counterx += int(px / smoothness)
            countery += int(py / smoothness)
    elif px != 0:
        for idx, i in enumerate(range(smoothness)):
            #time.sleep(Game_Tick / smoothness/delay)
            player.x += int(px / smoothness)
            time.sleep(Game_Tick/smoothness)
            counterx += int(px / smoothness)
    else:
        for idx, i in enumerate(range(smoothness)):
            #time.sleep(Game_Tick / smoothness / delay)
            player.y += int(py / smoothness)
            time.sleep(Game_Tick / smoothness)
            countery += int(py / smoothness)
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


def player_movement_handler():
    counter = 0
    while running:
        up = False
        blocks_around_player()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and keys[pygame.K_w]:
            up = True
            if blocks_around_p[0].id == 0 and blocks_around_p[1].id == 0 and blocks_around_p[3].id == 0 :
                player_smooth_movement(-Cube_Size, -Cube_Size)
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            if blocks_around_p[3].id == 0 and blocks_around_p[6].id == 0 and blocks_around_p[7].id == 0:
                player_smooth_movement(-Cube_Size, Cube_Size)
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            up = True
            if blocks_around_p[1].id == 0 and blocks_around_p[2].id == 0 and blocks_around_p[5].id == 0:
                player_smooth_movement(Cube_Size, -Cube_Size)
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            if blocks_around_p[5].id == 0 and blocks_around_p[7].id == 0 and blocks_around_p[8].id == 0:
                player_smooth_movement(Cube_Size, Cube_Size)
        elif keys[pygame.K_a]:
            if blocks_around_p[7].id != 0 or blocks_around_p[3].id == 0:
                player_smooth_movement(-Cube_Size, 0)

        elif keys[pygame.K_d]:
            if blocks_around_p[7].id != 0 or blocks_around_p[5].id == 0:
                player_smooth_movement(+Cube_Size, 0)
        elif keys[pygame.K_w]:
            up = True
            if blocks_around_p[1].id == 0:
                player_smooth_movement(0, -Cube_Size)
        elif keys[pygame.K_s]:
            if blocks_around_p[7].id == 0:
                player_smooth_movement(0, +Cube_Size)
            else:
                #mining
                time.sleep(Game_Tick*player.mining_delay)
                player_smooth_movement(0, +Cube_Size)
        #elif keys[pygame.K_e]:
            #global show_inventory
            #show_inventory = not show_inventory

        if not up:
            gravity()
        else:
            counter += 1
        collision_detector()
        #time.sleep(Game_Tick/12)
        time.sleep(Game_Tick / 6)


def blocks_around_player():
    global blocks_around_p
    blocks = []
    for i in world_section:
        if player.x - Cube_Size <= i.x * Cube_Size <= player.x + Cube_Size and player.y - Cube_Size <= i.y * Cube_Size <= player.y + Cube_Size:
            blocks.append(i)
    blocks_around_p = blocks


def collision_detector():
    for i in blocks_around_p:
        recti = pygame.Rect((i.x, i.y), (i.x + Cube_Size, i.y + Cube_Size))
        rectp = pygame.Rect((player.x, player.y), (player.x + Cube_Size, player.y + Cube_Size))
        if rectp.colliderect(recti):
            print("colided")
        if player.x == i.x * Cube_Size and player.y == i.y * Cube_Size and i.id != 0:
            print("colided cords")
            player.inventory.add_block_to_inventory(i.id)
            i.id = 0
        #print(player.x)
        #print(i.x*64)


def gravity():
    #while running:
        #print("s")
        temp_list = blocks_around_p.copy()
        if len(temp_list) > 7:
            if temp_list[7].id == 0:
                player_smooth_movement(0, +Cube_Size)
        #time.sleep(Game_Tick)


player_movement = threading.Thread(target=player_movement_handler)
player_movement.start()
update_visible_world = threading.Thread(target=update_world_section)
update_visible_world.start()
#gravity = threading.Thread(target=gravity)
#gravity.start()

load_world()

cProfile.run('draw_world()')

while running:

    clock.tick(120)
    window.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
           running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_e:
                show_inventory = not show_inventory

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
    draw_inventory()
    show_fps(window, clock)
    pygame.display.flip()


save_world()
pygame.quit()




