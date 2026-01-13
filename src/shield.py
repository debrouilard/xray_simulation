import pygame
from src.settings import *

class Shield:
    def __init__(self):
        # Shifted left: starts at ANODE_X and extends leftward
        # Width is adjusted to cover the area between Cathode and Anode
        self.rect = pygame.Rect(ANODE_X - 250, SHIELD_Y, 340, 20) 

    def draw(self, surface, thick):
        self.rect.height = int(thick)
        pygame.draw.rect(surface, COL_SHIELD, self.rect, border_radius=3)
        
        # Shortened text label
        lbl = get_font(12).render("Shield", True, (255, 255, 255))
        # Placed slightly left of center for better visibility
        text_rect = lbl.get_rect(center=(self.rect.centerx - 20, self.rect.y + 12))
        surface.blit(lbl, text_rect)