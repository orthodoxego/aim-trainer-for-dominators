# Если отсутствуют библиотеки, выполнить следующие команды
# в терминале Windows (или в виртуальном окружении)
# pip install pygame
# pip install pywin32
# pip install pyautogui

import ctypes
import pyautogui
import pygame
import win32api
import win32con
import win32gui
import time

from buttons.buttons import Buttons
from ctypes import wintypes
from random import randint

from engine.cursor import Cursor
from engine.engine import Engine
from engine.font.end_stage import EndStage

from settings.settings import Settings
from sounds.sounds import Sounds

def get_engine():
    return Engine(int(Settings.WIDTH * 0.25), int(Settings.WIDTH * 0.75),
                int(Settings.HEIGHT * 0.25), int(Settings.HEIGHT * 0.75),
                sounds)

pygame.init()
scene = pygame.display.set_mode((0, 0),
                                pygame.NOFRAME,
                                pygame.FULLSCREEN)
pygame.display.set_caption("AimTFD")

Settings.WIDTH = pygame.display.Info().current_w
Settings.HEIGHT = pygame.display.Info().current_h

pygame.mouse.set_visible(False)

cursor = Cursor(pygame.image.load("buttons/cursor.png"))
clock = pygame.time.Clock()

# Хромакей
transparency = (0, 0, 0)

# =============================
# Прозрачное окно на весь экран и на передний план
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparency), 0, win32con.LWA_COLORKEY)
user32 = ctypes.WinDLL("user32")
user32.SetWindowPos.restype = wintypes.HWND
user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND,
                                wintypes.INT, wintypes.INT,
                                wintypes.INT, wintypes.INT, wintypes.UINT]
user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001)
# =============================
play_game = True
delta_time = 0               # Синхронизация движения с частотой кадров
frame = 0
# =============================

sounds = Sounds()

# Задать границы области для появления фигур
engine = get_engine()
buttons = Buttons(engine.x1, engine.x2, engine.y1, engine.y2)

riffle = False
pause_riffle = 0
ending = False

# ==========================================================================================
# ==========================================================================================
# ==========================================================================================
while play_game:

    # ==========================================================================================
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play_game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                play_game = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            riffle = True
            pause_riffle = 0
            x, y = pygame.mouse.get_pos()
            btn = buttons.click_mouse(x, y, sounds)
            if btn == 8:
                play_game = False
            elif btn == 7:
                # В первый раз создаст сцену со стастистикой
                if not ending:
                    engine.dec_life(1000)
                    ending = True
                # ...по второму нажатию запустит
                else:
                    ending = False
                    engine = get_engine()
        elif event.type == pygame.MOUSEBUTTONUP:
            cursor.recoil_correct = 1
            riffle = False


    # ==========================================================================================
    scene.fill(transparency)
    engine.draw(scene=scene)
    buttons.draw(scene=scene)
    cursor.draw(scene=scene)
    pygame.display.update()
    # ==========================================================================================

    engine.act(delta_time=delta_time)

    if riffle:
        if pause_riffle == 0:
            x, y = pygame.mouse.get_pos()
            if engine.click_mouse(x + cursor.corrx, y + cursor.corry):
                pause_riffle = 0
            cursor.recoil()
            cursor.increase_recoil()
        if pause_riffle > 0:
            pause_riffle -= 1
        else:
            pause_riffle = 4 + randint(0, 2)
    else:
        cursor.act(delta_time=delta_time)

    if engine.end_training:
        engine = EndStage(engine.x1, engine.x2, engine.y1, engine.y2, engine.data_dict)

    # ==========================================================================================
    delta_time = clock.tick(Settings.FPS) / 1000
    frame += 1
