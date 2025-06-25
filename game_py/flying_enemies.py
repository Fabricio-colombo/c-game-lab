import os
import pygame
import random


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class FlyingEnemies:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemies = []
        self.spawn_timer = 0

        self.enemy_imgs = []
        paths = [
            os.path.join(BASE_DIR, "img", "enemies-img", "enemy1.png"),
            os.path.join(BASE_DIR, "img", "enemies-img", "enemy2.png"),
        ]
        for path in paths:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (img.get_width() // 12, img.get_height() // 12))
            self.enemy_imgs.append(img)

    def spawn_enemy(self):
        self.spawn_timer += 1
        if self.spawn_timer > 120:
            img = random.choice(self.enemy_imgs)
            rect = img.get_rect()
            rect.x = self.screen_width
            rect.y = random.choice([self.screen_height - 200, self.screen_height - 150, self.screen_height - 100])
            self.enemies.append((rect, img))
            self.spawn_timer = 0

    def move_enemies(self):
        for i, (rect, img) in enumerate(self.enemies):
            rect.x -= 10
            self.enemies[i] = (rect, img)
        self.enemies = [(r, i) for (r, i) in self.enemies if r.x + r.width > 0]

    def check_collision(self, hero_rect):
        for rect, img in self.enemies:
            if hero_rect.colliderect(rect):
                return True
        return False

    def draw(self, screen):
        for rect, img in self.enemies:
            screen.blit(img, rect)
