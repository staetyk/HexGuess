import pygame
import os

import constants

import round as _round


class Level:
    platform_list = None

    background = None

    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.coin_list = pygame.sprite.Group()
        self.player = player
        self.score = 0
        self.level_num = 0

    def update(self):
        self.platform_list.update()
        self.coin_list.update()

    def draw(self, screen, bg = 0x1000000, options = ()):
        if bg <= 0xffffff:
            screen.fill(bg)
            back = pygame.image.load("images/round_back.png")
            screen.blit(back, (0, 0))
        if len(options) == 4:
            font = pygame.font.SysFont("Arial", 80)
            text = font.render(options[0], False, constants.BLACK)
            screen.blit(text, (90, 110))
            text = font.render(options[1], False, constants.BLACK)
            screen.blit(text, (590, 110))
            text = font.render(options[2], False, constants.BLACK)
            screen.blit(text, (90, 430))
            text = font.render(options[3], False, constants.BLACK)
            screen.blit(text, (590, 430))
        self.platform_list.draw(screen)
        self.coin_list.draw(screen)


class Round(Level):
    def __init__(self, player):
        Level.__init__(self, player)
        _round.main(self)
        self.level_limit = float('-inf')