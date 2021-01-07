import pygame.font
from pygame.sprite import Group
from space_warrior import SpaceWarrior

class Scoreboard:
    def __init__(self, settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.settings = settings

        self.text_color = (255, 255, 255    )
        self.font = pygame.font.SysFont(None, 36)
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_space_war()

    def prep_score(self):
        rounded_score = round(self.stats.score, -1)
        score_str = "Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.settings.space_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.settings.screen_width - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.space_wars.draw(self.screen)

    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "High score: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color,
                                                 self.settings.space_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = 20

    def prep_level(self):
        level = 'Lvl: ' + str(self.stats.level)
        self.level_image = self.font.render(level, True, self.text_color,
                                            self.settings.space_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 5

    def prep_space_war(self):
        self.space_wars = Group()
        for space_war_number in range(self.stats.spaceWar_left):
            space_war = SpaceWarrior(self.screen, self.settings)
            space_war.rect.x = 10 + space_war_number * space_war.rect.width
            space_war.rect.y = 10
            self.space_wars.add(space_war)
