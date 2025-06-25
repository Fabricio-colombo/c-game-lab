import os
import pygame
from flying_enemies import FlyingEnemies
from terrestrial_enemies import TerrestrialEnemies

pygame.init()

WIDTH, HEIGHT = 800, 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAVITY = 0.8

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_image(path, divisor=None, scale_factor=None):
    img = pygame.image.load(path).convert_alpha()
    if divisor:
        width = img.get_width() // divisor
        height = img.get_height() // divisor
        img = pygame.transform.scale(img, (width, height))
    elif scale_factor:
        width = int(img.get_width() * scale_factor)
        height = int(img.get_height() * scale_factor)
        img = pygame.transform.scale(img, (width, height))
    return img

def load_background():
    bg_path = os.path.join(BASE_DIR, "img", "textures-img", "newchao.jpg")
    bg_img = pygame.image.load(bg_path).convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    return bg_img

def init_game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    hero_img_path = os.path.join(BASE_DIR, "img", "hero-img", "hero-run1.png")
    hero_img = load_image(hero_img_path)  # tamanho original

    obstacle_img_path = os.path.join(BASE_DIR, "img", "obstacle-img", "2.png")
    obstacle_img = load_image(obstacle_img_path, divisor=12)  # reduzido

    bg_img = load_background()

    hero_rect = hero_img.get_rect()
    hero_rect.x = 50
    hero_rect.y = HEIGHT - hero_rect.height - 50

    flying_enemies = FlyingEnemies(WIDTH, HEIGHT)
    terrestrial_enemies = TerrestrialEnemies(WIDTH, HEIGHT)

    return screen, clock, font, hero_img, hero_rect, obstacle_img, bg_img, flying_enemies, terrestrial_enemies

def handle_hero_movement(hero_rect, y_velocity, on_ground, keys):
    if keys[pygame.K_SPACE] and on_ground:
        y_velocity = -15
        on_ground = False
    y_velocity += GRAVITY
    hero_rect.y += y_velocity
    if hero_rect.y >= HEIGHT - hero_rect.height - 50:
        hero_rect.y = HEIGHT - hero_rect.height - 50
        y_velocity = 0
        on_ground = True
    return hero_rect, y_velocity, on_ground

def spawn_obstacle(obstacles, obstacle_img, spawn_timer):
    spawn_timer += 1
    if spawn_timer > 60:
        obstacle = obstacle_img.get_rect()
        obstacle.x = WIDTH
        obstacle.y = HEIGHT - obstacle.height - 50
        obstacles.append(obstacle)
        spawn_timer = 0
    return obstacles, spawn_timer

def move_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle.x -= 8
    obstacles = [o for o in obstacles if o.x + o.width > 0]
    return obstacles

def check_collision(hero_rect, obstacles):
    for obstacle in obstacles:
        if hero_rect.colliderect(obstacle):
            return True
    return False

def draw_background(screen, bg_img):
    screen.blit(bg_img, (0, 0))

def draw(screen, bg_img, hero_img, hero_rect, obstacle_img, obstacles, font, score, flying_enemies, terrestrial_enemies):
    draw_background(screen, bg_img)
    screen.blit(hero_img, hero_rect)
    for obstacle in obstacles:
        screen.blit(obstacle_img, obstacle)
    flying_enemies.draw(screen)
    terrestrial_enemies.draw(screen)
    score_text = font.render(f"Score: {score // 10}", True, BLACK)
    screen.blit(score_text, (10, 10))
    pygame.display.update()

def main():
    screen, clock, font, hero_img, hero_rect, obstacle_img, bg_img, flying_enemies, terrestrial_enemies = init_game()
    y_velocity = 0
    on_ground = True
    obstacles = []
    spawn_timer = 0
    score = 0
    run = True

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        hero_rect, y_velocity, on_ground = handle_hero_movement(hero_rect, y_velocity, on_ground, keys)
        obstacles, spawn_timer = spawn_obstacle(obstacles, obstacle_img, spawn_timer)
        obstacles = move_obstacles(obstacles)

        flying_enemies.spawn_enemy()
        flying_enemies.move_enemies()

        terrestrial_enemies.spawn_enemy()
        terrestrial_enemies.move_enemies()

        if (check_collision(hero_rect, obstacles) or
            flying_enemies.check_collision(hero_rect) or
            terrestrial_enemies.check_collision(hero_rect)):
            run = False

        score += 1
        draw(screen, bg_img, hero_img, hero_rect, obstacle_img, obstacles, font, score, flying_enemies, terrestrial_enemies)

    pygame.quit()

if __name__ == "__main__":
    main()