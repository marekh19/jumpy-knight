import pygame
from sys import exit
from random import randint


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = my_font.render(f'Score: {current_time}', False, '#333333')
    score_rect = score_surf.get_rect(center=(640, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 7

            if obstacle_rect.bottom == 500:
                screen.blit(shadowwalker_surf, obstacle_rect)
            if obstacle_rect.bottom == 350:
                screen.blit(bat_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -200]

        return obstacle_list
    else:
        return []


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def read_highscore():
    high_score_file = open(r'highscore', 'r')
    high_score = int(high_score_file.read())
    high_score_file.close()
    return high_score


def player_animation():
    # play walking animation if player is on the floor
    # display the jump surface when player is above ground
    global player_surf, player_index

    if player_rect.bottom < 500:
        player_surf = player_walk_2
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]


# Base setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Jumpy Knight')
clock = pygame.time.Clock()
my_font = pygame.font.Font('fonts/advanced_pixel-7.ttf', 50)
game_active = False
start_time = 0
score = 0
high_score = read_highscore()

# Environment
sky_surf = pygame.image.load('images/sky.png').convert()
ground_surf = pygame.image.load('images/ground.png').convert()

# Shadowwalker
shadowwalker_frame_1 = pygame.image.load('images/shadowwalker_1.png').convert_alpha()
shadowwalker_frame_2 = pygame.image.load('images/shadowwalker_2.png').convert_alpha()
shadowwalker_frames = [shadowwalker_frame_1, shadowwalker_frame_2]
shadowwalker_frame_index = 0
shadowwalker_surf = shadowwalker_frames[shadowwalker_frame_index]

# Bat
bat_frame_1 = pygame.image.load('images/bat_1.png').convert_alpha()
bat_frame_2 = pygame.image.load('images/bat_2.png').convert_alpha()
bat_frames = [bat_frame_1, bat_frame_2]
bat_frame_index = 0
bat_surf = bat_frames[bat_frame_index]

obstacle_rect_list = []

# Player
player_walk_1 = pygame.image.load('images/player_1.png').convert_alpha()
player_walk_2 = pygame.image.load('images/player_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(80, 500))


# Intro screen
player_stand = pygame.transform.rotozoom(player_walk_1, 0, 2)
player_stand_rect = player_stand.get_rect(center=(640, 360))

game_title_surf = my_font.render('Jumpy Knight', False, '#333333')
game_title_rect = game_title_surf.get_rect(center=(640, 200))

instruction_surf = my_font.render('Press SPACE to start', False, '#333333')
instruction_rect = instruction_surf.get_rect(center=(640, 520))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

shadowwalker_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(shadowwalker_animation_timer, 400)

bat_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(bat_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            # Click player to jump
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 500:
                    player_gravity = -25

            # Hit space to jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 500:
                    player_gravity = -25

            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(shadowwalker_surf.get_rect(bottomright=(randint(900, 1280), 500)))
                else:
                    obstacle_rect_list.append(bat_surf.get_rect(bottomright=(randint(900, 1280), 350)))
            
            if event.type == shadowwalker_animation_timer:
                if shadowwalker_frame_index == 0:
                    shadowwalker_frame_index = 1
                else:
                    shadowwalker_frame_index = 0
                shadowwalker_surf = shadowwalker_frames[shadowwalker_frame_index]
            
            if event.type == bat_animation_timer:
                if bat_frame_index == 0:
                    bat_frame_index = 1
                else:
                    bat_frame_index = 0
                bat_surf = bat_frames[bat_frame_index]


        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 500))
        score = display_score()

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 500:
            player_rect.bottom = 500
        player_animation()
        screen.blit(player_surf, player_rect)

        # Obstable movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Collision
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill('#84daf3')
        screen.blit(player_stand, player_stand_rect)

        # After game over, place player back to starting point & despawn enemies
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 500)
        player_gravity = 0

        score_message = my_font.render(f'Your score: {score}', False, '#333333')
        score_message_rect = score_message.get_rect(center=(640, 520))

        high_score_message = my_font.render(f'High score: {high_score}', False, '#333333')
        high_score_rect = high_score_message.get_rect(center=(640, 600))

        new_high_score = my_font.render('NEW HIGH SCORE!', False, '#333333')
        new_high_score_rect = new_high_score.get_rect(center=(640, 600))

        # Save new high score
        if score > high_score:
            high_score = score
            high_score_file = open(r'highscore', 'w')
            high_score_file.write(f'{score}')
            high_score_file.close()

        screen.blit(game_title_surf, game_title_rect)
        if score == 0:
            screen.blit(instruction_surf, instruction_rect)
            screen.blit(high_score_message, high_score_rect)
        elif score == high_score:
            screen.blit(score_message, score_message_rect)
            screen.blit(new_high_score, new_high_score_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(high_score_message, high_score_rect)

    pygame.display.update()
    clock.tick(60)
