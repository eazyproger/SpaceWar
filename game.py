import pygame

from game_settings import Settings
from space_warrior import SpaceWarrior
from game_stats import GameStats
from button import  Button
from scoreboard import Scoreboard
import game_functions as gf


def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width,
                                      settings.screen_height))
    pygame.display.set_caption('Space War')
    play_button = Button(settings, screen, 'Play')
    spaceWarrior = SpaceWarrior(screen, settings)
    aliens = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    gf.create_fleet(settings, screen, aliens, spaceWarrior)
    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)

    # draw cycle
    while True:
        gf.check_events(settings, stats, screen, sb, spaceWarrior, aliens,
                        bullets, play_button)
        if stats.game_active:
            spaceWarrior.update()
            gf.update_aliens(settings, stats, screen, sb, spaceWarrior,
                             aliens, bullets)
            gf.update_bullets(settings, screen, stats, sb, spaceWarrior, aliens, bullets)
        gf.update_screen(settings, stats, sb, screen, spaceWarrior, aliens,
                         bullets, play_button)


run_game()
