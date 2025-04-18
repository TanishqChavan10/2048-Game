import pygame
import sys
from utils.config import FPS, THEMES
from models.grid import GameGrid
from models.score import ScoreManager
from utils.theme_manager import ThemeManager
from views.renderer import GameRenderer

class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.game_grid = GameGrid()
        self.score_manager = ScoreManager()
        self.theme_manager = ThemeManager(default_theme='classic')
        self.renderer = GameRenderer(screen, self.theme_manager)
        self.running = True
        self.game_over = False
        self.moved = False
        self.restart_button_rect = None
        self.exit_button_rect = None
    
    def reset_game(self):
        """Reset the game state"""
        self.game_grid.reset()
        self.score_manager.reset_score()
        self.theme_manager.update_theme_colors()
        self.game_over = False
        self.moved = False
    
    def handle_events(self):
        """Handle user input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle key presses during active gameplay
            if event.type == pygame.KEYDOWN and not self.game_over and len(self.game_grid.tile_animations) == 0:
                self.moved = False
                
                # Theme selection keys
                if event.key == pygame.K_1:
                    self.theme_manager.set_theme('classic')
                elif event.key == pygame.K_2:
                    self.theme_manager.set_theme('dark')
                elif event.key == pygame.K_3:
                    self.theme_manager.set_theme('blue')
                elif event.key == pygame.K_4:
                    self.theme_manager.set_theme('purple')
                elif event.key == pygame.K_5:
                    self.theme_manager.set_theme('green')
                # Movement keys
                elif event.key == pygame.K_LEFT:
                    self.moved = self.game_grid.move_tiles("left", self.theme_manager.tile_colors)
                elif event.key == pygame.K_RIGHT:
                    self.moved = self.game_grid.move_tiles("right", self.theme_manager.tile_colors)
                elif event.key == pygame.K_UP:
                    self.moved = self.game_grid.move_tiles("up", self.theme_manager.tile_colors)
                elif event.key == pygame.K_DOWN:
                    self.moved = self.game_grid.move_tiles("down", self.theme_manager.tile_colors)
                elif event.key == pygame.K_ESCAPE:  # Exit on Escape key
                    self.running = False
                
                if self.moved:
                    # Update score
                    self.score_manager.update_score(self.game_grid.score)
                    
                    # Check for game over
                    if self.game_grid.check_game_over():
                        self.game_over = True
                elif not self.game_grid.check_game_over():
                    # If no move was made and game isn't over yet, check if any move is possible
                    self.check_for_possible_moves()
            
            # Theme selection should work even during game over
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.theme_manager.set_theme('classic')
                elif event.key == pygame.K_2:
                    self.theme_manager.set_theme('dark')
                elif event.key == pygame.K_3:
                    self.theme_manager.set_theme('blue')
                elif event.key == pygame.K_4:
                    self.theme_manager.set_theme('purple')
                elif event.key == pygame.K_5:
                    self.theme_manager.set_theme('green')
                
                # Restart on R key during game over
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
            
            # Handle mouse clicks for buttons during game over
            if event.type == pygame.MOUSEBUTTONDOWN and self.game_over:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if restart button was clicked
                if self.restart_button_rect and self.restart_button_rect.collidepoint(mouse_pos):
                    self.reset_game()
                
                # Check if exit button was clicked
                if self.exit_button_rect and self.exit_button_rect.collidepoint(mouse_pos):
                    self.running = False
    
    def check_for_possible_moves(self):
        """Check if any move is possible"""
        # Save current state
        original_grid = [row[:] for row in self.game_grid.grid]
        original_score = self.game_grid.score
        
        # Try each direction
        for direction in ["left", "right", "up", "down"]:
            if self.game_grid.move_tiles(direction, self.theme_manager.tile_colors):
                # If a move is possible, restore original state and return
                self.game_grid.grid = original_grid
                self.game_grid.score = original_score
                self.game_grid.tile_animations = []
                return
        
        # If no move is possible, game is over
        self.game_over = True
    
    def update(self):
        """Update game state"""
        # Update animations
        self.game_grid.update_animations()
        self.game_grid.update_particles()
        
        # Add new tile if animations finished and one is needed
        if len(self.game_grid.tile_animations) == 0 and self.moved and not self.game_grid.new_tile_animations:
            self.game_grid.add_new_tile()
            self.moved = False
            
            # Check for game over again after adding new tile
            if self.game_grid.check_game_over():
                self.game_over = True
    
    def render(self):
        """Render game state"""
        # Draw grid and game elements
        self.renderer.draw_grid(self.game_grid, self.score_manager)
        
        # Draw game over screen if game is over
        if self.game_over:
            self.restart_button_rect, self.exit_button_rect = self.renderer.draw_game_over(self.score_manager)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        self.reset_game()
        
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        # Save the high score before exiting
        self.score_manager.save_high_score(self.score_manager.best_score)
        
        pygame.quit()
        sys.exit() 