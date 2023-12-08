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

from ctypes import wintypes
from random import randint
from engine.engine import Engine

from settings.settings import Settings

pygame.init()
scene = pygame.display.set_mode((0, 0),
                                pygame.NOFRAME,
                                pygame.FULLSCREEN)
pygame.display.set_caption("AimTFD")

Settings.WIDTH = pygame.display.Info().current_w
Settings.HEIGHT = pygame.display.Info().current_h

pygame.mouse.set_visible(False)

cursor = pygame.image.load("targets/cursor.png")
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

# Задать границы области для появления фигур
engine = Engine(int(Settings.WIDTH * 0.25), int(Settings.WIDTH * 0.75),
                int(Settings.HEIGHT * 0.25), int(Settings.HEIGHT * 0.75))

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
            x, y = pygame.mouse.get_pos()
            engine.click_mouse(x, y)

    # ==========================================================================================
    scene.fill(transparency)
    engine.draw(scene=scene)
    scene.blit(cursor, (pygame.mouse.get_pos()[0] - 16, pygame.mouse.get_pos()[1] - 16))
    pygame.display.update()
    # ==========================================================================================

    engine.act(delta_time=delta_time)

    # ==========================================================================================
    delta_time = clock.tick(Settings.FPS) / 1000
    frame += 1
