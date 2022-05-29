class Settings:

    def __init__(self):
        self.alien_speed = None
        self.bullet_speed = None
        self.ship_speed = None
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (11, 20, 25)
        self.ship_limit = 3
        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Star settings
        self.min_star_size = 5
        self.max_star_size = 15
        # Alien settings
        self.fleet_drop_speed = 50
        self.fleet_direction = 1
        self.alien_score = 50
        # How quickly the game speeds up
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.07

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
