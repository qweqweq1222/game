import pygame
from parameters import *
import sys
def music():
    pygame.mixer.music.stop()
    pygame.mixer.music.load('music/music.mp3')
    pygame.mixer.music.play(10)

def menu(surface):
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    pygame.mixer.music.load('music/menu.mp3')
    pygame.mixer.music.play(10)
    x = 0
    button_font = pygame.font.Font('scrpht/font0.ttf', 72)
    start = button_font.render('START', 1, pygame.Color('lightgray'))
    button_start = pygame.Rect(0, 0, 400, 150)
    button_start.center = WIDTH // 2, HEIGHT // 2
    exit = button_font.render('EXIT', 1, pygame.Color('lightgray'))
    button_exit = pygame.Rect(0, 0, 400, 150)
    button_exit.center = WIDTH // 2, HEIGHT // 2 + 200
    menu_picture = pygame.image.load('img/bg.jpg').convert()
    menu_trigger = True
    while menu_trigger:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        surface.blit(menu_picture, (0, 0), (WIDTH, HEIGHT // 2, WIDTH, HEIGHT))
        x += 1

        pygame.draw.rect(surface, BLACK, button_start, border_radius=25, width=10)
        surface.blit(start, (button_start.centerx - 130, button_start.centery - 70))

        pygame.draw.rect(surface, BLACK, button_exit, border_radius=25, width=10)
        surface.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        if button_start.collidepoint(mouse_pos):
            pygame.draw.rect(surface, BLACK, button_start, border_radius=25)
            surface.blit(start, (button_start.centerx - 130, button_start.centery - 70))
            if mouse_click[0]:
                menu_trigger = False
        elif button_exit.collidepoint(mouse_pos):
            pygame.draw.rect(surface, BLACK, button_exit, border_radius=25)
            surface.blit(exit, (button_exit.centerx - 85, button_exit.centery - 70))
            if mouse_click[0]:
                pygame.quit()
                sys.exit()
        pygame.display.flip()

def check_win(surface, sprites, player):
    if not len([obj for obj in sprites.list_of_objects[player.index] if obj.flag == 1 and not obj.is_dead]):
        player.index += 1
        player.x = WIDTH
        player.y = HEIGHT
        if player.index == 1:
            for i in range(500):
                pygame.mixer.music.stop()
                pygame.mixer.music.load('music/music.mp3')
                pygame.mixer.music.play(10)
                render = pygame.font.Font('scrpht/font0.ttf', 144).render('ROUND 2!!!', 1, (120, 0, 0))
                rect = pygame.Rect(0, 0, 1000, 300)
                rect.center = WIDTH // 2, HEIGHT // 2
                pygame.draw.rect(surface, BLACK, rect, border_radius=50)
                surface.blit(render, (rect.centerx - 430, rect.centery - 140))
                pygame.display.flip()
        elif player.index == 2:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('music/winning.mp3')
            pygame.mixer.music.play(10)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            sys.exit()
                render = pygame.font.Font('scrpht/font0.ttf', 144).render('YOU WIN!!!', 1, (120, 0, 0))
                rect = pygame.Rect(0, 0, 1000, 300)
                rect.center = WIDTH // 2, HEIGHT // 2
                pygame.draw.rect(surface, BLACK, rect, border_radius=50)
                surface.blit(render, (rect.centerx - 430, rect.centery - 140))
                pygame.display.flip()

