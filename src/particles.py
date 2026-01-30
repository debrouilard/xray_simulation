import pygame
import random
import math
from src.settings import *

class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.anode_hits = 0
        self.cathode_hits = 0

    def update(self, kvp, ma, rate, speed, shield_thick, shield_obj, anode_angle):
        self.anode_hits = 0
        self.cathode_hits = 0
        
        # Spawn Electrons (Red) based on mA and Rate
        if random.random() < (ma / 500) * (rate / 10):
            self.particles.append({
                'pos': [500, 300 + random.randint(-4, 4)],
                'color': RED,
                'state': 'flying',
                'vel': [-speed, 0]
            })

        for p in self.particles[:]:
            p['pos'][0] += p['vel'][0]
            p['pos'][1] += p['vel'][1]

            # Calculate the tilted impact X-coordinate
            tilt_x_adjustment = (p['pos'][1] - 300) * math.tan(math.radians(anode_angle))
            impact_x = ANODE_X + tilt_x_adjustment

            # Impact Logic (Anode Target)
            if p['state'] == 'flying' and p['pos'][0] <= impact_x:
                p['pos'][0] = impact_x 
                p['color'] = BLUE
                p['state'] = 'falling'
                
                # Anode Heel Effect Physics (Absorption)
                spread = random.uniform(-4, 4)
                intensity_factor = (22 / anode_angle) 
                survival_prob = 0.55 + (spread * 0.2 * intensity_factor)
                
                # If random check fails, particle is absorbed by the "Heel"
                if random.random() > max(0.01, min(0.99, survival_prob)):
                    self.particles.remove(p)
                    continue

                p['vel'] = [spread, 6 + (kvp/70)] 

            # Detection at the bottom for the Intensity Graph
            if p['state'] == 'falling':
                # Shielding Check
                if shield_obj.is_in_shield_range(p['pos'], shield_thick):
                    if random.randint(0, 120) < shield_thick:
                        if p in self.particles: self.particles.remove(p)
                        continue
                
                # Register hits for the graph before particle leaves screen
                if p['pos'][1] > HEIGHT - 30:
                    if p['pos'][0] < ANODE_X: self.anode_hits += 1
                    else: self.cathode_hits += 1

                if p['pos'][1] > HEIGHT:
                    if p in self.particles: self.particles.remove(p)

            # Cleanup out of bounds
            if p['pos'][0] < 0 or p['pos'][0] > WIDTH:
                if p in self.particles: self.particles.remove(p)
        
        # IMPORTANT: Returns total hits to main.py for the graph
        return self.anode_hits + self.cathode_hits

    def draw(self, screen):
        for p in self.particles:
            pygame.draw.circle(screen, p['color'], (int(p['pos'][0]), int(p['pos'][1])), 3)