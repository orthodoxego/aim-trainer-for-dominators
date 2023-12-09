from random import randint

import pygame
import time

from engine.decoy import Decoy
from engine.font.font import Font
from settings.settings import Settings
from targets.target import Target
from sounds.sounds import Sounds


class Engine:

    def __init__(self, x1, x2, y1, y2, sounds):

        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        self.count_firing = 0
        self.headshot = False
        self.frame = 1
        self.timing = 1
        self.adding_seconds = 10
        self.damage = 0
        self.targets_list = []
        self.all_time = 0

        self.sounds = sounds
        self.font = Font(self)

        self.decoy_img = pygame.image.load("buttons/decoy.png")
        new_width = (x2 - x1) * 0.01
        self.decoy_img = pygame.transform.scale(self.decoy_img, (new_width, new_width))

        self.decoys = []
        self.count_riffle = 0

        self.life = x2 - x1
        self.minus_life = self.life / 230

    def draw(self, scene):

        pygame.draw.rect(scene, (10, 10, 10), (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))

        pygame.draw.rect(scene, (37, 37, 37), (self.x1, self.y2 + 5, self.y2 - self.y1, 10))
        pygame.draw.rect(scene, (100, 255, 0), (self.x1, self.y2 + 5, self.life, 10))


        if self.headshot:
            pygame.draw.rect(scene, (255, 0, 50),
                             (self.x1 * 1.25, self.y1 * 1.25, self.x2 - self.x1 * 1.5, self.y2 - self.y1 * 1.5))
            self.headshot = False

        for decoy in self.decoys:
            decoy.draw(scene)

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
                self.dec_life(2)
                self.targets_list.remove(target)

        self.frame += 1
        if self.frame > 10000:
            self.adding_seconds = 1
            self.frame = 1

        self.font.act(delta_time)

    def click_mouse(self, x, y):
        for target in self.targets_list:
            if target.enabled and target.rect.collidepoint(x, y):

                a = (x - target.rect.centerx) ** 2
                b = (y - target.rect.centery) ** 2
                c = (a + b) ** 0.5

                target.adding_shoot_random_x = randint(-2, 2)
                target.adding_shoot_random_y = randint(0, 2)

                self.headshot = False
                if c < 10:
                    dmg = 100
                    self.sounds.play_headshot()
                    self.headshot = True
                else:
                    self.sounds.play_shoot()
                    dmg = max(5, 50 - int(((c / target.rect.width + c / target.rect.height) / 4) * 100))

                self.count_riffle += 1

                if self.count_riffle >= Settings.counting_shoot_for_end_target:
                    self.targets_list.remove(target)
                    self.adding_seconds += 1
                    self.count_firing += 1
                    self.count_riffle = 0

                self.all_time += time.time() - target.time
                self.font.add_moving_text(f"+{dmg}", dmg)
                return True


        self.sounds.play_shoot()

        # Если не попадает, добавляем декой
        if x > self.x1 and x < self.x2 and y > self.y1 and y < self.y2:
            self.decoys.append(Decoy(
                x - self.decoy_img.get_width() // 2,
                y - self.decoy_img.get_height() // 2,
                self.decoy_img))
            if len(self.decoys) > 50:
                del self.decoys[0]

        self.dec_life(0.5)
        return False

    def adding_damage(self, damage):

        self.sounds.play_add_score()
        self.damage += damage

        self.timing += 0.15
        if self.timing > 60:
            self.timing = 60

    def dec_life(self, multiple):
        self.life -= self.minus_life * multiple
        if self.life < 0:
            self.life = 0