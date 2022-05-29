class GameStatus:

    def __init__(self, game):
        self.settings = game.settings
        self.ships_left = None
        self.reset_status()
        self.game_active = False
        self.score = 0
        self.high_score = 0
        self.level = 1

    def reset_status(self):
        self.ships_left = self.settings.ship_limit

