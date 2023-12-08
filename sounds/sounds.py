import pygame.mixer_music

"""
    Класс для хранения и воспроизведения звуков в игре.
"""


class Sounds:

    def __init__(self):
        self.shoot = pygame.mixer.Sound("sounds/shoot.ogg")
        self.alarm = pygame.mixer.Sound("sounds/alarm.ogg")
        self.add_score = pygame.mixer.Sound("sounds/add_score.ogg")


    def play_shoot(self):
        self.shoot.play()

    def play_alarm(self):
        self.alarm.play()

    def play_add_score(self):
        self.add_score.play()
