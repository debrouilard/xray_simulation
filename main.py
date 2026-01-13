import pygame
import sys
import datetime
from collections import deque
from src.settings import *
from src.tubes import Anode, Cathode
from src.particles import ParticleManager
from src.shield import Shield

# --- UI CLASSES ---
class InputBox:
    def __init__(self, x, y, w, h, label):
        self.rect = pygame.Rect(x, y, w, h); self.text = ''; self.label = label
        self.active = False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE: self.text = self.text[:-1]
            elif event.unicode.isdigit(): self.text += event.unicode
    def draw(self, surface):
        color = COL_ACCENT if self.active else (200, 200, 200)
        pygame.draw.rect(surface, color, self.rect, 2)
        txt = get_font(16, False).render(self.text, True, COL_TEXT)
        lbl = get_font(11).render(self.label, True, (80, 90, 100))
        surface.blit(txt, (self.rect.x + 5, self.rect.y + 5))
        surface.blit(lbl, (self.rect.x, self.rect.y - 18))

class Slider:
    def __init__(self, x, y, w, min_v, max_v, init, label):
        self.rect = pygame.Rect(x, y, w, 6); self.min, self.max, self.val = min_v, max_v, init
        self.label = label; self.dragging = False
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.inflate(0, 15).collidepoint(event.pos): self.dragging = True
        if event.type == pygame.MOUSEBUTTONUP: self.dragging = False
        if event.type == pygame.MOUSEMOTION and self.dragging:
            rel = max(0, min(event.pos[0] - self.rect.x, self.rect.width))
            self.val = self.min + (rel / self.rect.width) * (self.max - self.min)
    def draw(self, surface):
        ratio = (self.val - self.min) / (self.max - self.min)
        pygame.draw.rect(surface, (220, 225, 230), self.rect)
        pygame.draw.circle(surface, COL_ACCENT, (int(self.rect.x + self.rect.width * ratio), self.rect.centery), 8)
        lbl = get_font(10).render(f"{self.label}: {int(self.val)}", True, COL_TEXT)
        surface.blit(lbl, (self.rect.x, self.rect.y - 15))

class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h); self.text = text; self.color = color
        self.is_hovered = False
    def draw(self, surface):
        draw_color = (0, 150, 0) if self.is_hovered else self.color
        pygame.draw.rect(surface, draw_color, self.rect, border_radius=4)
        txt = get_font(11).render(self.text, True, (255, 255, 255))
        surface.blit(txt, (self.rect.centerx - txt.get_width()//2, self.rect.centery - txt.get_height()//2))
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION: self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered: return True
        return False

def save_session_data(kv, ma, data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("xray_data.txt", "a") as f:
        f.write(f"\n--- Session: {timestamp} ---\n")
        f.write(f"Settings: {kv} kV, {ma} mA\n")
        f.write(f"Intensity Peaks: {list(data)}\n")
        f.write("-" * 30 + "\n")
    print(f"Data saved at {timestamp}")

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("X-Ray Physics Console")
    clock = pygame.time.Clock()

    input_state = 'KV'
    box_kv = InputBox(WIDTH//2 - 90, 150, 180, 35, "1. Voltage (kV)")
    box_ma = InputBox(WIDTH//2 - 90, 210, 180, 35, "2. Current (mA)")
    box_kv.active = True 
    
    anode, cathode = Anode(), Cathode()
    pm, shield = ParticleManager(), Shield()
    
    s_spawn = Slider(30, 460, 150, 1, 100, 30, "Spawn Rate")
    s_speed = Slider(220, 460, 150, 1, 100, 40, "Electron Speed")
    s_thick = Slider(410, 460, 150, 5, 120, 30, "Shield Thickness")
    
    # Smaller, shifted Save Button to avoid Anode overlap
    btn_save = Button(WIDTH - 170, 105, 140, 22, "SAVE", (34, 139, 34))
    
    graph_pts = deque([0]*150, maxlen=150)

    while True:
        screen.fill(COL_BG)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if input_state != 'SIM':
                if input_state == 'KV':
                    box_kv.handle_event(event)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        input_state = 'MA'; box_kv.active = False; box_ma.active = True
                elif input_state == 'MA':
                    box_ma.handle_event(event)
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        input_state = 'SIM'
            else:
                s_spawn.handle_event(event); s_speed.handle_event(event); s_thick.handle_event(event)
                if btn_save.handle_event(event):
                    save_session_data(box_kv.text, box_ma.text, graph_pts)

        if input_state != 'SIM':
            box_kv.draw(screen); box_ma.draw(screen)
        else:
            pm.spawn_electron(s_spawn.val)
            pm.update(s_speed.val, anode.target_rect, shield.rect, s_thick.val)
            graph_pts.append(pm.intensity_data)

            shield.draw(screen, s_thick.val)
            anode.draw(screen); cathode.draw(screen); pm.draw(screen)
            s_spawn.draw(screen); s_speed.draw(screen); s_thick.draw(screen)

            # Intensity Monitor
            g_rect = pygame.Rect(WIDTH - 180, 20, 160, 80)
            pygame.draw.rect(screen, (255, 255, 255), g_rect)
            pygame.draw.rect(screen, (210, 215, 220), g_rect, 1)
            pts = [(g_rect.x + i, g_rect.bottom - min(g_rect.height, v*25)) for i, v in enumerate(graph_pts)]
            if len(pts) > 1: pygame.draw.lines(screen, (220, 30, 30), False, pts, 1)
            
            btn_save.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()