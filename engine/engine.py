from engine.font.font import Font
from settings.settings import Settings
from targets.target import Target


class Engine:

    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.timing = 5
        self.adding_seconds = 10

        self.score = 1000

        self.targets_list = []

    def draw(self, scene):
        for target in self.targets_list:
            target.draw(scene)

    def act(self, delta_time, frame):
        if frame % int(1 + self.adding_seconds * delta_time * Settings.FPS) == 0 and len(self.targets_list) == 0:
            self.targets_list.append(
                Target(self.x1, self.x2, self.y1, self.y2, self.timing)
            )

        for target in self.targets_list:
            target.act(delta_time)
            if not target.enabled:
                self.targets_list.remove(target)

    def click_mouse(self, x, y):
        for target in self.targets_list:
            if target.rect.collidepoint(x, y):
                point_x = target.width - abs(target.rect.center[0] - x)
                point_y = target.height - abs(target.rect.center[1] - y)

                points = (point_x + point_y) // 2
                self.score += points
                self.targets_list.remove(target)
                self.adding_seconds += 1