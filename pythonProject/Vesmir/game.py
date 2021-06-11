import pygame
from fotky import load_fotky, get_random_position, load_zvuk
from modely import Ship, Sutr

class Vesmir:

    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self.__init__pygame()
        self.screen = pygame.display.set_mode((1024,768))
        self.background = load_fotky("space", False)

        self.clock = pygame.time.Clock()
        self.asteroid = []
        self.strely = []
        self.spaceship = Ship((400,300), self.strely.append)

        for _ in range(6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break
            self.asteroid.append(Sutr(position, self.asteroid.append))

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()
    def __init__pygame(self):
        pygame.init()
        pygame.display.set_caption("VESMIRNE SUTRY")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()

            if(
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

        press = pygame.key.get_pressed()
        if self.spaceship:
            if press[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise = True)
            if press[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise = False)
            if press[pygame.K_UP]:
                self.spaceship.accelerate()
            if press[pygame.K_DOWN]:
                self.spaceship.decelerate()

    def _get_game_objects(self):
        game_objects = [*self.asteroid, *self.strely]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects


    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroid:
                if asteroid.kolize(self.spaceship):
                    self.spaceship = None

                break
        for strela in self.strely[:]:
            for asteroid in self.asteroid[:]:
                if asteroid.kolize(strela):
                    self.asteroid.remove(asteroid)
                    self.strely.remove(strela)
                    asteroid.split()
                    asteroid.zvuk.play()
                    break

        for strela in self.strely[:]:
            if not self.screen.get_rect().collidepoint(strela.position):
                self.strely.remove(strela)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))

        for game_object in self._get_game_objects():
            game_object.draw(self.screen)

        self.clock.tick(60)
        pygame.display.flip()