import pygame
from sys import exit


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = my_font.render(f'Score: {current_time}', False, '#333333')
    score_rect = score_surf.get_rect(center=(640, 50))
    screen.blit(score_surf, score_rect)
    return current_time


pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Jumpu Knight')
clock = pygame.time.Clock()
my_font = pygame.font.Font('fonts/advanced_pixel-7.ttf', 50)
game_active = False
start_time = 0
score = 0

sky_surf = pygame.image.load('images/sky.png').convert()
ground_surf = pygame.image.load('images/ground.png').convert()

enemy_surf = pygame.image.load('images/enemy.png').convert_alpha()
enemy_rect = enemy_surf.get_rect(bottomright=(1080, 500))

player_surf = pygame.image.load('images/player.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 500))

# Intro screen
player_stand = pygame.transform.rotozoom(player_surf, 0, 2)
player_stand_rect = player_stand.get_rect(center=(640, 360))

game_title_surf = my_font.render('Jumpy Knight', False, '#333333')
game_title_rect = game_title_surf.get_rect(center=(640, 200))

instruction_surf = my_font.render('Press SPACE to start', False, '#333333')
instruction_rect = instruction_surf.get_rect(center=(640, 520))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 500:
                    player_gravity = -25

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 500:
                    player_gravity = -25
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                enemy_rect.left = 1280
                player_rect.y = 500
                player_gravity = 0
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 500))
        score = display_score()

        enemy_rect.x -= 7
        if enemy_rect.right <= 0:
            enemy_rect.left = 1280
        screen.blit(enemy_surf, enemy_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 500:
            player_rect.bottom = 500
        screen.blit(player_surf, player_rect)

        # Collision
        if enemy_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill('#84daf3')
        screen.blit(player_stand, player_stand_rect)

        score_message = my_font.render(f'Your score: {score}', False, '#333333')
        score_message_rect = score_message.get_rect(center=(640, 520))

        screen.blit(game_title_surf, game_title_rect)
        if score == 0:
            screen.blit(instruction_surf, instruction_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
