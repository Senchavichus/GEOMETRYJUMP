import pygame as pg


class Player:
    def __init__(self, x, y, size, jump_strength, gravity, background_height):
        self.x = x
        self.y = y
        self.size = size
        self.jump_strength = jump_strength
        self.gravity = gravity
        self.background_height = background_height
        self.vel_y = 0
        self.on_ground = False      # Флаг нахождения игрока на земле для возможности прыжка
        self.image = pg.transform.scale(pg.image.load("src/sprites/player.png"), (size, size))

    # Метод прыжка для игрока
    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False

    # Метод обновления положения игрока
    def update(self):
        self.y += self.vel_y
        self.vel_y += self.gravity
        if self.y >= self.background_height - self.size:
            self.y = self.background_height - self.size
            self.on_ground = True
            self.vel_y = 0

    # Метод отрисовки игрока
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
