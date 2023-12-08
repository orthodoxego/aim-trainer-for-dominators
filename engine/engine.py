from random import randint

import pygame
import time

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
        self.timing = 1
        self.adding_seconds = 10
        self.damage = 0
        self.targets_list = []
        self.all_time = 0

        self.sounds = Sounds()
        self.font = Font(self)

    def draw(self, scene):

        pygame.draw.rect(scene, (10, 10, 10), (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))

        for target in self.targets_list:
            target.draw(scene)

        react_time = 0 if self.count_firing == 0 else round(self.all_time * 1000 / self.count_firing, 1)
        self.font.draw(scene, int(self.damage), self.count_firing, react_time)

    def act(self, delta_time):
        if self.frame % int(1 + self.adding_seconds * delta_time * Settings.FPS) == 0 and len(self.targets_list) == 0:
            self.targets_list.append(
                Target(self.x1, self.x2,
                       self.y1, self.y2,
                       self.timing,
                       self.sounds,
                       time.time()
                       )
            )

        for target in self.targets_list:
            target.act(delta_time)

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

                a = (x - target.rect.centerx) ** 2
                b = (y - target.rect.centery) ** 2
                c = (a + b) ** 0.5

                headshot = False

                if c < 10:
                    headshot = True
                    dmg = 100
                    self.sounds.play_headshot()
                else:
                    self.sounds.play_shoot()
                    dmg = max(5, 80 - int(((c / target.rect.width + c / target.rect.height) / 4) * 100))


                self.targets_list.remove(target)
                self.adding_seconds += 1
                self.count_firing += 1
                self.all_time += time.time() - target.time

                r = randint(900, 1300)


                self.font.add_moving_text(f"+{dmg}", dmg)

    def adding_damage(self, damage):

        self.sounds.play_add_score()
        self.damage += damage

        self.timing += 0.3
        if self.timing > 60:
            self.timing = 60
