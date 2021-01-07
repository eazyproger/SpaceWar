class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        self.spaceWar_left = self.settings.spaceWarrior_limit
        self.score = 0
        self.level = 1