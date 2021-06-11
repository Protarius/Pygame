from pygame.math import Vector2
from pygame.transform import rotozoom
from fotky import load_fotky, wrap_position, get_random_velocity, load_zvuk



UP = Vector2(0,-1)


class Objekt:
    def __init__(self, position, sprite, velocity):
        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, position):
        blit_position = self.position - Vector2(self.radius)
        position.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def kolize(self, other_obj):
        distance = self.position.distance_to(other_obj.position)
        return distance < self.radius + other_obj.radius

class Ship(Objekt):
    MANEUVERABILITY = 5
    ACCELERATION = 0.1
    BRAKE = 0.1
    RYCHLOST_STRELY = 3

    def __init__(self, position, create_callback):
        self.laser_sound = load_zvuk("laser")
        self.create_callback = create_callback
        self.direction = Vector2(UP)

        super().__init__(position, load_fotky("spaceship"), Vector2(0))

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION

    def decelerate(self):
        self.velocity = self.direction * 0

    def shoot(self):
        bullet_velocity = self.direction * self.RYCHLOST_STRELY + self.velocity
        strela = Strela(self.position, bullet_velocity)
        self.create_callback(strela)
        self.laser_sound.play()

class Sutr(Objekt):
    def __init__(self, position, sutr_callback, size=3):
        self.sutr_callback = sutr_callback
        self.size = size
        self.zvuk = load_zvuk("exp")
        size_to_scale = {
            3: 0.25,
            2: 0.2,
            1: 0.1,
        }
        scale = size_to_scale[size]
        fotka = rotozoom(load_fotky("asteroid"), 0, scale)

        super().__init__(position, fotka, get_random_velocity(1,2))

    def split(self):
        if self.size > 1:
            for _ in range(2):
                asteroid = Sutr(self.position, self.sutr_callback, self.size -1)
                self.sutr_callback(asteroid)

class Strela(Objekt):
    def __init__(self, position, velocity):
        fotka = rotozoom(load_fotky("strela"), 0 , 0.25)
        super().__init__(position, fotka, velocity)

    def move(self, surface):
        self.position = self.position + self.velocity

