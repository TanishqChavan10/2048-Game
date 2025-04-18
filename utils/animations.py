import random
import pygame
import math
from utils.config import TILE_SIZE, GRID_PADDING

class TileAnimation:
    def __init__(self, from_pos, to_pos, value, merged=False):
        self.from_pos = from_pos  # (row, col)
        self.to_pos = to_pos  # (row, col)
        self.value = value
        self.progress = 0.0
        self.merged = merged
        self.scale = 1.0

    def update(self):
        if self.progress < 1.0:
            self.progress += 0.1
            if self.merged and self.progress > 0.8:
                self.scale = 1.1 - (self.progress - 0.8) * 0.5
            return False  # Animation not complete
        return True  # Animation complete

    def get_current_position(self):
        start_x = self.from_pos[1] * TILE_SIZE + GRID_PADDING
        start_y = self.from_pos[0] * TILE_SIZE + 100
        end_x = self.to_pos[1] * TILE_SIZE + GRID_PADDING
        end_y = self.to_pos[0] * TILE_SIZE + 100
        
        # Smooth easing function
        t = self.progress
        t = 1.0 - (1.0 - t) * (1.0 - t)  # easeOutQuad
        
        current_x = start_x + (end_x - start_x) * t
        current_y = start_y + (end_y - start_y) * t
        
        return (current_x, current_y)

class NewTileAnimation:
    def __init__(self, pos, value):
        self.pos = pos  # (row, col)
        self.value = value
        self.progress = 0.0

    def update(self):
        if self.progress < 1.0:
            self.progress += 0.15
            return False
        return True

    def get_scale(self):
        # Start small and grow to full size
        return min(1.0, self.progress * 1.2)

class Particle:
    def __init__(self, x, y, color, value):
        self.x = x
        self.y = y
        self.color = color
        self.value = value
        self.size = random.randint(4, 8)
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)
        self.life = 1.0  # Life from 1 to 0
        self.fade_speed = random.uniform(0.02, 0.05)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravity
        self.size -= 0.1
        self.life -= self.fade_speed
        return self.life > 0 and self.size > 0
        
    def draw(self, surface):
        # Apply fade to color
        alpha = int(255 * self.life)
        color = (self.color[0], self.color[1], self.color[2], alpha)
        
        # Draw particle
        if self.size > 0:
            pygame.draw.circle(
                surface,
                color,
                (int(self.x), int(self.y)),
                int(self.size)
            ) 