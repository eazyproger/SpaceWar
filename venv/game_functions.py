import sys
from time import sleep

import pygame
from alien import Alien
from bullet import Bullet

def check_events(settings, stats, screen, sb, spaceWarrior, aliens,
                 bullets, play_button):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, spaceWarrior,
                               bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, spaceWarrior)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, stats, screen, sb, play_button, spaceWarrior, aliens, bullets, mouse_x, mouse_y)

def check_play_button(settings, stats, screen, sb, play_button, spaceWar,
                      aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        stats.reset_stats()
        settings.initialize_dynamic_settings()
        stats.game_active = True
        aliens.empty()
        bullets.empty()
        create_fleet(settings,screen, aliens, spaceWar)
        spaceWar.center_spaceWar()
        pygame.mouse.set_visible(False)
        sb.prep_score()
        sb.prep_level()
        sb.prep_high_score()
        sb.prep_space_war()

def check_keydown_events(event, settings, screen, spaceWarrior, bullets):
    if event.key == pygame.K_RIGHT:
        spaceWarrior.moving_right = True
    elif event.key == pygame.K_LEFT:
        spaceWarrior.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, spaceWarrior, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()

def check_keyup_events(event, spaceWarrior):
    if event.key == pygame.K_RIGHT:
        spaceWarrior.moving_right = False
    elif event.key == pygame.K_LEFT:
        spaceWarrior.moving_left = False

def update_screen(settings, stats, sb, screen, spaceWarrior, aliens,
                  bullets, play_button):
    screen.fill(settings.space_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    spaceWarrior.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_aliens(settings, stats, screen, sb, spaceWar, aliens, bullets):
    check_fleet_edges(settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(spaceWar, aliens):
        spaceWar_hit(settings, stats, screen, sb, spaceWar, aliens, bullets)
    check_aliens_bootom(settings, stats, screen, sb, spaceWar, aliens, bullets)

def update_bullets(settings, screen, stats, sb, spaceWar, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(settings, screen, stats, sb, spaceWar, aliens, bullets)

def fire_bullet(settings, screen, spaceWarrior, bullets):
    if len(bullets) < settings.bullet_allowed:
        new_bullet = Bullet(settings, screen, spaceWarrior)
        bullets.add(new_bullet)

def create_fleet(settings, screen, aliens, spaceWar):
    alien = Alien(settings, screen)
    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, spaceWar.rect.height,
                                  alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(settings, alien_width):
    available_space_x = settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(settings, screen, aliens, alien_number, row_number):
    alien = Alien(settings, screen)
    alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.y = alien.rect.height * 2 + 1.5 * alien.rect.height * row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)

def get_number_rows(settings, spaceWar_height, alien_height):
    available_space_y = settings.screen_height - 3 * alien_height \
                        - spaceWar_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def check_fleet_edges(settings, aliens):
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break

def change_fleet_direction(settings, aliens):
    for alien in aliens:
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1

def check_bullet_alien_collision(settings, screen, stats, sb, spaceWar, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
        check_high_score(stats, sb)
        sb.prep_score()
    if len(aliens) == 0:
        stats.level += 1
        sb.prep_level()
        bullets.empty()
        settings.increase_speed()
        create_fleet(settings, screen, aliens, spaceWar)

def spaceWar_hit(settings, stats, screen, sb, spaceWar, aliens, bullets):
    if stats.spaceWar_left > 1:
        stats.spaceWar_left -= 1
        sb.prep_space_war()
        aliens.empty()
        bullets.empty()
        create_fleet(settings, screen, aliens, spaceWar)
        spaceWar.center_spaceWar()
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bootom(settings, stats, screen, sb, spaceWar, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            spaceWar_hit(settings, stats, screen, sb, spaceWar, aliens, bullets)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()