import pygame.font
from pygame.sprite import Group
from ship import Ship


class ScoreBoard:

    def __init__(self, game):
        self.ships = None
        self.game = game
        self.level_rect = None
        self.level_image = None
        self.high_score_rect = None
        self.high_score_image = None
        self.score_rect = None
        self.score_image = None
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings
        self.game_status = game.game_status

        self.text_color = (230, 230, 30)
        self.font = pygame.font.SysFont(None, 28)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        rounded_score = round(self.game_status.score)
        score_str = "Your Score: {:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        rounded_score = round(self.game_status.high_score)
        high_score_str = "High Score: {:,}".format(rounded_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Center the high score at the center of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        level_str = "Level : " + str(self.game_status.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 20
        self.level_rect.top = self.score_rect.bottom + 30

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.game_status.ships_left):
            ship = Ship(self.game)
            ship.image = pygame.transform.scale(ship.image, (30, 30))
            ship.rect = ship.image.get_rect()
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def draw_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        if self.game_status.score > self.game_status.high_score:
            self.game_status.high_score = self.game_status.score
            self.prep_high_score()
