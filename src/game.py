import sys
import random as rnd

import pygame as pg

from src import config as cfg
from src.floor import FloorTile
from src.obstacle import Obstacle
from src.player import Player


class Game:
    def __init__(self):
        # Инициализация pygame
        pg.init()
        pg.mixer.init()

        # Включение музыки
        pg.mixer.music.load('src/music/stereo_madness.mp3')
        pg.mixer.music.play(-1)
        pg.mixer.music.set_volume(0.1)

        # Создание экрана
        self.screen = pg.display.set_mode((cfg.SCREEN_WIDTH, cfg.FLOOR_SIZE + cfg.BACKGROUND_HEIGHT))
        pg.display.set_caption("GEOMETRY JUMP")
        self.clock = pg.time.Clock()
        self.player = Player(150, 100, cfg.PLAYER_SIZE, cfg.JUMP_STRENGTH, cfg.GRAVITY, cfg.BACKGROUND_HEIGHT)

        # Создание флага для проверки зажатия SPACE, для возможности зажимать для прыжка
        self.jumping = False

        # Создание списка препятствий
        self.obstacles = []

        # Создание списка клеток пола
        self.floor_tiles = [
            FloorTile(i * cfg.FLOOR_SIZE, cfg.BACKGROUND_HEIGHT, cfg.FLOOR_SIZE, cfg.PLAYER_SPEED,
                      cfg.SCREEN_WIDTH // cfg.FLOOR_SIZE + 2) for i in
            range(cfg.SCREEN_WIDTH // cfg.FLOOR_SIZE + 2)]

        # Изначальное время появления шипов
        self.last_obstacle_time = pg.time.get_ticks()
        self.next_obstacle_time = cfg.OBSTACLE_FREQUENCY_LOWER

        # Создание счетчика перепрыгнутых шипов
        self.spike_count = 0
        self.font = pg.font.SysFont('comic sans', 20)

        # Инициализация фона
        self.background_image = pg.transform.scale(pg.image.load("src/sprites/background.png"),
                                                   (cfg.SCREEN_WIDTH, cfg.BACKGROUND_HEIGHT))

        self.running = True

    # Игровой цикл
    def run(self):
        while self.running:
            self.update_game_logic()
            self.draw()
            self.handle_events()
            self.check_collisions()

            # Обновление экрана и игрового времени
            pg.display.update()
            self.clock.tick(60)

        # Завершение работы
        print(f"Счет: {self.spike_count}")
        pg.quit()
        sys.exit()

    # Отрисовка фона, пола, шипов, клеток пола, линии разделения пола и счетчика
    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for tile in self.floor_tiles:
            tile.draw(self.screen)

        pg.draw.line(self.screen, (200, 200, 200), (0, cfg.BACKGROUND_HEIGHT),
                     (cfg.SCREEN_WIDTH, cfg.BACKGROUND_HEIGHT), 4)

        spike_counter_text = self.font.render(f"Появилось шипов: {self.spike_count}", True, (255, 200, 255))
        self.screen.blit(spike_counter_text, (10, 10))

    # Метод считывания нажатий клавиш клавиатуры
    def handle_events(self):
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False

                if event.key == pg.K_SPACE:
                    self.jumping = True
            if event.type == pg.KEYUP:
                self.jumping = False
        if self.jumping:
            self.player.jump()

    # Логика игры
    def update_game_logic(self):
        self.player.update()

        # Физика появления шипов на экране не реже OBSTACLE_FREQUENCY_UPPER и не чаще OBSTACLE_FREQUENCY_LOWER
        time_now = pg.time.get_ticks()

        if time_now - self.last_obstacle_time > self.next_obstacle_time:
            # Обновление времени появления шипов
            self.next_obstacle_time = rnd.randrange(cfg.OBSTACLE_FREQUENCY_LOWER, cfg.OBSTACLE_FREQUENCY_UPPER)
            self.last_obstacle_time = time_now

            # Гарантированное создание нового шипа
            obstacle_type = rnd.random()
            self.obstacles.append(
                Obstacle(cfg.SCREEN_WIDTH + cfg.OBSTACLE_SIZE, cfg.BACKGROUND_HEIGHT - cfg.OBSTACLE_SIZE,
                         cfg.OBSTACLE_SIZE,
                         cfg.PLAYER_SPEED))
            self.spike_count += 1

            # Создание второго шипа если шип двойной или тройной
            if obstacle_type >= 1 - cfg.TRIPLE_PROBABILITY - cfg.DOUBLE_PROBABILITY:
                self.obstacles.append(
                    Obstacle(cfg.SCREEN_WIDTH + 2 * cfg.OBSTACLE_SIZE, cfg.BACKGROUND_HEIGHT - cfg.OBSTACLE_SIZE,
                             cfg.OBSTACLE_SIZE,
                             cfg.PLAYER_SPEED))
                self.spike_count += 1

            # Создание третьего шипа  если шип тройной
            if obstacle_type >= 1 - cfg.TRIPLE_PROBABILITY:
                self.obstacles.append(
                    Obstacle(cfg.SCREEN_WIDTH + 3 * cfg.OBSTACLE_SIZE, cfg.BACKGROUND_HEIGHT - cfg.OBSTACLE_SIZE,
                             cfg.OBSTACLE_SIZE,
                             cfg.PLAYER_SPEED))
                self.spike_count += 1

        # Обновление шипов на экране с помощью создания нового списка прогружаемых препятствий
        # Позволяет избежать обновления списка шипов внутри цикла на списке шипов и сдвига препятствий при удалении
        new_obstacles = []
        for obstacle in self.obstacles:
            obstacle.update()

            if obstacle.x > -cfg.OBSTACLE_SIZE:
                new_obstacles.append(obstacle)

        self.obstacles = new_obstacles

        for tile in self.floor_tiles:
            tile.update()

    # Метод проверки столкновения игрока с шипом
    def check_collisions(self):
        # Создание хитбоксов шипов и игрока для слежки для столкновениями
        player_rect = pg.Rect(self.player.x, self.player.y, cfg.PLAYER_SIZE, cfg.PLAYER_SIZE)

        for obstacle in self.obstacles:
            obstacle_rect = pg.Rect(obstacle.x + cfg.OBSTACLE_SIZE / 3, obstacle.y + cfg.OBSTACLE_SIZE / 3,
                                    cfg.OBSTACLE_SIZE / 2, cfg.OBSTACLE_SIZE / 2)

            # Физика столкновения и завершения игры
            if player_rect.colliderect(obstacle_rect):
                self.running = False
