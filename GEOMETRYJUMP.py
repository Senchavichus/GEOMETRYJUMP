import pygame as pg
import sys
import random

# Инициализация библиотеки PyGame
pg.init()

# Постоянные величины для физики игрока, логики шипов и размеров игрока, шипов, заднего фона, пола (БОЛЬШИМИ БУКВАМИ!)
WIDTH = 1980                                 # Ширина экрана
FLOOR_HEIGHT = 280                           # Высота пола
BACKGROUND_HEIGHT = 800                      # Высота заднего фона
PLAYER_SIZE = 100                            # Размеры игрока (квадрат)
OBSTACLE_SIZE = 100                          # Размеры препятствий (квадрат, но сам спрайт шипа треугольный)
GRAVITY = 2                                  # Величина гравитации в физике игры
JUMP_STRENGTH = -30                          # Начальная скорость по вертикали после прыжка игрока
PLAYER_SPEED = 30                            # Скорость игрока/шипов
OBSTACLE_FREQUENCY_LOWER = 600               # Нижняя граница частоты появления шипов
OBSTACLE_FREQUENCY_UPPER = 1800              # Верхняя граница частоты появления шипов

# Создание окна для игры размером WIDTH X (FLOOR_HEIGHT + BACKGROUND_HEIGHT)
screen = pg.display.set_mode((WIDTH, FLOOR_HEIGHT + BACKGROUND_HEIGHT))
pg.display.set_caption("GEOMETRY JUMP")

# Загрузка и растяжение используемых спрайтов для игрка, шипов, заднего фона, пола под используемые константы
player_image = pg.transform.scale(pg.image.load("sprites/player.png"), (PLAYER_SIZE, PLAYER_SIZE))
background_image = pg.transform.scale(pg.image.load("sprites/background.png"), (WIDTH, BACKGROUND_HEIGHT))
floor_image = pg.transform.scale(pg.image.load("sprites/floor.png"), (WIDTH, FLOOR_HEIGHT))
obstacle_image = pg.transform.scale(pg.image.load("sprites/obstacle.png"), (OBSTACLE_SIZE, OBSTACLE_SIZE))

# Объект библиотеки PyGame для мониторинга времени
clock = pg.time.Clock()

# Начальные условия для игрока
player_pos = [150, 100]
player_vel_y = 0
on_ground = False

# Задание стартовых значений для появления шипов
last_obstacle_time = pg.time.get_ticks()
next_obstacle_time = random.randrange(OBSTACLE_FREQUENCY_LOWER, OBSTACLE_FREQUENCY_UPPER)

# Создание списка прогруженных шипов
obstacles = []

# Цикл игры
running = True
while running:
    # Создание слоев сначала заднего фона, потом пола, потом игрока
    screen.blit(background_image, (0, 0))
    screen.blit(floor_image, (0, BACKGROUND_HEIGHT))
    screen.blit(player_image, player_pos)

    # Логика нажатия клавиш
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            # Выход из игры с помощью клавиши ESCAPE
            if event.key == pg.K_ESCAPE:
                running = False
            # Прыжок происходит только при нажатии клавиши пробел и только при нахождении игрока на земле
            if event.key == pg.K_SPACE and on_ground:
                player_vel_y = JUMP_STRENGTH
                on_ground = False

    # Физика движения игрока, обновляющаяся каждый тик
    player_pos[1] += player_vel_y
    player_vel_y += GRAVITY

    # Проверка нахождения игрока на земле (при небольшом проваливании под координату земли ставит игрока на землю)
    if player_pos[1] >= BACKGROUND_HEIGHT - PLAYER_SIZE:
        player_pos[1] = BACKGROUND_HEIGHT - PLAYER_SIZE
        on_ground = True
        player_vel_y = 0

    # Физика появления шипов на экране не реже OBSTACLE_FREQUENCY_UPPER и не чаще OBSTACLE_FREQUENCY_LOWER
    time_now = pg.time.get_ticks()
    # Сравнение времени сейчас и времени появления последнего появившегося шипа
    if time_now - last_obstacle_time > next_obstacle_time:
        # Обновление времени появления следующего шипа
        next_obstacle_time = random.randrange(OBSTACLE_FREQUENCY_LOWER, OBSTACLE_FREQUENCY_UPPER)
        # Обновление времени появления последнего шипа
        last_obstacle_time = time_now
        # Создание нового шипа
        obstacles.append([WIDTH + OBSTACLE_SIZE, BACKGROUND_HEIGHT - OBSTACLE_SIZE])

    for obstacle in obstacles:
        # Физика движения шипов
        obstacle[0] -= PLAYER_SPEED
        if obstacle[0] < -OBSTACLE_SIZE:
            # Удаление шипов ушедших за экран для сохранения эффективности
            obstacles.remove(obstacle)
        else:
            # Создание слоев шипов, находящихся на экране
            screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

    # Создание хитбоксов шипов и игрока для слежки для столкновениями
    player_rect = pg.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    for obstacle in obstacles:
        obstacle_rect = pg.Rect(obstacle[0], obstacle[1], OBSTACLE_SIZE / 2, OBSTACLE_SIZE / 2)
        # Физика столкновения и завершения игры
        if player_rect.colliderect(obstacle_rect):
            running = False

    # Обновление экрана
    pg.display.update()

    # Тикрейт/фреймрейт игры
    clock.tick(60)

# Завершение работы игры после ее окончания
pg.quit()
sys.exit()
