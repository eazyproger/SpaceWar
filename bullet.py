import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, settings, screen, spaceWarrior):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, settings.bullet_width,
                                settings.bullet_height)
        self.rect.centerx = spaceWarrior.rect.centerx
        self.rect.top = spaceWarrior.rect.top
        self.y = float(self.rect.y)
        self.color = settings.bullet_color
        self.speed = settings.bullet_speed

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
