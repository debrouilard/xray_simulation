import pygame
from src.settings import *

class LeadShield:
    def __init__(self):
        self.rect = pygame.Rect(220, SHIELD_Y, 300, 10)
        self.label_font = pygame.font.SysFont("Arial", 11, bold=True)

    def is_in_shield_range(self, pos, thickness):
        if self.rect.x < pos[0] < self.rect.x + self.rect.width:
            if self.rect.y < pos[1] < self.rect.y + thickness:
                return True
        return False

    def draw(self, screen, thickness):
        # Reduced Shield Label
        screen.blit(self.label_font.render("LEAD SHIELD", True, WHITE), (self.rect.x + 110, self.rect.y - 18))
        
        if thickness > 0:
            s_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, int(thickness))
            pygame.draw.rect(screen, LEAD_GRAY, s_rect)
            pygame.draw.rect(screen, WHITE, s_rect, 1)