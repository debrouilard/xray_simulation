import pygame
import random
from src.settings import *

class ParticleManager:
    def __init__(self):
        self.electrons = []
        self.intensity_data = 0 

    def spawn_electron(self, rate):
        if random.randint(0, 100) < rate:
            self.electrons.append({
                'x': CATHODE_X + 55, 
                'y': CENTER_Y + random.randint(-5, 5),
                'state': 'red',
                'vx': 0, 'vy': 0
            })

    def update(self, speed, anode_target_rect, shield_rect, thick_val):
        self.intensity_data = 0 
        move_speed = speed * 0.18
        
        for p in self.electrons[:]:
            if p['state'] == 'red':
                p['x'] += move_speed
                # STRICT COLLISION: Stop at the target face
                if p['x'] >= anode_target_rect.left:
                    p['x'] = anode_target_rect.left 
                    p['state'] = 'purple'
                    p['vx'] = random.uniform(-1, -3) 
                    p['vy'] = random.uniform(2, 6)
                    self.intensity_data += 1
            else:
                p['x'] += p['vx']
                p['y'] += p['vy']
                
                if shield_rect.collidepoint(p['x'], p['y']):
                    if random.randint(0, 120) < thick_val:
                        self.electrons.remove(p)
                
                elif p['y'] > 700 or p['x'] < 0:
                    if p in self.electrons: self.electrons.remove(p)

    def draw(self, surface):
        for p in self.electrons:
            color = (255, 60, 60) if p['state'] == 'red' else (130, 50, 250)
            pygame.draw.circle(surface, color, (int(p['x']), int(p['y'])), 3)