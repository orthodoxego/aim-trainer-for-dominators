import pygame

from settings.settings import Settings

"""
    Класс для хранения и вывода текста на экран.
"""


class Font:

    def __init__(self):
        self.font = pygame.font.Font("font/chava.ttf", 24)
        self.score_text = ""
        self.score_render = None
        self.score_render_black = None

    """
    Формирует строки для вывода и проверяет, изменились ли они с предыдущей отрисовки.
    Если строки изменились, то вызывается перерисовка (if).
    """

    def draw(self, scene, score):
        score_text = f"{score}"

        if self.score_text != score_text:
            self.score_render = self.font.render(score_text, False, (0, 255, 50))
            self.score_render_black = self.font.render(score_text, False, (20, 0, 0))
            self.score_text = score_text

        scene.blit(self.score_render, (Settings.WIDTH - 353, 17))
        scene.blit(self.score_render_black, (Settings.WIDTH - 353, 47))
