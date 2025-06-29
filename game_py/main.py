import os
import pygame
import numpy as np
from ai_player import AIPlayer
from genetic import GeneticAlgorithm
from best_player import save_best
from flying_enemies import FlyingEnemies
from terrestrial_enemies import TerrestrialEnemies
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from visualizar_pkl import show_best_info


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

    hero_imgs = {
        "run": load_image(os.path.join(BASE_DIR, "img", "hero-img", "hero-run1.png")),
        "down": load_image(os.path.join(BASE_DIR, "img", "hero-img", "hero-down.png")),
        "up": load_image(os.path.join(BASE_DIR, "img", "hero-img", "hero-up.png"))
    }

    obstacle_img = load_image(os.path.join(BASE_DIR, "img", "obstacle-img", "2.png"), divisor=12)
    bg_img = load_background()
    flying_enemies = FlyingEnemies(WIDTH, HEIGHT)
    terrestrial_enemies = TerrestrialEnemies(WIDTH, HEIGHT)

    return screen, clock, font, hero_imgs, obstacle_img, bg_img, flying_enemies, terrestrial_enemies

def get_next_obstacle_info(obstacles, hero_rect):
    for obs in obstacles:
        if obs.x + obs.width > hero_rect.x:
            dist = obs.x - hero_rect.x
            height = obs.height
            return [dist / WIDTH, height / HEIGHT, 1.0] 
    return [1.0, 0.0, 0.0] 

def simulate_player(ai_player, screen, clock, font, hero_imgs, obstacle_img, bg_img, flying_enemies, terrestrial_enemies, show=False):
    hero_rect = hero_imgs["run"].get_rect()
    hero_rect.x = 50
    hero_rect.y = HEIGHT - hero_imgs["run"].get_height() - 50

    y_velocity = 0
    on_ground = True
    obstacles = []
    spawn_timer = 0
    score = 0
    alive = True
    current_hero_img = hero_imgs["run"]

    while alive and score < 3000:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        inputs = get_next_obstacle_info(obstacles, hero_rect)
        action = ai_player.decide(inputs) if inputs[2] > 0 else 0

        if action == 1 and on_ground:
            y_velocity = -15
            on_ground = False
        elif action == 2:
            current_hero_img = hero_imgs["down"]
        else:
            current_hero_img = hero_imgs["run"] if on_ground else hero_imgs["up"]

        y_velocity += GRAVITY
        hero_rect.y += y_velocity
        if hero_rect.y >= HEIGHT - hero_rect.height - 50:
            hero_rect.y = HEIGHT - hero_rect.height - 50
            y_velocity = 0
            on_ground = True

        hero_rect.width = current_hero_img.get_width()
        hero_rect.height = current_hero_img.get_height()

        spawn_timer += 1
        if spawn_timer > 166:
            obstacle = obstacle_img.get_rect()
            obstacle.x = WIDTH
            obstacle.y = HEIGHT - obstacle.height - 50
            obstacles.append(obstacle)
            spawn_timer = 0
        for obstacle in obstacles:
            obstacle.x -= 8
        obstacles = [o for o in obstacles if o.x + o.width > 0]

        flying_enemies.spawn_enemy()
        flying_enemies.move_enemies()
        terrestrial_enemies.spawn_enemy()
        terrestrial_enemies.move_enemies()

        hero_hitbox = hero_rect.inflate(-hero_rect.width * 0.4, -hero_rect.height * 0.2)
        if any(hero_hitbox.colliderect(o) for o in obstacles) or \
           flying_enemies.check_collision(hero_hitbox) or \
           terrestrial_enemies.check_collision(hero_hitbox):
            alive = False

        if show:
            screen.blit(bg_img, (0, 0))
            screen.blit(current_hero_img, hero_rect)
            for obs in obstacles:
                screen.blit(obstacle_img, obs)
            flying_enemies.draw(screen)
            terrestrial_enemies.draw(screen)

            score_text = font.render(f"Score: {score // 10}", True, BLACK)
            screen.blit(score_text, (10, 10))
            pygame.display.update()

        score += 1

    return score

def main():
    screen, clock, font, hero_imgs, obstacle_img, bg_img, flying_enemies, terrestrial_enemies = init_game()
    ga = GeneticAlgorithm(pop_size=30, input_size=3)

    while True:
        fitnesses = []
        for i, player in enumerate(ga.population):
            score = simulate_player(player, screen, clock, font, hero_imgs, obstacle_img, bg_img, flying_enemies, terrestrial_enemies, show=(i == 0))
            fitnesses.append(score)
            print(f"Jogador {i + 1} - Score: {score}")

        best_index = np.argmax(fitnesses)
        save_best(ga.population[best_index])

        print(f"\n--- Geracao {ga.generation} - Melhor Score: {max(fitnesses)} ---\n")
        ga.evolve(fitnesses)

        screen.fill(WHITE)
        text = font.render(f"Nova Geracao: {ga.generation}", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.update()
        pygame.time.delay(2000)

        best = ga.population[best_index]
        simulate_player(best, screen, clock, font, hero_imgs, obstacle_img, bg_img, flying_enemies, terrestrial_enemies, show=True)
        show_best_info()

if __name__ == "__main__":
    main()
