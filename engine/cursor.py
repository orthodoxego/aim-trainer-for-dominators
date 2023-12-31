from random import randint

import pygame


class Cursor:

    def __init__(self, img):
        self.img = img

        self.corrx = 0
        self.corry = 0
        self.recoil_correct = 1

    def act(self, delta_time):
        if self.corrx > 1:
            self.corrx -= abs(self.corrx) * delta_time * self.recoil_correct
        elif self.corrx < -1:
            self.corrx += abs(self.corrx) * delta_time * self.recoil_correct
        else:
            self.corrx = 0

        if self.corry > 1:
            self.corry -= max(abs(self.corry * 4), 100) * delta_time * self.recoil_correct
        elif self.corry < -1:
            self.corry += max(abs(self.corry * 4), 100) * delta_time * self.recoil_correct
        else:
            self.corry = 0
            self.recoil_correct = 1

    def draw(self, scene):
        scene.blit(self.img, (pygame.mouse.get_pos()[0] - 16 + self.corrx, pygame.mouse.get_pos()[1] - 16 + self.corry))

    def recoil(self):
        self.corrx += randint(int(-6 * self.recoil_correct), int(5 * self.recoil_correct * 2))
        if self.corrx > 120:
            self.corrx = 120
        elif self.corrx < -120:
            self.corrx = -120

        self.corry += randint(int(-7 * self.recoil_correct), int(-4 * self.recoil_correct))

        if self.corry < -300:
            self.corry = -300 + randint(10, 30)

    def increase_recoil(self):
        if self.recoil_correct == 1:
            self.recoil_correct = 1.5
            return

        self.recoil_correct *= 1.3
        if self.recoil_correct > 12:
            self.recoil_correct = 12 - randint(5, 7)