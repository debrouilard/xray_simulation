import pygame

COL_BG = (255, 255, 255)       
COL_UI_BG = (242, 245, 248)    
COL_ACCENT = (0, 102, 204)     
COL_TEXT = (30, 40, 50)        
COL_SHIELD = (120, 125, 130)

WIDTH, HEIGHT = 600, 500 
FPS = 60

# Tightened coordinates for 600x500
CATHODE_X = 50
ANODE_X = 350      
CENTER_Y = 180      
COMPONENT_HEIGHT = 100 
SHIELD_Y = 310  # Positioned to grow downward safely

def get_font(size, bold=True):
    return pygame.font.SysFont("Segoe UI", size, bold=bold)