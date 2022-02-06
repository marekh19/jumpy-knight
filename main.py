import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('images/player_1.png').convert_alpha()
        self.player_walk_2 = pygame.image.load('images/player_2.png').convert_alpha()
        self.player_walk = [player_walk_1, self.player_walk_2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(120, 500))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 500:
            self.gravity = -25

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 500:
            self.rect.bottom = 500

    def animation_state(self):
        if self.rect.bottom < 500:
            self.image = self.player_walk_2
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'bat':
            bat_1 = pygame.image.load('images/bat_1.png').convert_alpha()
            bat_2 = pygame.image.load('images/bat_2.png').convert_alpha()
            self.frames = [bat_1, bat_2]
            y_pos = 350
        if type == 'shadowwalker':
            shadowwalker_1 = pygame.image.load('images/shadowwalker_1.png').convert_alpha()
            shadowwalker_2 = pygame.image.load('images/shadowwalker_2.png').convert_alpha()
            self.frames = [shadowwalker_1, shadowwalker_2]
            y_pos = 500

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1400, 1700), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 7
        self.destroy()

    def destroy(self):
        if self.rect.x <= -200:
            self.kill()


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = my_font.render(f'Score: {current_time}', False, '#333333')
    score_rect = score_surf.get_rect(center=(640, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


def read_highscore():
    high_score_file = open(r'highscore', 'r')
    high_score = int(high_score_file.read())
    high_score_file.close()
    return high_score


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

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# Environment
sky_surf = pygame.image.load('images/sky.png').convert()
ground_surf = pygame.image.load('images/ground.png').convert()

# Intro screen
player_stand = pygame.image.load('images/player_1.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(640, 360))

game_title_surf = my_font.render('Jumpy Knight', False, '#333333')
game_title_rect = game_title_surf.get_rect(center=(640, 200))

instruction_surf = my_font.render('Press SPACE to start', False, '#333333')
instruction_rect = instruction_surf.get_rect(center=(640, 520))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

# Game runtime
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bat', 'shadowwalker', 'shadowwalker'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 500))
        score = display_score()

        # Player
        player.draw(screen)
        player.update()

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collision_sprite()

    else:
        screen.fill('#84daf3')
        screen.blit(player_stand, player_stand_rect)

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
