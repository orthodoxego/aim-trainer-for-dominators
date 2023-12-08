from engine.font.font import Font
from settings.settings import Settings
from targets.target import Target
from sounds.sounds import Sounds


class Engine:

    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.count_firing = 0
        self.frame = 1
        self.timing = 5
        self.adding_seconds = 10
        self.score = 1000
        self.targets_list = []

        self.sounds = Sounds()
        self.font = Font(self)

    def draw(self, scene):
        for target in self.targets_list:
            target.draw(scene)

        self.font.draw(scene, int(self.score), self.count_firing)

    def act(self, delta_time):
        if self.frame % int(1 + self.adding_seconds * delta_time * Settings.FPS) == 0 and len(self.targets_list) == 0:
            self.targets_list.append(
                Target(self.x1, self.x2, self.y1, self.y2, self.timing, self.sounds)
            )

        for target in self.targets_list:
            target.act(delta_time)

            self.score -= (abs(target.width + target.height) // 2) * delta_time

            if not target.enabled:
                self.targets_list.remove(target)


        self.frame += 1
        if self.frame > 10000:
            self.adding_seconds = 1
            self.frame = 1

        self.font.act(delta_time)

    def click_mouse(self, x, y):
        for target in self.targets_list:
            if target.rect.collidepoint(x, y):
                self.sounds.play_shoot()
                point_x = target.width - abs(target.rect.center[0] - x)
                point_y = target.height - abs(target.rect.center[1] - y)

                points = (point_x + point_y) // 2
                self.score += points
                self.targets_list.remove(target)
                self.adding_seconds += 1
                self.count_firing += 1

                self.font.add_moving_text(f"+{points}", points)

    def adding_score(self, score):
        self.sounds.play_add_score()
        self.score += score
