import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('My Cool Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('fonts/advanced_pixel-7.ttf', 50)

sky_surface = pygame.image.load('images/sky.png').convert()
ground_surface = pygame.image.load('images/ground.png').convert()
text_surface = test_font.render('My game', False, 'black')

enemy_surface = pygame.image.load('images/enemy.png').convert_alpha()
enemy_x_pos = 1130

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 0))
    screen.blit(text_surface, (600, 50))
    enemy_x_pos -= 4
    if enemy_x_pos < -200:
        enemy_x_pos = 1130
    screen.blit(enemy_surface, (enemy_x_pos, 412))

    pygame.display.update()
    clock.tick(60)
