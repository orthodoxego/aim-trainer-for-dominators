import pygame.image
from dataclasses import dataclass

from settings.settings import Settings


@dataclass
class Btn:
    img: pygame.image
    rect: pygame.Rect = None
    num: int = 0
    active: bool = False


class Buttons:

    def __init__(self, x1, x2, y1, y2):
        self.btns = []
        self.width_field = x2 - x1
        self.height_field = y2 - y1

        self.btns.append(Btn(self.get_scaled_img(pygame.image.load("buttons/btn0101.png"))))
        self.btns[0].rect = self.btns[0].img.get_rect()
        self.btns[0].rect.x = x1
        self.btns[0].rect.y = y1 - self.btns[0].rect.height * 1.1
        self.btns[0].num = 0
        self.btns[0].active = True

        self.btns.append(Btn(self.get_scaled_img(pygame.image.load("buttons/btn0102.png"))))
        self.btns[1].rect = self.btns[1].img.get_rect()
        self.btns[1].rect.x = x1
        self.btns[1].rect.y = y1 - self.btns[1].rect.height * 1.1
        self.btns[1].num = 1

        self.btns.append(Btn(self.get_scaled_img(pygame.image.load("buttons/btn0201.png"))))
        self.btns[2].rect = self.btns[2].img.get_rect()
        self.btns[2].rect.x = x1 + self.btns[2].rect.width * 1.025
        self.btns[2].rect.y = y1 - self.btns[2].rect.height * 1.1
        self.btns[2].num = 2
        self.btns[2].active = True

        self.btns.append(Btn(self.get_scaled_img(pygame.image.load("buttons/btn0202.png"))))
        self.btns[3].rect = self.btns[3].img.get_rect()
        self.btns[3].rect.x = x1 + self.btns[3].rect.width * 1.025
        self.btns[3].rect.y = y1 - self.btns[3].rect.height * 1.1
        self.btns[3].num = 3

        self.btns.append(Btn(self.get_scaled_img(pygame.image.load("buttons/btn0203.png"))))
        self.btns[4].rect = self.btns[4].img.get_rect()
        self.btns[4].rect.x = x1 + self.btns[4].rect.width * 1.025
        self.btns[4].rect.y = y1 - self.btns[4].rect.height * 1.1
        self.btns[4].num = 4

        self.btns.append(Btn(self.get_scaled_img(pygame.image.load("buttons/btn0301.png"))))
        self.btns[5].rect = self.btns[5].img.get_rect()
        self.btns[5].rect.x = x1 + self.btns[5].rect.width * 2.05
        self.btns[5].rect.y = y1 - self.btns[5].rect.height * 1.1
        self.btns[5].num = 5
        self.btns[5].active = True

        self.btns.append(Btn(self.get_scaled_img(pygame.image.load("buttons/btn0302.png"))))
        self.btns[6].rect = self.btns[6].img.get_rect()
        self.btns[6].rect.x = x1 + self.btns[6].rect.width * 2.05
        self.btns[6].rect.y = y1 - self.btns[6].rect.height * 1.1
        self.btns[6].num = 6
        
        self.btns.append(Btn(self.get_scaled_img(pygame.image.load("buttons/btn0401.png"))))
        self.btns[7].rect = self.btns[7].img.get_rect()
        self.btns[7].rect.x = x2 - self.btns[7].rect.width * 2.025
        self.btns[7].rect.y = y1 - self.btns[7].rect.height * 1.1
        self.btns[7].num = 7
        self.btns[7].active = True

        self.btns.append(Btn(self.get_scaled_img(pygame.image.load("buttons/btn0501.png"))))
        self.btns[8].rect = self.btns[8].img.get_rect()
        self.btns[8].rect.x = x2 - self.btns[8].rect.width
        self.btns[8].rect.y = y1 - self.btns[8].rect.height * 1.1
        self.btns[8].num = 8
        self.btns[8].active = True


        # self.btn0102 = pygame.image.load("buttons/btn0102.png")
        # self.btn0201 = pygame.image.load("buttons/btn0201.png")
        # self.btn0202 = pygame.image.load("buttons/btn0202.png")
        # self.btn0203 = pygame.image.load("buttons/btn0203.png")
        # self.btn0301 = pygame.image.load("buttons/btn0301.png")
        # self.btn0302 = pygame.image.load("buttons/btn0302.png")
        # self.btn0401 = pygame.image.load("buttons/btn0401.png")

    def get_scaled_img(self, img) -> pygame.image:
        new_width = self.width_field / 5.3
        scale = new_width / img.get_width()
        img = pygame.transform.scale(img, (new_width,
                                           img.get_height() * scale))
        return img

    def draw(self, scene):
        for btns in self.btns:
            if btns.active:
                scene.blit(btns.img, btns.rect)

    def click_mouse(self, x, y, sounds):
        btn = -1

        for b in self.btns:
            if b.active and b.rect.collidepoint(x, y):
                sounds.play_click()
                btn = b.num

        if btn == 0:    # Убрать движение
            self.btns[0].active = False
            self.btns[1].active = True
            Settings.moving = False
        elif btn == 1:  # Активировать движение
            self.btns[1].active = False
            self.btns[0].active = True
            Settings.moving = True
        elif btn == 2:  # Активировать двойной
            self.btns[2].active = False
            self.btns[3].active = True
            Settings.fire = 2
        elif btn == 3:  # Активировать тройной
            self.btns[3].active = False
            self.btns[4].active = True
            Settings.fire = 3
        elif btn == 4:  # Активировать одиночный
            self.btns[4].active = False
            self.btns[2].active = True
            Settings.fire = 1
        elif btn == 5:  # Звук откл
            self.btns[5].active = False
            self.btns[6].active = True
            Settings.sounds = False
        elif btn == 6:  # Звук вкл
            self.btns[6].active = False
            self.btns[5].active = True
            Settings.sounds = True



        return btn
