import random
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound

def load_zvuk(name):
    path = f"bin/zvuky/{name}.wav"
    return Sound(path)

def load_fotky(name, with_alpha = True ):
    path = f"bin/fotky/{name}.png"
    nahrana_fotka = load(path)

    if with_alpha:
        return nahrana_fotka.convert_alpha()
    else:
        return nahrana_fotka.convert()


def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),
        random.randrange(surface.get_height()),
    )

def get_random_velocity(min_speed, max_speed):
    speed = random.randint(min_speed, max_speed)
    angle = random.randrange(0,360)
    return Vector2(speed,0).rotate(angle)
