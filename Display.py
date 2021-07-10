import pygame
from parameters import *
from map import ENV, map_a
from collections import deque
import sys
class Display:
    def __init__(self, surface, map_surface):
        self.surface = surface
        self.map_surface = map_surface
        self.weapon_base_sprite = pygame.image.load('img/shotgun/0.png').convert_alpha()
        self.weapon_shot_animation = deque([pygame.image.load(f'img/shotgun/{i}.png').convert_alpha()
                                            for i in range(7)])
        self.weapon_rect = self.weapon_base_sprite.get_rect()
        self.weapon_pos = (WIDTH // 2 - self.weapon_rect.width // 2, HEIGHT - self.weapon_rect.height)
        self.shot_length = len(self.weapon_shot_animation)
        self.shot_length_count = 0
        self.shot_animation_speed = 3 # скорость прокрутки анимации
        self.shot_animation_count = 0 # счетчик анимации
        self.shot_animation_trigger = True

    def ray_casting(self, player_pos, player_angle, texture, player_index): # главная функция отрисовки карты
        walls = []
        # определяем стартовый луч
        angle = player_angle - HALF_FOV
        xo, yo = player_pos
        # определяем вертикаль
        cur_sq_x = (xo // TILE) * TILE
        # определяем горизонталь
        cur_sq_y = (yo // TILE) * TILE

        for ray in range(NUM_RAYS):

            sin = math.sin(angle) if math.sin else 0.000001
            cos = math.cos(angle) if math.cos else 0.000001

            x, dx = (cur_sq_x + TILE, 1) if cos >= 0 else (cur_sq_x, -1)
            for i in range(0, WIDTH * 2, TILE):
                vertical = (x - xo) / cos
                yv = yo + vertical * sin
                if (((x+dx) // TILE) * TILE, (yv // TILE) * TILE) in ENV[player_index]:
                    texture_w = ENV[player_index][(((x+dx) // TILE) * TILE, (yv // TILE) * TILE)]
                    break
                x += dx * TILE

            y, dy = (cur_sq_y + TILE, 1) if sin >= 0 else (cur_sq_y, -1)
            for i in range(0, HEIGHT * 2, TILE):
                horizontal = (y - yo) / sin
                xh = xo + horizontal * cos
                if ((xh // TILE) * TILE, ((y+dy) // TILE) * TILE) in ENV[player_index]:
                    texture_s = ENV[player_index][((xh // TILE) * TILE, ((y+dy) // TILE) * TILE)]
                    break
                y += dy * TILE

            depth, offset, texture_chosen = (vertical, yv, texture_w) if vertical < horizontal else (horizontal, xh, texture_s)
            # определяем сдвиг
            offset = int(offset) % TILE
            # фиксим рыбий глаз
            depth *= math.cos(player_angle - angle)
            # избегаем деления на 0 в projection
            depth = max(depth, 0.00001)
            # вычисляем размер проекции
            projection = min(int(7 * DISTANCE * TILE / depth), 5 * HEIGHT)

            # режем подение фпс при приближении к стенам
            if projection > HEIGHT:
                coeff = projection / HEIGHT
                texture_height = WIDTH / coeff
                # определяем "ленту" текстуры
                tape = texture[texture_chosen].subsurface(offset * TEXTURE_SCALE,  WIDTH//2 - texture_height //2, TEXTURE_SCALE, texture_height)
                tape = pygame.transform.scale(tape, (SCALE, HEIGHT))
                tape_pos = (ray * SCALE,0)

            else:
                # определяем "ленту" текстуры
                tape = texture[texture_chosen].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, WIDTH)
                tape = pygame.transform.scale(tape, (SCALE, projection))
                tape_pos = (ray * SCALE, HEIGHT // 2 - projection // 2)

            # отрисовываем "ленту" текстуры
            self.surface.blit(tape, (ray * SCALE, HEIGHT // 2 - projection // 2))
            walls.append((depth, tape, tape_pos))
            angle += DELTA_ANGLE
        return walls

    def blind(self, angle, textures):
        # устраняем разрыв изображений за счет правильного сдвига
        sky_offset = -5 * math.degrees(angle) % WIDTH
        self.surface.blit(textures['H'], (sky_offset, 0))
        self.surface.blit(textures['H'], (sky_offset - WIDTH, 0))
        self.surface.blit(textures['H'], (sky_offset + WIDTH, 0))
        pygame.draw.rect(self.surface, DARKGRAY, (0, HEIGHT//2, WIDTH, HEIGHT // 2))

    def fps(self, clock):
        self.surface.blit(pygame.font.SysFont('Arial', 36, bold=True).render(str(int(clock.get_fps())), 0, RED), (WIDTH - 65, 0))

    def hp(self, player, hart):
        keys = pygame.key.get_pressed()
        if 70 <= player.hp <= 100:
            for i in range(3):
                self.surface.blit(hart, (i*20, 0))
        if 40 <= player.hp < 70:
            for i in range(2):
                self.surface.blit(hart, (i*20, 0))
        if 10 <= player.hp < 40:
            for i in range(1):
                self.surface.blit(hart, (i*20, 0))
        if player.hp == 0:
            pygame.mixer.music.stop()
            pygame.mixer.music.load('music/dramatic.mp3')
            pygame.mixer.music.play(10)
            render = pygame.font.Font('scrpht/font0.ttf', 144).render('YOU LOST', 1, (120, 0, 0))
            rect = pygame.Rect(0, 0, 1000, 300)
            rect.center = WIDTH // 2, HEIGHT // 2
            pygame.draw.rect(self.surface, BLACK, rect, border_radius=50)
            self.surface.blit(render, (rect.centerx - 430, rect.centery - 140))
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            sys.exit()

    def patrons(self, player, bullets):
        self.surface.blit(pygame.font.SysFont('Arial', 18, bold=True).render(str(player.bullets) if player.bullets > 0 else str(0), 0, BLACK),
                          (60, 40))
        self.surface.blit(bullets, (10, 40))

    def display_map(self, player):
        self.map_surface.fill(BLACK)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.line(self.map_surface, GREEN, (map_x, map_y), (map_x + 300 * math.cos(player.angle), map_y + 300 * math.sin(player.angle)), 2)
        pygame.draw.circle(self.map_surface, RED, (int(map_x), int(map_y)), 5)
        for x, y in map_a[player.index]:
            pygame.draw.rect(self.map_surface, (100, 0, 30), (x, y, MAP_TILE, MAP_TILE))
        self.surface.blit(self.map_surface, (0, HEIGHT - HEIGHT // MINIMAP_SCALE))

    # главный метод отрисовки спрайтов
    def world(self, surface, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                surface.blit(object, object_pos)

    def weapon(self, player):
        if player.with_gun == True:
            if player.shot:
                pygame.mixer.Sound('music/shot.mp3').play()
                shot_sprite = self.weapon_shot_animation[0]
                self.surface.blit(shot_sprite, self.weapon_pos)
                self.shot_animation_count += 1
                if self.shot_animation_count == self.shot_animation_speed:
                    self.weapon_shot_animation.rotate(-1)
                    self.shot_animation_count = 0
                    self.shot_length_count += 1
                    self.shot_animation_trigger = False
                if self.shot_length_count == self.shot_length:
                    player.shot = False
                    self.shot_length_count = 0
                    self.shot_animation_trigger = True
            else:
                self.surface.blit(self.weapon_base_sprite, self.weapon_pos)
