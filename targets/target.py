from random import randint

import pygame
from pygame import Rect

from settings.settings import Settings


class Target:

    def __init__(self, x1, x2, y1, y2, timing, sounds):
        self.width = randint(int(Settings.WIDTH * 0.03), int(Settings.WIDTH * 0.07))
        self.height = randint(int(Settings.WIDTH * 0.03), int(Settings.WIDTH * 0.07))
        self.rect: Rect = Rect((
                               randint(x1, int(x2 - self.width)),
                               randint(y1, int(y2 - self.height)),
                               self.width,
                               self.height
                               ))
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.timing = timing

        self.sounds = sounds
        self.beeper = True

        self.color = [255, 160, 0]
        self.enabled = True
        self.destroy_step = 0

    def act(self, delta_time):
        if not self.enabled:
            return

        if self.color[1] > 0 and self.color[1] != 200:
            self.color[1] -= 160 / self.timing * delta_time
            if self.color[1] < 1:
                self.color[1] = 0

        if self.color[1] == 0:
            self.color = (200, 200, 0)
            self.destroy_step += 10 * delta_time
            if self.beeper:
                self.sounds.play_alarm()
                self.beeper = False

        elif self.color[1] == 200:
            self.color = (255, 0, 0)
            self.destroy_step += 10 * delta_time

        if self.destroy_step > self.timing // 2:
            self.enabled = False

    def draw(self, scene: pygame.surface):
        if not self.enabled:
            return

        pygame.draw.rect(scene,
                         self.color,
                         self.rect,
                         0)
