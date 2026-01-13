import pygame
from src.settings import *

class Anode:
    def __init__(self):
        self.body_rect = pygame.Rect(ANODE_X, CENTER_Y - 50, 80, 100)
        self.target_rect = pygame.Rect(ANODE_X - 8, CENTER_Y - 30, 8, 60)

    def draw(self, surface):
        pygame.draw.rect(surface, (15, 15, 15), self.body_rect)
        pygame.draw.rect(surface, (180, 180, 180), self.target_rect)
        lbl = get_font(12).render("ANODE (+)", True, COL_TEXT)
        surface.blit(lbl, (self.body_rect.x, self.body_rect.y - 20))

class Cathode:
    def __init__(self):
        self.rect = pygame.Rect(CATHODE_X, CENTER_Y - 50, 40, 100)
        self.filament_pos = (CATHODE_X + 35, CENTER_Y)

    def draw(self, surface):
        pygame.draw.rect(surface, (160, 160, 160), self.rect, 2)
        pygame.draw.circle(surface, (255, 120, 0), self.filament_pos, 8)
        lbl = get_font(12).render("CATHODE (-)", True, COL_TEXT)
        surface.blit(lbl, (self.rect.x, self.rect.y - 20))