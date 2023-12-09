import pygame.mixer_music

from settings.settings import Settings

"""
    Класс для хранения и воспроизведения звуков в игре.
"""


class Sounds:

    def __init__(self):
        self.shoot = pygame.mixer.Sound("sounds/shoot.ogg")
        self.alarm = pygame.mixer.Sound("sounds/alarm.ogg")
        self.add_score = pygame.mixer.Sound("sounds/add_score.ogg")
        self.headshot = pygame.mixer.Sound("sounds/headshot.ogg")
        self.click = pygame.mixer.Sound("sounds/click.ogg")


    def play_shoot(self):
        if Settings.sounds:
            self.shoot.play()

    def play_alarm(self):
        if Settings.sounds:
            self.alarm.play()

    def play_add_score(self):
        if Settings.sounds:
            self.add_score.play()

    def play_headshot(self):
        if Settings.sounds:
            self.headshot.play()

    def play_click(self):
        if Settings.sounds:
            self.click.play()
