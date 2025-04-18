import pygame

# Constants
WIDTH, HEIGHT = 500, 600  # Slightly taller for score display
GRID_SIZE = 4
TILE_SIZE = WIDTH // GRID_SIZE  # Automatically calculate tile size based on window width
GRID_PADDING = 5  # Reduced padding to ensure tiles fill more space
FPS = 60
WINDOW_TITLE = "2048 Game"

# Theme definitions
THEMES = {
    'classic': {
        'name': 'Classic',
        'background_color': (205, 193, 180),
        'gradient_top': (170, 155, 140),
        'gradient_bottom': (205, 193, 180),
        'grid_color': (205, 193, 180),
        'empty_tile': (220, 210, 200),
        'text_color': (119, 110, 101),
        'light_text_color': (249, 246, 242),
    },
    'dark': {
        'name': 'Dark',
        'background_color': (50, 50, 50),
        'gradient_top': (30, 30, 30),
        'gradient_bottom': (60, 60, 60),
        'grid_color': (70, 70, 70),
        'empty_tile': (80, 80, 80),
        'text_color': (230, 230, 230),
        'light_text_color': (255, 255, 255),
    },
    'blue': {
        'name': 'Ocean',
        'background_color': (100, 150, 200),
        'gradient_top': (70, 130, 180),
        'gradient_bottom': (135, 206, 235),
        'grid_color': (100, 150, 200),
        'empty_tile': (160, 200, 240),
        'text_color': (20, 60, 100),
        'light_text_color': (240, 248, 255),
    },
    'purple': {
        'name': 'Violet',
        'background_color': (150, 120, 170),
        'gradient_top': (128, 0, 128),
        'gradient_bottom': (186, 85, 211),
        'grid_color': (150, 120, 170),
        'empty_tile': (180, 160, 200),
        'text_color': (70, 30, 80),
        'light_text_color': (240, 230, 250),
    },
    'green': {
        'name': 'Forest',
        'background_color': (143, 188, 143),
        'gradient_top': (85, 107, 47),
        'gradient_bottom': (143, 188, 143),
        'grid_color': (143, 188, 143),
        'empty_tile': (170, 220, 170),
        'text_color': (47, 79, 47),
        'light_text_color': (240, 255, 240),
    }
}

# Default tile colors (consistent across themes)
DEFAULT_TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

# Overlay color for game over screen
OVERLAY_COLOR = (0, 0, 0, 180)  # Semi-transparent black 