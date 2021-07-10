from parameters import *
from collections import deque
from map import collision_walls
import pygame

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()

class Sprites:
    def __init__(self):
        self.counter = 3
        self.sprite_params = {'devil': {'sprite': pygame.image.load(f'img/tomato/0.png').convert_alpha(),
                                        'shift': -0.3,
                                        'dead': pygame.image.load(f'img/tomato_death/5.png').convert_alpha(),
                                        'scale': 2,
                                        'death': deque([pygame.image.load(f'img/tomato_death/{i}.png').convert_alpha() for i in range(3)]),
                                        'animation': deque([pygame.image.load(f'img/tomato/{i}.png').convert_alpha() for i in range(9)]),
                                        'visible': True,
                                        'is_gun': False,
                                        'equipment': False},

                              'demon': {'sprite': pygame.image.load(f'img/demon/0.png').convert_alpha(),
                                        'shift':  0,
                                        'scale': 2,
                                        'dead' : pygame.image.load(f'img/demon/death/0.png').convert_alpha(),
                                        'death': deque([pygame.image.load(f'img/demon/death/{i}.png').convert_alpha() for i in range(5)]),
                                        'animation': deque([pygame.image.load(f'img/demon/{i}.png').convert_alpha() for i in range(4)]),
                                        'visible': True,
                                        'is_gun': False,
                                        'equipment': False
                                        },
                              'shotgun': {
                                        'sprite': pygame.image.load(f'img/shotgun_2/gun_1.png').convert_alpha(),
                                        'shift': 1,
                                        'scale': 1,
                                        'dead': pygame.image.load(f'img/shotgun_2/gun_1.png').convert_alpha(),
                                        'death': deque(
                                            [pygame.image.load(f'img/shotgun_2/gun_1.png').convert_alpha()]),
                                        'animation': deque(
                                            [pygame.image.load(f'img/shotgun_2/gun_1.png').convert_alpha()]),
                                        'visible': True,
                                        'is_gun': True,
                                        'equipment': False
                                        },
                              'patrons': {
                                  'sprite': pygame.image.load(f'img/shotgun_2/0.png').convert_alpha(),
                                  'shift': 3,
                                  'scale': 0.5,
                                  'dead': pygame.image.load(f'img/shotgun_2/0.png').convert_alpha(),
                                  'death': deque(
                                      [pygame.image.load(f'img/shotgun_2/0.png').convert_alpha()]),
                                  'animation': deque(
                                      [pygame.image.load(f'img/shotgun_2/0.png').convert_alpha()]),
                                  'visible': True,
                                  'is_gun': True,
                                  'equipment': True
                              }
                              }
        self.list_of_objects_1 = [SpriteObject(self.sprite_params['patrons'], (200, 600)),
                                  SpriteObject(self.sprite_params['patrons'], (200, 800)),
                                  SpriteObject(self.sprite_params['patrons'], (200, 1000)),
                                  SpriteObject(self.sprite_params['shotgun'], (200, 400)),
                                  SpriteObject(self.sprite_params['devil'], (2 * WIDTH - 200, 2 * HEIGHT - 500)),
                                  SpriteObject(self.sprite_params['devil'], (2 * WIDTH - 600, 2 * HEIGHT - 1200)),
                                  SpriteObject(self.sprite_params['devil'], (WIDTH - 200, HEIGHT - 100)),
                                  SpriteObject(self.sprite_params['devil'], (WORLD_WIDTH - 200, WORLD_HEIGHT - 100)),
                                  SpriteObject(self.sprite_params['devil'], (WORLD_WIDTH - 400, WORLD_HEIGHT - 100)),
                                  SpriteObject(self.sprite_params['demon'], (WORLD_WIDTH - 200, WORLD_HEIGHT - 300)),
                                  SpriteObject(self.sprite_params['demon'], (WORLD_WIDTH - 400, WORLD_HEIGHT - 300)),
                                  SpriteObject(self.sprite_params['demon'], (WORLD_WIDTH - 1000, WORLD_HEIGHT - 600)),
                                  SpriteObject(self.sprite_params['demon'], (WORLD_WIDTH - 1400, WORLD_HEIGHT - 300)),
                                  ]

        self.list_of_objects_2 = [
                                  SpriteObject(self.sprite_params['devil'], (2 * WIDTH - 200, 200)),
                                  SpriteObject(self.sprite_params['devil'], (2 * WIDTH - 200, 500)),
                                  SpriteObject(self.sprite_params['devil'], (2 * WIDTH - 200, 2 * HEIGHT - 200)),
                                  SpriteObject(self.sprite_params['devil'], (2 * WIDTH - 200, 2 * HEIGHT - 500)),
                                  SpriteObject(self.sprite_params['devil'], (WORLD_WIDTH - 200, WORLD_HEIGHT - 100)),
                                  SpriteObject(self.sprite_params['devil'], (WORLD_WIDTH - 400, WORLD_HEIGHT - 100)),
                                  SpriteObject(self.sprite_params['devil'], (WORLD_WIDTH - 600, WORLD_HEIGHT - 100)),
                                  SpriteObject(self.sprite_params['demon'], (WORLD_WIDTH - 200, WORLD_HEIGHT - 300)),
                                  SpriteObject(self.sprite_params['demon'], (WIDTH - 100, WORLD_HEIGHT - 200)),
                                  SpriteObject(self.sprite_params['demon'], (WORLD_WIDTH - 400, WORLD_HEIGHT - 300)),
                                  SpriteObject(self.sprite_params['demon'], (WIDTH + 200, HEIGHT)),
                                  SpriteObject(self.sprite_params['demon'], (WIDTH - 200, HEIGHT))
                                  ]
        self.list_of_objects = [self.list_of_objects_1, self.list_of_objects_2]

class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.visible = parameters['visible']
        self.shift = parameters['shift']
        self.is_gun = parameters['is_gun']
        self.scale = parameters['scale']
        self.animation = parameters['animation'].copy()
        self.animation_dead = parameters['dead'].copy()
        self.animation_count = 0
        self.death_animation_count = 0
        self.equipment = parameters['equipment']
        self.death_animation = parameters['death'].copy()
        self.is_dead = False
        self.flag = 1
        self.side = 100
        self.x = pos[0]
        self.y = pos[1]
        self.counter = 0
        self.theta = 0
        self.distance_to_sprite = 0
        self.current_ray = 0
        self.projection = 0

    @property
    def is_on_fire(self): # спрайт находится под огнем
        if (NUM_RAYS//2 - 1) - self.side // 4 < self.current_ray < (NUM_RAYS//2 - 1) + self.side // 4:
            return True
        return False

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    # политика движения спрайтов аналогичная движению игрока
    def walls(self, dx, dy, player):
        rect = pygame.Rect(self.x - self.side // 4, self.y - self.side // 4, 50, 50)
        f_rect = rect.copy()
        f_rect.move_ip(dx, dy)
        bumps = f_rect.collidelistall(collision_walls[player.index])
        ''' test if all rectangles in a list intersect 
            Returns a list of all the indices that contain rectangles that collide with the Rect. 
            If no intersecting rectangles are found, an empty list is returned
        '''
        if len(bumps) > 0:
            delta_x, delta_y = 0, 0
            for bump in bumps:
                bump_rect = collision_walls[player.index][bump]
                delta_x = delta_x + f_rect.right - bump_rect.left if dx > 0 else delta_x + bump_rect.right - f_rect.left
                delta_y = delta_y + f_rect.bottom - bump_rect.top if dy > 0 else delta_y + bump_rect.bottom - f_rect.top

            # проверка на попадение в угол
            if abs(delta_x - delta_y) < 15:
                dx, dy = 0, 0

            dy, dx = (0, dx) if (delta_x > delta_y) else (dy, 0)

        self.x += dx
        self.y += dy

    def enemy_movement(self, player):
        if abs(self.distance_to_sprite) > TILE and not self.is_dead and not self.is_gun:
            dx = self.x - player.x
            dy = self.y - player.y
            if dx < 0:
                self.walls(2, 0, player)
            if dx > 0:
                self.walls(-2, 0, player)
            if dy > 0:
                self.walls(0, -2, player)
            if dy < 0:
                self.walls(0, 2, player)


    def position(self, player, dist_walls, surface):
        # фиксим проблемы с отрисовкой за экраном добавляя "фейковые" лучи (100)
        fake_0 = [dist_walls[0] for i in range(FAKE)]
        fake_1 = [dist_walls[-1] for i in range(FAKE)]
        fake = fake_0 + dist_walls + fake_1

        dx, dy = self.x - player.x, self.y - player.y
        self.distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += math.pi * 2

        delta_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = (NUM_RAYS // 2 - 1) + delta_rays
        self.distance_to_sprite *= math.cos(HALF_FOV - self.current_ray * DELTA_ANGLE)
        if 0 <= self.current_ray + FAKE <= NUM_RAYS - 1 + 2 * FAKE and self.distance_to_sprite < fake[self.current_ray + FAKE][0]:
            self.projection = min(int((3 * DISTANCE * TILE) / self.distance_to_sprite * self.scale), 2 * HEIGHT)
            shift = (self.projection // 2) * self.shift
            sprite_object = self.object
        # логика спрайтов
            if self.animation and not (self.is_on_fire and player.shot) and not self.is_dead and not self.is_gun:
                sprite_object = self.animation[0]
                if self.animation_count < 5:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0
                if self.distance_to_sprite < 150 and self.animation_count == 3:
                    self.counter += 2
                    if self.counter % 30 == 0:
                        self.counter = self.counter % 30
                        pygame.mixer.Sound('music/damage.mp3').play()
                    player.hp -= 2
        # логика убийства
            if (self.distance_to_sprite < 5 * TILE and self.is_on_fire) and (len(self.death_animation) > 1) \
                    and player.bullets != 0 and not self.is_gun and player.with_gun and player.shot and not self.is_dead:
                self.is_dead = True
                sprite_object = self.death_animation[0]

            if len(self.death_animation) > 1 and self.is_dead:
                self.animation_count += 1
                if self.animation_count >= 10:
                    self.death_animation.popleft()
                    self.animation_count = 0
                self.shift = 0.5

            if len(self.death_animation) == 1 and not self.is_gun:
                sprite_object = self.animation_dead

        # логика поднятия оружия и патронов
            elif self.is_gun or self.equipment:
                self.is_dead = True
                if self.distance_to_sprite < 100 and not player.with_gun and self.is_gun:
                    pygame.mixer.Sound('music/shotgun.mp3').play()
                    self.visible = False
                    player.with_gun = True
                elif self.distance_to_sprite < 100 and self.equipment:
                    pygame.mixer.Sound('music/bullet.mp3').play()
                    self.visible = False
                    player.bullets += 10
                sprite_object = self.object

            self.enemy_movement(player)
            sprite_pos = (self.current_ray * WIDTH//NUM_RAYS - (self.projection // 2),
                          HEIGHT // 2 - (self.projection // 2) + shift)
            sprite = pygame.transform.scale(sprite_object, (self.projection, self.projection))
            return self.distance_to_sprite, sprite, sprite_pos
        else:
            return False,












