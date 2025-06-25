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

    hero_run_img = load_image(os.path.join(BASE_DIR, "img", "hero-img", "hero-run1.png"))
    hero_down_img = load_image(os.path.join(BASE_DIR, "img", "hero-img", "hero-down.png"))
    hero_up_img = load_image(os.path.join(BASE_DIR, "img", "hero-img", "hero-up.png"))

    obstacle_img = load_image(os.path.join(BASE_DIR, "img", "obstacle-img", "2.png"), divisor=12)
    bg_img = load_background()

    hero_rect = hero_run_img.get_rect()
    hero_rect.x = 50
    hero_rect.y = HEIGHT - hero_run_img.get_height() - 50

    flying_enemies = FlyingEnemies(WIDTH, HEIGHT)
    terrestrial_enemies = TerrestrialEnemies(WIDTH, HEIGHT)

    return screen, clock, font, hero_run_img, hero_down_img, hero_up_img, hero_rect, obstacle_img, bg_img, flying_enemies, terrestrial_enemies

def handle_hero_movement(hero_rect, y_velocity, on_ground, keys):
    if keys[pygame.K_UP] and on_ground:
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
    return [o for o in obstacles if o.x + o.width > 0]

def check_collision(hero_rect, obstacles):
    for obstacle in obstacles:
        if hero_rect.colliderect(obstacle):
            return True
    return False

def draw_background(screen, bg_img):
    screen.blit(bg_img, (0, 0))

def draw(screen, bg_img, current_hero_img, hero_rect, obstacle_img, obstacles, font, score, flying_enemies, terrestrial_enemies, game_active):
    draw_background(screen, bg_img)
    screen.blit(current_hero_img, hero_rect)
    for obstacle in obstacles:
        screen.blit(obstacle_img, obstacle)
    flying_enemies.draw(screen)
    terrestrial_enemies.draw(screen)

    if game_active:
        score_text = font.render(f"Score: {score // 10}", True, BLACK)
        screen.blit(score_text, (10, 10))
    else:
        msg = font.render("Game Over! Press SPACE to restart.", True, BLACK)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))
    pygame.display.update()

def main():
    screen, clock, font, hero_run_img, hero_down_img, hero_up_img, hero_rect, obstacle_img, bg_img, flying_enemies, terrestrial_enemies = init_game()
    y_velocity = 0
    on_ground = True
    obstacles = []
    spawn_timer = 0
    score = 0
    game_active = True
    current_hero_img = hero_run_img

    while True:
        clock.tick(60)
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if game_active:
            if not on_ground:
                current_hero_img = hero_up_img
            elif keys[pygame.K_DOWN]:
                current_hero_img = hero_down_img
            else:
                current_hero_img = hero_run_img

            hero_rect.width = current_hero_img.get_width()
            hero_rect.height = current_hero_img.get_height()
            hero_rect.y = min(hero_rect.y, HEIGHT - hero_rect.height - 50)

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
                game_active = False

            score += 1

        elif not game_active and keys[pygame.K_SPACE]:
            main()
            return

        draw(screen, bg_img, current_hero_img, hero_rect, obstacle_img, obstacles, font, score, flying_enemies, terrestrial_enemies, game_active)

if __name__ == "__main__":
    main()
