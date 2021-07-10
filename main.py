import MM
from movement import Player
from MM import *
from Sprites import *
from Display import Display
pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
# инициализация
pygame.mouse.set_visible(True)
map_surface = pygame.Surface((WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE))
texture_0 = {'W': pygame.image.load('img/1.png').convert(), 'S': pygame.image.load('img/2.png').convert(), 'H': pygame.image.load('img/hell.png').convert()}
texture_1 = {'W': pygame.image.load('img/3.png').convert(), 'S': pygame.image.load('img/4.png').convert(), 'H': pygame.image.load('img/sky.png').convert()}
text = [texture_0, texture_1]
clock = pygame.time.Clock()
player = Player()
display = Display(surface, map_surface)
sprites = Sprites()
menu(surface)
pygame.mouse.set_visible(False)
music()
hart = pygame.image.load('img/hp/hearts.png')
hart = pygame.transform.scale(hart, (40, 40))
bullets = pygame.image.load('img/shotgun_2/0.png')

# основной цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    texture = text[player.index]
    surface.fill(BLACK)
    player.movement()
    display.blind(player.angle, texture)
    walls = display.ray_casting(player.location, player.angle, texture, player.index)
    display.world(surface, walls + [obj.position(player, walls, surface) for obj in sprites.list_of_objects[player.index] if obj.visible == True])
    display.weapon(player)
    display.display_map(player)
    display.hp(player, hart)
    display.patrons(player, bullets)
    display.fps(clock)
    MM.check_win(surface, sprites, player)
    pygame.display.flip()
    clock.tick()
