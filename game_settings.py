class Settings:
    # class with settings of game

    def __init__(self):
        # self.screen_width = 600
        # self.screen_height = 700

        self.screen_width = 1366
        self.screen_height = 768

        self.space_color = [0, 0, 0]

        self.spaceWarrior_limit = 2

        self.bullet_height = 10
        self.bullet_width = 2
        self.bullet_color = [0, 255, 163]
        self.bullet_allowed = 5

        self.fleet_drop_speed = 15

        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.spaceWarrior_speed = 1
        self.bullet_speed = 2
        self.alien_speed = 0.5
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.spaceWarrior_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.speedup_scale)