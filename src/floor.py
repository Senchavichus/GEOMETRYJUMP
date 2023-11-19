import pygame as pg


class FloorTile:
    def __init__(self, x, y, size, speed, number_of_tiles):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.num_of_tiles = number_of_tiles     # Количество клеток пола на экране
        self.image = pg.transform.scale(pg.image.load("src/sprites/floor_tile.png"), (size, size))

    # Метод движения клеток пола
    def update(self):
        self.x -= self.speed
        if self.x <= -self.size:
            self.x += self.size * self.num_of_tiles

    # Метод отрисовик клеток пола
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
