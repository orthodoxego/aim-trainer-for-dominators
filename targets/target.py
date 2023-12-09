from random import randint

import pygame
from pygame import Rect

from settings.settings import Settings


class Target:

    def __init__(self, x1, x2, y1, y2, timing, sounds, time):
        self.time = time

        square_w = int((x2 - x1) / (1 + timing / 2))

        # square_h = min(int((y2 - y1) / (1 + timing / 2)), square_w)
        square_h = min(y2 - y1, square_w)

        self.width = randint(int(square_w / 2), square_w)
        self.height = randint(int(square_h / 2), square_h)
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

        self.vectorx = 0
        self.strafe_width = randint(int(Settings.WIDTH * 0.05), int(Settings.WIDTH * 0.1))

        if self.rect.x < (x2 + x1) / 2:
            self.vectorx = self.rect.width * 2 / randint(2, 4)
        else:
            self.vectorx = -self.rect.width * 2 / randint(2, 4)

        self.first_point = self.rect.x

        self.random_mode = Settings.STOP
        if Settings.mode == Settings.RANDOM:
            r = randint(1, 3)
            if r == 1:
                self.random_mode = Settings.MOVING
            elif r == 2:
                self.random_mode = Settings.STRAFE


    def act(self, delta_time):
        if not self.enabled:
            return

        if self.color[1] > 0 and self.color[1] != 200:
            self.color[1] -= (10 / (1 / self.timing)) * delta_time
            if self.color[1] < 1:
                self.color[1] = 0

        if self.color[1] == 0:
            self.color = (200, 200, 0)
            self.destroy_step += 20 * delta_time

            if self.beeper:
                self.sounds.play_alarm()
                self.beeper = False

        elif self.color[1] == 200:
            self.color = (255, 0, 0)
            self.destroy_step += 10 * delta_time

        if Settings.mode == Settings.MOVING or self.random_mode == Settings.MOVING:
            self.run_moving(delta_time)
        elif Settings.mode == Settings.STRAFE or self.random_mode == Settings.STRAFE:
            self.run_strafe(delta_time)


        if self.destroy_step > self.timing // 2:
            self.sounds.play_bad()
            self.enabled = False

    def draw(self, scene: pygame.surface):
        if not self.enabled:
            return

        pygame.draw.rect(scene,
                         self.color,
                         self.rect,
                         0)
        pygame.draw.circle(scene,
                         (200, 255, 200),
                           (self.rect.centerx, self.rect.centery),
                         10)

    def check_vector(self, delta_time):
        if self.rect.x < self.x1 or self.rect.x + self.rect.width > self.x2:
            self.vectorx *= -1
            self.rect.x += self.vectorx * delta_time

    def run_moving(self, delta_time):
        self.rect.x += self.vectorx * delta_time
        self.check_vector(delta_time)

    def run_strafe(self, delta_time):
        self.rect.x += self.vectorx * delta_time
        if self.rect.x > self.first_point + self.strafe_width \
                or self.rect.x < self.first_point - self.strafe_width:
            self.vectorx *= -1
            self.rect.x += self.vectorx * delta_time
        self.check_vector(delta_time)
