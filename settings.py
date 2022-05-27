class Settings:

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (11, 20, 25)
        self.ship_speed = 1.5
        # Bullet settings
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
        # Star settings
        self.min_star_size = 5
        self.max_star_size = 15
        # Alien settings
        self.alien_speed = 0.2
        self.fleet_drop_speed = 50
        self.fleet_direction = 1
