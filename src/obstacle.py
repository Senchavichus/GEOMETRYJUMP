import pygame as pg


class Obstacle:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.image = pg.transform.scale(pg.image.load("src/sprites/obstacle.png"), (size, size))

    # Метод для движения шипа
    def update(self):
        self.x -= self.speed

    # Метод для отрисовки шипа
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
