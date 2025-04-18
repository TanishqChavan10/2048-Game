import pygame
import math
from utils.config import WIDTH, HEIGHT, GRID_SIZE, TILE_SIZE, GRID_PADDING, OVERLAY_COLOR

class GameRenderer:
    def __init__(self, screen, theme_manager):
        self.screen = screen
        self.theme_manager = theme_manager
        
        # Initialize font objects directly
        self.font = pygame.font.SysFont("Arial", 40, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.title_font = pygame.font.SysFont("Arial", 50, bold=True)
    
    def draw_tile(self, x, y, size, color, value=None, alpha=255, scale=1.0):
        """Draw a tile with shadow and text."""
        # Draw shadow
        shadow_offset = 3
        shadow_color = (0, 0, 0, 100)  # Semi-transparent black
        shadow = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(shadow, shadow_color, (0, 0, size, size), border_radius=5)
        self.screen.blit(shadow, (x + shadow_offset, y + shadow_offset))
        
        # Draw tile
        tile = pygame.Surface((size, size), pygame.SRCALPHA)
        color_with_alpha = (*color, alpha)
        pygame.draw.rect(tile, color_with_alpha, (0, 0, size, size), border_radius=5)
        self.screen.blit(tile, (x, y))
        
        # Draw text if value is provided
        if value and value != 0:
            text_color = self.theme_manager.light_text_color if value > 4 else self.theme_manager.text_color
            text = self.font.render(str(value), True, text_color)
            text_size = text.get_size()
            self.screen.blit(text, (x + (size - text_size[0]) / 2, y + (size - text_size[1]) / 2))
    
    def draw_grid(self, game_grid, score_manager):
        """Draws the grid, tiles, score, and animations."""
        # Draw the gradient background
        self.screen.blit(self.theme_manager.gradient_background, (0, 0))
        
        # Draw title and score area
        title_text = self.title_font.render("2048", True, self.theme_manager.text_color)
        self.screen.blit(title_text, (20, 20))
        
        # Draw theme name
        theme_text = self.small_font.render(f"Theme: {self.theme_manager.current_theme}", True, self.theme_manager.text_color)
        self.screen.blit(theme_text, (20, 60))
        
        # Draw score boxes with subtle shadows
        # Increase box width and adjust position
        box_width = 90  # Increased from 75
        box_height = 65  # Increased from 60
        score_box_x = WIDTH - 190  # Adjusted for wider boxes
        best_box_x = WIDTH - 95
        
        # Shadow for first box
        pygame.draw.rect(self.screen, (0, 0, 0, 100), (score_box_x + 3, 23, box_width, box_height), border_radius=6)
        # Shadow for second box
        pygame.draw.rect(self.screen, (0, 0, 0, 100), (best_box_x + 3, 23, box_width, box_height), border_radius=6)
        
        # Actual score boxes
        pygame.draw.rect(self.screen, self.theme_manager.grid_color, (score_box_x, 20, box_width, box_height), border_radius=6)
        pygame.draw.rect(self.screen, self.theme_manager.grid_color, (best_box_x, 20, box_width, box_height), border_radius=6)
        
        score_label = self.small_font.render("SCORE", True, self.theme_manager.text_color)
        best_label = self.small_font.render("BEST", True, self.theme_manager.text_color)
        
        score_value = self.small_font.render(str(score_manager.current_score), True, self.theme_manager.text_color)
        best_value = self.small_font.render(str(score_manager.best_score), True, self.theme_manager.text_color)
        
        # Center text in the boxes
        self.screen.blit(score_label, (score_box_x + (box_width - score_label.get_width()) // 2, 25))
        self.screen.blit(best_label, (best_box_x + (box_width - best_label.get_width()) // 2, 25))
        self.screen.blit(score_value, (score_box_x + (box_width - score_value.get_width()) // 2, 50))
        self.screen.blit(best_value, (best_box_x + (box_width - best_value.get_width()) // 2, 50))
        
        # Draw grid background with shadow
        shadow_offset = 5
        pygame.draw.rect(
            self.screen,
            (0, 0, 0, 100),
            (shadow_offset, 100 + shadow_offset, WIDTH, HEIGHT - 100),
            border_radius=10
        )
        pygame.draw.rect(
            self.screen,
            self.theme_manager.grid_color,
            (0, 100, WIDTH, HEIGHT - 100),
            border_radius=10
        )
        
        # Draw empty tile slots
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                self.draw_tile(
                    j * TILE_SIZE + GRID_PADDING,
                    i * TILE_SIZE + 100,
                    TILE_SIZE - 2*GRID_PADDING,
                    self.theme_manager.tile_colors[0]
                )
        
        # Draw animated tiles (moving)
        for anim in game_grid.tile_animations:
            x, y = anim.get_current_position()
            tile_size = (TILE_SIZE - 2*GRID_PADDING) * (anim.scale if anim.merged else 1.0)
            self.draw_tile(
                x, y,
                tile_size,
                self.theme_manager.tile_colors[anim.value],
                anim.value
            )
        
        # Draw static tiles (only those not currently animating)
        animating_positions = [(anim.to_pos[0], anim.to_pos[1]) for anim in game_grid.tile_animations]
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if (i, j) not in animating_positions and game_grid.grid[i][j] != 0:
                    # Check if this tile is in new tile animations
                    in_new_anim = False
                    for anim in game_grid.new_tile_animations:
                        if anim.pos == (i, j):
                            in_new_anim = True
                            scale = anim.get_scale()
                            tile_size = (TILE_SIZE - 2*GRID_PADDING) * scale
                            offset = (TILE_SIZE - 2*GRID_PADDING - tile_size) / 2
                            
                            self.draw_tile(
                                j * TILE_SIZE + GRID_PADDING + offset,
                                i * TILE_SIZE + 100 + offset,
                                tile_size,
                                self.theme_manager.tile_colors[game_grid.grid[i][j]],
                                game_grid.grid[i][j] if scale > 0.5 else None,  # Only draw text when tile is big enough
                                int(255 * min(1.0, scale * 1.5))  # Fade in
                            )
                            break
                    
                    if not in_new_anim:
                        self.draw_tile(
                            j * TILE_SIZE + GRID_PADDING,
                            i * TILE_SIZE + 100,
                            TILE_SIZE - 2*GRID_PADDING,
                            self.theme_manager.tile_colors[game_grid.grid[i][j]],
                            game_grid.grid[i][j]
                        )
        
        # Draw particles
        self.draw_particles(game_grid.particles)
    
    def draw_particles(self, particles):
        """Draw all particles"""
        particle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for particle in particles:
            particle.draw(particle_surface)
        self.screen.blit(particle_surface, (0, 0))
    
    def draw_game_over(self, score_manager):
        """Draw game over overlay and return button rectangles"""
        # Create a semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY_COLOR)
        
        # Apply a pulsating alpha for a cool effect
        current_time = pygame.time.get_ticks()
        pulse = (math.sin(current_time * 0.003) * 0.1) + 0.9  # Pulsate between 0.8 and 1.0
        
        # Apply the alpha
        overlay.set_alpha(int(200 * pulse))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text with subtle glow effect
        glow_size = int(2 + math.sin(current_time * 0.005) * 2)
        
        # Glow effect
        for offset in range(glow_size, 0, -1):
            glow_color = (255, 215, 0, int(150/offset))  # Golden glow
            glow_text = self.title_font.render("Game Over!", True, glow_color)
            self.screen.blit(glow_text, (WIDTH//2 - glow_text.get_width()//2 - offset, HEIGHT//2 - 120 - offset))
            self.screen.blit(glow_text, (WIDTH//2 - glow_text.get_width()//2 + offset, HEIGHT//2 - 120 - offset))
            self.screen.blit(glow_text, (WIDTH//2 - glow_text.get_width()//2 - offset, HEIGHT//2 - 120 + offset))
            self.screen.blit(glow_text, (WIDTH//2 - glow_text.get_width()//2 + offset, HEIGHT//2 - 120 + offset))
        
        # Main text
        game_over_text = self.title_font.render("Game Over!", True, (255, 255, 255))
        self.screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 120))
        
        # Display current score
        score_text = self.font.render(f"Your Score: {score_manager.current_score}", True, (255, 255, 255))
        self.screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 60))
        
        # Display highest score with a nice decoration
        if score_manager.current_score >= score_manager.best_score and score_manager.current_score > 0:
            high_score_text = self.font.render(f"NEW HIGH SCORE!", True, (255, 215, 0))  # Gold color
            self.screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 - 20))
        else:
            high_score_text = self.font.render(f"Best Score: {score_manager.best_score}", True, (255, 255, 255))
            self.screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 - 20))
        
        # Display theme info
        theme_text = self.small_font.render(f"Press 1-5 to change theme (current: {self.theme_manager.current_theme})", True, (200, 200, 200))
        self.screen.blit(theme_text, (WIDTH//2 - theme_text.get_width()//2, HEIGHT//2 + 150))
        
        # Get mouse position for hover effects
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw restart button with hover effect
        restart_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 30, 200, 50)
        button_color = (80, 175, 76)  # Green color
        hover_color = (100, 195, 96)  # Lighter green
        
        # Check if mouse is hovering over restart button
        if restart_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, hover_color, restart_button, border_radius=8)
            # Add a subtle shadow effect
            pygame.draw.rect(self.screen, (255, 255, 255, 30), restart_button.inflate(-8, -8), 2, border_radius=6)
        else:
            pygame.draw.rect(self.screen, button_color, restart_button, border_radius=8)
        
        restart_text = self.small_font.render("Play Again", True, (255, 255, 255))
        self.screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 30 + (50 - restart_text.get_height())//2))
        
        # Draw exit button with hover effect
        exit_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 90, 200, 50)
        exit_button_color = (175, 76, 76)  # Red color
        exit_hover_color = (195, 96, 96)  # Lighter red
        
        # Check if mouse is hovering over exit button
        if exit_button.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, exit_hover_color, exit_button, border_radius=8)
            # Add a subtle shadow effect
            pygame.draw.rect(self.screen, (255, 255, 255, 30), exit_button.inflate(-8, -8), 2, border_radius=6)
        else:
            pygame.draw.rect(self.screen, exit_button_color, exit_button, border_radius=8)
        
        exit_text = self.small_font.render("Exit Game", True, (255, 255, 255))
        self.screen.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, HEIGHT//2 + 90 + (50 - exit_text.get_height())//2))
        
        return restart_button, exit_button 