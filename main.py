import pygame
from worldgenerator import WorldGenerator
import cProfile

pygame.init()
clock = pygame.time.Clock()
running = True
window = pygame.display.set_mode((1980, 1080))
window.fill((255, 255, 255))
cProfile.run('WorldGenerator(500)')
world = WorldGenerator(500).get_world()


def draw_world():
    for i in world:
        print("drawing")
        window.blit(i.image, (i.x * 25, i.y * 25))


while running:

    clock.tick(60)
    window.fill((255, 255, 255))
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False


    draw_world()

    pygame.display.flip()


pygame.quit()




