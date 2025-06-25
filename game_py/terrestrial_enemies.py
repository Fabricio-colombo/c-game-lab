import os
import pygame
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class TerrestrialEnemies:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.enemies = []
        enemy_path = os.path.join(BASE_DIR, "img", "enemies-img", "enemy3.png")
        img = pygame.image.load(enemy_path).convert_alpha()
        self.enemy_img = pygame.transform.scale(img, (img.get_width() // 12, img.get_height() // 12))
        self.spawn_timer = 0

    def spawn_enemy(self):
        self.spawn_timer += 1
        if self.spawn_timer > 746:
            rect = self.enemy_img.get_rect()
            rect.x = self.screen_width
            rect.y = self.screen_height - rect.height - 50
            self.enemies.append(rect)
            self.spawn_timer = 0

    def move_enemies(self):
        for i, rect in enumerate(self.enemies):
            rect.x -= 8 
            self.enemies[i] = rect
        self.enemies = [r for r in self.enemies if r.x + r.width > 0]

    def check_collision(self, hero_rect):
        for rect in self.enemies:
            if hero_rect.colliderect(rect):
                return True
        return False

    def draw(self, screen):
        for rect in self.enemies:
            screen.blit(self.enemy_img, rect)
