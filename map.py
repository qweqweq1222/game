from parameters import *
import pygame
str_map = [
    'SWSWSWSWSWSWSWSWSWSWSWSW',
    'W......................S',
    'S..WWWWWWWWWWWWWWWSS...S',
    'W..WWWWWWWWWWWWWWWSS...S',
    'S..WWW.................S',
    'W..SSSSSSSSSSSSSS......S',
    'S..SSSSS........W......S',
    'S...............W......S',
    'S..SSS.S........W......S',
    'W..SSS.SSSSSSSSSWSS..WWS',
    'S..SSS.................S',
    'W..SSS.......SSSSSS....S',
    'S..SSS.......W.........S',
    'W..SSS.......S.........S',
    'S..SSS.......W.........S',
    'WSWSWSWSWSWSWWSWSWSWSWSW'
]
str_map_1 = [
    'SWSWSWSWSWSWSWSWSWSWSWSW',
    'W......................S',
    'S..WWWWWWWW..WWWWWSS...S',
    'W..WWWWWWWW..WWWWWSS...S',
    'S..WWW.................S',
    'W..SSSSSSSS..SSSS......S',
    'S..SSSSS........W......S',
    'S...............W......S',
    'S..SSS.S........W......S',
    'W..SSS.SSSSSSSSSWSS..WWS',
    'S..SSS.................S',
    'W..SSS.WSSSSSSSSSSS....S',
    'S..SSS.......W.........S',
    'W..SSS.......S.........S',
    'S..SSS.......W.........S',
    'WSWSWSWSWSWSWWSWSWSWSWSW'
]

environment = {}
environment_1 = {}
map_1 = set()
map_2 = set()
map_a = [map_1, map_2]
collision_walls_0 = []
collision_walls_1 = []
for j, row in enumerate(str_map):
    for i, char in enumerate(row):
        if char != '.':
            collision_walls_0.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 'W':
                environment[(i * TILE, j * TILE)] = 'W'
                #environment_1[(i * TILE, j * TILE)] = 'W'
            elif char == 'S':
                environment[(i * TILE, j * TILE)] = 'S'
                #environment_1[(i * TILE, j * TILE)] = 'S'
            map_1.add((i * MAP_TILE, j * MAP_TILE))

for j, row in enumerate(str_map_1):
    for i, char in enumerate(row):
        if char != '.':
            collision_walls_1.append(pygame.Rect(i * TILE, j * TILE, TILE, TILE))
            if char == 'W':
                #environment[(i * TILE, j * TILE)] = 'W'
                environment_1[(i * TILE, j * TILE)] = 'W'
            elif char == 'S':
                #environment[(i * TILE, j * TILE)] = 'S'
                environment_1[(i * TILE, j * TILE)] = 'S'
            map_2.add((i * MAP_TILE, j * MAP_TILE))

collision_walls = [collision_walls_0, collision_walls_1]
ENV = [environment, environment_1]


