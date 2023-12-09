import pygame
import datetime


class EndStage:


    def __init__(self, x1, x2, y1, y2, data_dict):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.data_dict = data_dict

        # data_dict['damage'] = 700
        # data_dict['all_firing'] = 7
        # data_dict['average_reaction'] = 1.8
        # data_dict['missed_the_target'] = 3
        # data_dict['missed_the_figure'] = 50

        self.font = pygame.font.Font("engine/font/victor_mono_bold.ttf", 20)
        ver_live = 0 if data_dict['all_firing'] == 0 \
            else ((data_dict['damage'] / (data_dict['all_firing'] * 100) * 100) /
                  max(data_dict['average_reaction'], 1) / (0.7 + data_dict['average_reaction']) /
                  max(data_dict['missed_the_figure'], 1))
        ver_live = min(min(ver_live, 95), ver_live)
        out_txt = f"""
------------------------------------------`
               РЕЗУЛЬТАТЫ:`
------------------------------------------`
     Общий нанесённый урон: {data_dict['damage']} hp.`
  Попадание в центр фигуры: {data_dict['headshot']}`
        Всего выбито фигур: {data_dict['all_firing']}`
 Выживание в прямой стычке: {round(ver_live, 2)}%`
     Среднее время реакции: {data_dict['average_reaction']} сек.`
       Выстрелов мимо цели: {data_dict['missed_the_target']}`
           Пропущено фигур: {data_dict['missed_the_figure']}`
------------------------------------------`
Ваши результаты записаны в файл result.txt`
Нажмите управляющие кнопки для продолжения`
"""
        self.render = []
        out_txt = out_txt.replace("\n", "")

        # Должен быть нанесён урон и совершён выстрел для записи в файл
        if data_dict['damage'] > 0 and data_dict['all_firing'] > 0:
            with open("result.txt", "a", encoding="UTF-8") as f:
                t = datetime.datetime.now()
                f.write(f"Зафиксировано: {t.hour}:{t.minute}:{t.second} {t.day}.{t.month}.{t.year}\n")
                out = out_txt.split("`")
                for i in range(len(out) - 3):
                    f.write(f"{out[i]}\n")
                f.write("\n")
                f.close()

        for s in out_txt.split("`"):
            self.render.append(self.font.render(s, False, (255, 200, 0)))

        self.end_training = False
        pass

    def act(self, delta_time):
        pass

    def draw(self, scene):
        pygame.draw.rect(scene, (37, 37, 37), (self.x1, self.y1, self.x2 - self.x1, self.y2 - self.y1))

        stroke = 0
        for render in self.render:
            scene.blit(render, (self.x1 * 1.02, self.y1 * 1.02 + stroke * 30))
            stroke += 1

    def click_mouse(self, x, y):
        pass