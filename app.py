import pygame
import sys

pygame.init()

screen_width = 1200
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pygame Sample")

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

ship_width = 40
ship_height = 60
ship_x = (screen_width - ship_width) // 2
ship_y = screen_height - ship_height - 50

spaceship_img = pygame.image.load("spaceship.png").convert_alpha()  # convert_alpha keeps transparency
spaceship_img = pygame.transform.scale(spaceship_img, (40, 60))  # Resize if needed
speed = 5

laser_width = 5
laser_height = 20
laser_speed = 10
lasers = []

fire_delay = 250  # milliseconds between shots
last_shot_time = 0

enemy_width = 50
enemy_height = 30
enemy_x = 100
enemy_y = 80
enemy_speed = 3
enemy_alive = True
enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)

running = True
clock = pygame.time.Clock()
while running:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship_x -= speed
    if keys[pygame.K_RIGHT]:
        ship_x += speed
    if keys[pygame.K_ESCAPE]:
        running = False

    # FIRE ONCE
    if keys[pygame.K_SPACE]:
        if current_time - last_shot_time > fire_delay:
            laser_x = ship_x + ship_width // 2 - laser_width // 2
            laser_y = ship_y
            lasers.append(pygame.Rect(laser_x, laser_y, laser_width, laser_height))
            last_shot_time = current_time

    # MOVE LASERS + CHECK COLLISIONS
    for laser in lasers[:]:
        laser.y -= laser_speed
        if laser.y < 0:
            lasers.remove(laser)
        elif enemy_alive and laser.colliderect(enemy_rect):
            enemy_alive = False
            lasers.remove(laser)

    # MOVE ENEMY
    if enemy_alive:
        enemy_rect.x += enemy_speed
        if enemy_rect.right >= screen_width or enemy_rect.left <= 0:
            enemy_speed = -enemy_speed

    # DRAW
    screen.fill(BLACK)
    screen.blit(spaceship_img, (ship_x, ship_y))

    for laser in lasers:
        pygame.draw.rect(screen, RED, laser)

    if enemy_alive:
        pygame.draw.rect(screen, GREEN, enemy_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()