import pygame
from utils.config import THEMES, DEFAULT_TILE_COLORS, WIDTH, HEIGHT

class ThemeManager:
    def __init__(self, default_theme='classic'):
        self.current_theme = default_theme
        self.background_color = THEMES[self.current_theme]['background_color']
        self.gradient_top = THEMES[self.current_theme]['gradient_top']
        self.gradient_bottom = THEMES[self.current_theme]['gradient_bottom']
        self.grid_color = THEMES[self.current_theme]['grid_color']
        self.text_color = THEMES[self.current_theme]['text_color']
        self.light_text_color = THEMES[self.current_theme]['light_text_color']
        
        # Initialize tile colors with the default ones
        self.tile_colors = DEFAULT_TILE_COLORS.copy()
        self.tile_colors[0] = THEMES[self.current_theme]['empty_tile']
        
        # Initialize the gradient background
        self.gradient_background = None
        self.create_gradient_background(WIDTH, HEIGHT)
    
    def set_theme(self, theme_name):
        """Change the current theme"""
        if theme_name in THEMES:
            self.current_theme = theme_name
            self.update_theme_colors()
            return True
        return False
    
    def update_theme_colors(self):
        """Update colors based on current theme"""
        self.background_color = THEMES[self.current_theme]['background_color']
        self.gradient_top = THEMES[self.current_theme]['gradient_top']
        self.gradient_bottom = THEMES[self.current_theme]['gradient_bottom']
        self.grid_color = THEMES[self.current_theme]['grid_color']
        self.text_color = THEMES[self.current_theme]['text_color']
        self.light_text_color = THEMES[self.current_theme]['light_text_color']
        
        # Update empty tile color
        self.tile_colors[0] = THEMES[self.current_theme]['empty_tile']
        
        # Update background
        self.create_gradient_background(WIDTH, HEIGHT)
    
    def create_gradient_background(self, width=500, height=600):
        """Create a gradient background for the current theme"""
        self.gradient_background = pygame.Surface((width, height))
        for y in range(height):
            # Calculate the interpolation factor (0 at top, 1 at bottom)
            t = y / height
            # Interpolate between the top and bottom colors
            r = int(self.gradient_top[0] * (1 - t) + self.gradient_bottom[0] * t)
            g = int(self.gradient_top[1] * (1 - t) + self.gradient_bottom[1] * t)
            b = int(self.gradient_top[2] * (1 - t) + self.gradient_bottom[2] * t)
            # Draw a horizontal line with the interpolated color
            pygame.draw.line(self.gradient_background, (r, g, b), (0, y), (width, y))
        
        return self.gradient_background 