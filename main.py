import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = test_font.render(str(current_time), False, (64, 64, 64))
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    print(current_time)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == ground_pos:
                screen.blit(snail_surf, obstacle_rect)
            elif obstacle_rect.bottom == fly_pos:
                screen.blit(fly_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
    return obstacle_list

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): 
                return False
    return True

def player_animation():
    """play walking animation if the player is on the floor
    display the jump surface when the player is not on the floor"""
    global player_surf, player_index
    if player_rect.bottom < 300:
        #jump
        player_surf = player_jump
    else:
        #walk
        player_index += 0.1
        if player_index >= len(player_walk_list):
            player_index = 0
        player_surf = player_walk_list[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("Assets/font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score = 0

sky_surf = pygame.image.load("Assets/graphics/Sky.png").convert_alpha()
ground_surf = pygame.image.load("Assets/graphics/ground.png").convert_alpha()
ground_pos = 300
fly_pos = ground_pos-90

# region obstacles
snail_frame_1 = pygame.image.load('Assets/graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('Assets/graphics/snail/snail2.png').convert_alpha()
snail_frame_list = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frame_list[snail_frame_index]

fly_frame_1 = pygame.image.load('Assets/graphics/fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('Assets/graphics/fly/Fly2.png').convert_alpha()
fly_frame_list = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frame_list[fly_frame_index]

obstacle_rect_list = []
# endregion obstacles

player_walk_1 = pygame.image.load('Assets/graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('Assets/graphics/player/player_walk_2.png').convert_alpha()
player_walk_list = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('Assets/graphics/player/jump.png').convert_alpha()

player_surf = player_walk_list[player_index]
player_rect = player_walk_1.get_rect(midbottom = (80, ground_pos))
player_gravity = 0
jump_height = -20

# Intro Screen
player_stand = pygame.image.load('Assets/graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(surface=player_stand, angle=0, scale=2)
player_stand_rect = player_stand.get_rect(center = (400,200))
title_font = pygame.font.Font("Assets/font/Pixeltype.ttf", 50)
title_surface = test_font.render('Pixel Runner', False, (111, 196, 169))
title_rect = title_surface.get_rect(midtop = (400, 50))
instructions_surface = test_font.render("Press SPACE to start playing and to jump.", False, (111, 196, 169))
instructions_rect = instructions_surface.get_rect(midtop = (400, 315))

# region timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer, 200)
# endregion timers


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = jump_height
            if event.type == pygame.KEYDOWN and player_rect.bottom >= ground_pos:
                player_gravity = jump_height
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900, 1100), ground_pos)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900, 1100), fly_pos)))
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frame_list[snail_frame_index]
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frame_list[fly_frame_index]
        elif game_active == False:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 100)

    if game_active:
        #draw all our elements
        screen.blit(ground_surf, (0,ground_pos))
        screen.blit(sky_surf, (0,0))
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, border_radius=10)
        # pygame.draw.rect(screen, '#c0e8ec', score_rect, width=6, border_radius=10)
        # screen.blit(score_surf, score_rect)
        score = display_score()

        # region Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= ground_pos:
            player_rect.bottom = ground_pos

        player_animation()
        screen.blit(player_surf, player_rect)
        # endregion

        # region obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        # endregion obstacle movement

        # region collisions
        game_active = collisions(player_rect, obstacle_rect_list)
        # endregion collisions
    else:
        screen.fill('black')
        screen.blit(player_stand, player_stand_rect)
        screen.blit(source=title_surface, dest=title_rect)
        player_gravity = 0
        
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, ground_pos)

        score_message = test_font.render(f'Your score is: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center = (400, 315))
        if score == 0:
            screen.blit(source=instructions_surface, dest=instructions_rect)
        else:
            screen.blit(source=score_message, dest=score_message_rect)

    # update everything
    pygame.display.update()
    clock.tick(60)
