import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_status import GameStatus
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.game_status = GameStatus(self)
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self.create_fleet()
        self.create_stars()

        self.play_button = Button(self, "Let's Go")
        self.score_board = ScoreBoard(self)

    def run_game(self):
        while True:
            self._check_events()
            if self.game_status.game_active:
                self.ship.update()
                self.bullets.update()
                self.update_bullets()
                self._update_aliens()

            self._update_screen()

    def update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.game_status.score += self.settings.alien_score * len(aliens)
            self.score_board.prep_score()
            self.score_board.check_high_score()

        if not self.aliens:
            self.create_fleet()
            self.bullets.empty()
            self.settings.increase_speed()

            self.game_status.level += 1
            self.score_board.prep_level()

    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        ship_rect = self.ship.rect
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom - ship_rect.height:
                self._ship_hit()
                break

    def create_stars(self):
        for starCount in range(50):
            star = Star(self)
            self.stars.add(star)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_aliens_y = available_space_y // (2 * alien_height)

        for row_number in range(number_aliens_y):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)

    def create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_events(self):
        for event in pygame.event.get():
            # What for keyboard and mouse events
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_status.game_active:
            self.start_game()

    def start_game(self):
        self.game_status.reset_status()
        self.game_status.game_active = True

        # Get rid of the remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet and center the ship
        self.create_fleet()
        self.ship.center_ship()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset the game settings
        self.settings.initialize_dynamic_settings()

        # Reset the game score
        self.game_status.score = 0
        self.score_board.prep_score()
        self.score_board.prep_ships()

    def fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _ship_hit(self):
        if self.game_status.ships_left > 0:
            self.game_status.ships_left -= 1

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center the ship
            self.create_fleet()
            self.ship.center_ship()
            self.score_board.prep_ships()

            # Pause
            sleep(0.5)
        else:
            self.game_status.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        # Redraw the screen
        self.screen.fill(self.settings.bg_color)
        self.ship.blit()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.stars.draw(self.screen)

        # Draw the play button if game is inactive
        if not self.game_status.game_active:
            self.play_button.draw_button()

        # Draw the scoreboard
        self.score_board.draw_score()

        # Make the most recently drawn screen visible
        pygame.display.flip()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_p:
            self.start_game()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


if __name__ == '__main__':
    alien_invasion = AlienInvasion()
    alien_invasion.run_game()
