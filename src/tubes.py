import pygame
import math
from src.settings import *

class XRayTube:
    def __init__(self):
        self.label_font = pygame.font.SysFont("Courier", 14, bold=True)

    def draw(self, screen, angle_deg):
        # 1. Component Labels
        screen.blit(self.label_font.render("ANODE", True, WHITE), (320, 210))
        screen.blit(self.label_font.render("CATHODE", True, WHITE), (480, 210))

        # 2. Glass Envelope Outline
        glass_pts = [(180, 270), (180, 330), (400, 330), (430, 380), (530, 380), (530, 220), (430, 220), (400, 270)]
        pygame.draw.polygon(screen, (100, 130, 140), glass_pts, 1)

        # 3. Orange Induction Coils (Stator)
        pygame.draw.rect(screen, (180, 110, 50), (160, 230, 60, 40)) # Top
        pygame.draw.rect(screen, (180, 110, 50), (160, 330, 60, 40)) # Bottom

        # 4. Solid Anode Stem (Updated for length and connection)
        # Made the dark grey base longer (width changed from 70 to 120)
        pygame.draw.rect(screen, (60, 60, 60), (140, 270, 150, 60)) 
        
        # Made the 'stick' (shaft) longer to touch the light grey target
        pygame.draw.rect(screen, (80, 80, 80), (290, 292, 60, 16)) 

        # 5. TILTING ANODE TARGET FACE (Tungsten)
        angle_rad = math.radians(angle_deg)
        center_x, center_y = ANODE_X, 300
        length = 45 
        
        x_off = math.sin(angle_rad) * length
        y_off = math.cos(angle_rad) * length
        
        # Solid Tungsten Target (No lines/outlines)
        poly_pts = [
            (center_x + x_off - 5, center_y - y_off),
            (center_x + x_off + 5, center_y - y_off),
            (center_x - x_off + 8, center_y + y_off),
            (center_x - x_off - 8, center_y + y_off)
        ]
        pygame.draw.polygon(screen, (180, 185, 190), poly_pts) 

        # 6. Cathode Side
        pygame.draw.rect(screen, (70, 70, 70), (510, 265, 40, 70))
        # Filament visualization
        pygame.draw.arc(screen, RED, (495, 290, 20, 20), 1.5, 4.7, 2)