import pygame

from settings.settings import Settings
from dataclasses import dataclass

@dataclass
class MovingText:
    x: float
    y: float
    speed_y: float
    txt: str
    render_txt: str
    render_black: str
    score: int

"""
    Класс для хранения и вывода текста на экран.
"""
class Font:

    def __init__(self, engine):
        self.engine = engine
        self.font = pygame.font.Font("engine/font/victor_mono_bold.ttf", 28)
        self.score_text = ""
        self.fire_text = ""
        self.reaction_text = ""
        self.score_render = None
        self.score_render_black = None
        self.fire_render = None
        self.fire_render_black = None
        self.reaction_render = None
        self.reaction_render_black = None

        self.moving_text_lists = []

    def add_moving_text(self, stroke, score):
        self.moving_text_lists.append(MovingText(
                x=Settings.WIDTH - 217,
                y=int(Settings.HEIGHT * 0.35),
                speed_y=Settings.HEIGHT // 2,
                txt=stroke,
                render_txt=None,
                render_black=None,
                score=score
        ))

    def act(self, delta_time):
        for moving_text in self.moving_text_lists:
            moving_text.y -= int(moving_text.speed_y * delta_time)
            moving_text.speed_y *= 0.98
            if moving_text.speed_y < 50:
                moving_text.speed_y = 50
            if moving_text.y < 50:
                self.engine.adding_score(moving_text.score)
                self.moving_text_lists.remove(moving_text)
    """
    Формирует строки для вывода и проверяет, изменились ли они с предыдущей отрисовки.
    Если строки изменились, то вызывается перерисовка (if).
    """
    def draw(self, scene, score, count_firing, reaction_time):
        score_text =    f"   Очки: {score}"
        fire_text =     f"Зачтено: {count_firing}"

        if reaction_time > 1000:
            reaction_time = round(reaction_time / 1000, 2)
            reaction_text = f"Реакция: {reaction_time} с."
        else:
            reaction_text = f"Реакция: {reaction_time} мс."

        if self.score_text != score_text:
            self.score_render = self.font.render(score_text, False, (255, 128, 0))
            self.score_render_black = self.font.render(score_text, False, (20, 0, 0))
            self.score_text = score_text
        if self.fire_text != fire_text:
            self.fire_render = self.font.render(fire_text, False, (255, 200, 0))
            self.fire_render_black = self.font.render(fire_text, False, (20, 0, 0))
            self.fire_text = score_text
        if self.reaction_text != reaction_text:
            self.reaction_render = self.font.render(reaction_text, False, (255, 200, 0))
            self.reaction_render_black = self.font.render(reaction_text, False, (20, 0, 0))
            self.reaction_text = reaction_text


        pygame.draw.rect(scene, (37, 37, 37), (Settings.WIDTH - 400, 0, 400, 200))

        scene.blit(self.score_render_black, (Settings.WIDTH - 353, 47))
        scene.blit(self.score_render, (Settings.WIDTH - 353, 45))

        scene.blit(self.fire_render_black, (Settings.WIDTH - 353, 87))
        scene.blit(self.fire_render, (Settings.WIDTH - 353, 85))

        scene.blit(self.reaction_render_black, (Settings.WIDTH - 353, 127))
        scene.blit(self.reaction_render, (Settings.WIDTH - 353, 125))

        for moving_text in self.moving_text_lists:
            if moving_text.render_txt is None:
                moving_text.render_txt = self.font.render(moving_text.txt, False, (50, 200, 100))
                moving_text.render_black = self.font.render(moving_text.txt, False, (20, 0, 0))

            scene.blit(moving_text.render_black, (moving_text.x, moving_text.y + 2))
            scene.blit(moving_text.render_txt, (moving_text.x, moving_text.y))
