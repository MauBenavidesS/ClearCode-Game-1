import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("Assets/font/Pixeltype.ttf", 50)

sky_surface = pygame.image.load("Assets/graphics/Sky.png").convert_alpha()
ground_surface = pygame.image.load("Assets/graphics/ground.png").convert_alpha()
text_surface = test_font.render('My game', False, 'black').convert_alpha()

snail_surface = pygame.image.load('Assets/graphics/snail/snail1.png').convert_alpha()
snail_x_position = 600

player_surface = pygame.image.load('Assets/graphics/player/player_walk_1.png').convert_alpha()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #draw all our elements
    screen.blit(ground_surface, (0,300))
    screen.blit(sky_surface, (0,0))
    screen.blit(text_surface, (300, 50))
    snail_x_position -= 4
    if snail_x_position <= -100:
        snail_x_position = 800
    screen.blit(snail_surface, (snail_x_position, 250))
    screen.blit(player_surface, (80, 200))

    # update everything
    pygame.display.update()
    clock.tick(60)
