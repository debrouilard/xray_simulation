import pygame
import datetime
import os
from src.settings import *
from src.tubes import XRayTube
from src.shield import LeadShield
from src.particles import ParticleSystem

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("X-Ray Physics: Anode Heel Effect Simulator")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Courier", 13)
label_font = pygame.font.SysFont("Courier", 14, bold=True)

# Initialize Objects
tube = XRayTube()
shield = LeadShield()
particles = ParticleSystem()
intensity_history = [0] * 120 # Data points for the Intensity Graph

class Slider:
    def __init__(self, x, y, w, min_v, max_v, label, unit, initial_val=None):
        self.rect = pygame.Rect(x, y, w, 8)
        self.min, self.max = min_v, max_v
        self.val = initial_val if initial_val is not None else min_v + (max_v - min_v) / 2
        self.label, self.unit = label, unit
        self.grabbed = False

    def draw(self, surf):
        # Draw the slider track
        pygame.draw.rect(surf, (40, 40, 40), self.rect, border_radius=4)
        # Calculate and draw the handle
        pos = self.rect.x + int((self.val - self.min) / (self.max - self.min) * self.rect.w)
        pygame.draw.circle(surf, SUCCESS_GREEN, (pos, self.rect.centery), 8)
        # Draw the label text
        txt = font.render(f"{self.label}: {int(self.val)}{self.unit}", True, WHITE)
        surf.blit(txt, (self.rect.x, self.rect.y - 22))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.grabbed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        if self.grabbed and (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN):
            rel = max(0, min(event.pos[0] - self.rect.x, self.rect.w))
            self.val = self.min + (rel / self.rect.w) * (self.max - self.min)

# Control Configuration
sliders_left = {
    "kvp": Slider(25, 120, 110, 40, 150, "Voltage", "kV"),
    "ma": Slider(25, 200, 110, 1, 500, "Current", "mA")
}
sliders_right = {
    "rate": Slider(565, 240, 110, 1, 20, "Spawn Rate", ""),
    "speed": Slider(565, 310, 110, 2, 15, "Speed", "c"),
    "shield": Slider(565, 380, 110, 0, 120, "Shield", "mm"),
    "angle": Slider(565, 450, 110, 5, 45, "Anode Angle", "°", initial_val=15)
}

save_btn = pygame.Rect(20, 530, 130, 40)

def draw_ui():
    # Render Side Control Panels
    pygame.draw.rect(screen, PANEL_BG, (0, 0, 160, HEIGHT))
    pygame.draw.rect(screen, PANEL_BG, (540, 0, 160, HEIGHT))
    
    # Beam Intensity Graph (Top Right Box)
    g_box = pygame.Rect(545, 60, 140, 80)
    pygame.draw.rect(screen, (10, 10, 10), g_box)
    pygame.draw.rect(screen, (50, 50, 50), g_box, 1) # Box outline
    
    if len(intensity_history) > 1:
        # v * 25 provides high sensitivity for the visual demonstration
        pts = [
            (g_box.x + i * (g_box.w / len(intensity_history)), 
             g_box.bottom - min(v * 25, g_box.h - 5)) 
            for i, v in enumerate(intensity_history)
        ]
        pygame.draw.lines(screen, SUCCESS_GREEN, False, pts, 2)
    
    # Graph Caption
    screen.blit(font.render("BEAM INTENSITY GRAPH", True, WHITE), (545, 145))
    
    # Save Button
    pygame.draw.rect(screen, SUCCESS_GREEN, save_btn, border_radius=8)
    btn_txt = label_font.render("SAVE LOG", True, BLACK)
    screen.blit(btn_txt, (save_btn.centerx - btn_txt.get_width()//2, save_btn.centery - btn_txt.get_height()//2))

# --- Main Runtime Loop ---
running = True
while running:
    # Use a dark off-black to match medical software aesthetics
    screen.fill((15, 15, 15)) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Process slider interactions
        for s in list(sliders_left.values()) + list(sliders_right.values()):
            s.handle_event(event)

    # 1. Logic Update
    current_angle = sliders_right['angle'].val
    # particles.update returns the total hits from the anode/cathode sides
    hits_per_frame = particles.update(
        sliders_left['kvp'].val, 
        sliders_left['ma'].val, 
        sliders_right['rate'].val, 
        sliders_right['speed'].val, 
        sliders_right['shield'].val, 
        shield, 
        current_angle
    )
    
    # Update intensity history for the live graph
    intensity_history.pop(0)
    intensity_history.append(hits_per_frame)

    # 2. Render Simulation Objects
    tube.draw(screen, current_angle)     # Tilted anode target
    shield.draw(screen, sliders_right['shield'].val) # Protective barrier
    particles.draw(screen)               # Dynamic X-ray particles
    
    # 3. Render User Interface
    draw_ui()
    for s in list(sliders_left.values()) + list(sliders_right.values()):
        s.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()