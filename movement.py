from parameters import *
import pygame
import math
from map import collision_walls
class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.pos = (self.x, self.y)
        self.sns = 0.002
        self.hp = 100
        # игрок = квадрат (непроходимые стены)
        self.side = 50
        self.rect = pygame.Rect(*player_pos, self.side, self.side)
        self.index = 0
        self.bullets = 0
        self.shot = False
        self.with_gun = False
        self.player_with_gun = False

    @property
    def location(self):
        return (self.x, self.y)

    def walls(self, dx, dy):
        f_rect = self.rect.copy()
        f_rect.move_ip(dx, dy)
        bumps = f_rect.collidelistall(collision_walls[self.index])
        ''' test if all rectangles in a list intersect 
            Returns a list of all the indices that contain rectangles that collide with the Rect. 
            If no intersecting rectangles are found, an empty list is returned
        '''
        if len(bumps) > 0:
            delta_x, delta_y = 0, 0
            for bump in bumps:
                bump_rect = collision_walls[self.index][bump]
                delta_x = delta_x + f_rect.right - bump_rect.left if dx > 0 else delta_x + bump_rect.right - f_rect.left
                delta_y = delta_y + f_rect.bottom - bump_rect.top if dy > 0 else delta_y + bump_rect.bottom - f_rect.top

            # проверка на попадение в угол
            if abs(delta_x - delta_y) < 15:
                dx, dy = 0, 0

            dy, dx = (0, dx) if (delta_x > delta_y) else (dy, 0)

        self.x += dx
        self.y += dy

    def movement(self):
        self.key()
        self.mouse()
        self.rect.center = self.x, self.y
        self.angle %= math.pi * 2

    def key(self):
        sin = math.sin(self.angle)
        cos = math.cos(self.angle)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            dx = player_speed * cos
            dy = player_speed * sin
            self.walls(dx, dy)

        if keys[pygame.K_s]:
            dx = -player_speed * cos
            dy = -player_speed * sin
            self.walls(dx, dy)

        if keys[pygame.K_a]:
            dx = player_speed * sin
            dy = -player_speed * cos
            self.walls(dx, dy)

        if keys[pygame.K_d]:
            dx = -player_speed * sin
            dy = player_speed * cos
            self.walls(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_SPACE]:
            if not self.shot:
                if self.bullets > 0:
                    self.bullets -= 1
                elif self.bullets == 0:
                    self.bullets = 0
                self.shot = True

    def mouse(self):
        if pygame.mouse.get_focused():
            delta = pygame.mouse.get_pos()[0] - WIDTH // 2
            pygame.mouse.set_pos((WIDTH // 2, HEIGHT // 2))
            self.angle += delta * self.sns

