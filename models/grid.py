import random
from utils.config import GRID_SIZE, TILE_SIZE
from utils.animations import TileAnimation, NewTileAnimation, Particle

class GameGrid:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.tile_animations = []
        self.new_tile_animations = []
        self.particles = []
        
    def reset(self):
        """Reset the game grid and score"""
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.tile_animations = []
        self.new_tile_animations = []
        self.particles = []
        self.add_new_tile()
        self.add_new_tile()
    
    def add_new_tile(self):
        """Add a new tile (2 or 4) to a random empty cell"""
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            value = 2 if random.random() < 0.9 else 4  # 90% chance of 2, 10% of 4
            self.grid[i][j] = value
            self.new_tile_animations.append(NewTileAnimation((i, j), value))
    
    def create_merge_particles(self, row, col, value, tile_colors):
        """Create particles when tiles merge"""
        # Get the tile color based on its value
        color = tile_colors.get(value, (200, 200, 200))
        
        # Position in screen coordinates
        x = col * TILE_SIZE + TILE_SIZE // 2
        y = row * TILE_SIZE + 100 + TILE_SIZE // 2
        
        # Create particles
        for _ in range(20):  # Number of particles
            self.particles.append(Particle(x, y, color, value))
    
    def update_animations(self):
        """Update all animations and remove completed ones"""
        # Update tile movement animations
        i = 0
        while i < len(self.tile_animations):
            if self.tile_animations[i].update():
                self.tile_animations.pop(i)
            else:
                i += 1
        
        # Update new tile animations
        i = 0
        while i < len(self.new_tile_animations):
            if self.new_tile_animations[i].update():
                self.new_tile_animations.pop(i)
            else:
                i += 1
    
    def update_particles(self):
        """Update all particles and remove dead ones"""
        i = 0
        while i < len(self.particles):
            if self.particles[i].update():
                i += 1
            else:
                self.particles.pop(i)
    
    def transpose_grid(self, grid):
        """Transpose the grid (swap rows and columns)"""
        return [list(row) for row in zip(*grid)]
    
    def reverse_rows(self, grid):
        """Reverse each row in the grid"""
        return [row[::-1] for row in grid]
    
    def move_left(self, tile_colors):
        """Move tiles left and merge equal tiles"""
        moved = False
        new_grid = [row[:] for row in self.grid]  # Create a copy
        merged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        for i in range(GRID_SIZE):
            # Collect non-zero tiles
            row = [tile for tile in new_grid[i] if tile != 0]
            
            # Merge adjacent same-value tiles
            j = 0
            while j < len(row) - 1:
                if row[j] == row[j + 1]:
                    row[j] *= 2
                    self.score += row[j]
                    row.pop(j + 1)
                    merged[i][j] = True
                    moved = True
                    # Create particles for the merge
                    self.create_merge_particles(i, j, row[j], tile_colors)
                j += 1
            
            # Fill remaining spots with zeros
            row.extend([0] * (GRID_SIZE - len(row)))
            
            # Check if there was movement
            if new_grid[i] != row:
                moved = True
            
            # Create animations for this row
            for j in range(GRID_SIZE):
                if row[j] != 0:
                    # Find original position
                    found = False
                    for k in range(GRID_SIZE):
                        if new_grid[i][k] == row[j] and not found:
                            if merged[i][j] and k > j:
                                # If this was merged, create two animations: one for each original tile
                                self.tile_animations.append(TileAnimation((i, k), (i, j), row[j], merged=True))
                                
                                # Find the second tile that was merged (first one after k with same value)
                                for l in range(k+1, GRID_SIZE):
                                    if new_grid[i][l] == new_grid[i][k]:
                                        self.tile_animations.append(TileAnimation((i, l), (i, j), row[j], merged=True))
                                        break
                                found = True
                            elif k != j:  # Only animate if position changed
                                self.tile_animations.append(TileAnimation((i, k), (i, j), row[j]))
                                found = True
            
            new_grid[i] = row
        
        if moved:
            self.grid = new_grid
        
        return moved
    
    def move_right(self, tile_colors):
        """Move tiles right by reversing, moving left, then reversing back"""
        # Clear previous animations
        self.tile_animations = []
        
        # Reverse the grid for right movement
        reversed_grid = self.reverse_rows(self.grid)
        self.grid = reversed_grid
        
        # Move left
        moved = self.move_left(tile_colors)
        
        # Reverse back
        self.grid = self.reverse_rows(self.grid)
        
        # Adjust animation data for the reverse transformation
        for anim in self.tile_animations:
            anim.from_pos = (anim.from_pos[0], GRID_SIZE - 1 - anim.from_pos[1])
            anim.to_pos = (anim.to_pos[0], GRID_SIZE - 1 - anim.to_pos[1])
        
        return moved
    
    def move_up(self, tile_colors):
        """Move tiles up by transposing, moving left, then transposing back"""
        # Clear previous animations
        self.tile_animations = []
        
        # Transpose the grid for up movement
        transposed = self.transpose_grid(self.grid)
        self.grid = transposed
        
        # Move left
        moved = self.move_left(tile_colors)
        
        # Transpose back
        self.grid = self.transpose_grid(self.grid)
        
        # Adjust animation data for the transpose transformation
        for anim in self.tile_animations:
            anim.from_pos = (anim.from_pos[1], anim.from_pos[0])
            anim.to_pos = (anim.to_pos[1], anim.to_pos[0])
        
        return moved
    
    def move_down(self, tile_colors):
        """Move tiles down by transposing, moving right, then transposing back"""
        # Clear previous animations
        self.tile_animations = []
        
        # Transpose the grid
        transposed = self.transpose_grid(self.grid)
        self.grid = transposed
        
        # Reverse for right movement
        self.grid = self.reverse_rows(self.grid)
        
        # Move left
        moved = self.move_left(tile_colors)
        
        # Undo the transformations
        self.grid = self.reverse_rows(self.grid)
        self.grid = self.transpose_grid(self.grid)
        
        # Adjust animation data for the transformations
        for anim in self.tile_animations:
            temp = anim.from_pos[0]
            anim.from_pos = (GRID_SIZE - 1 - anim.from_pos[1], temp)
            temp = anim.to_pos[0]
            anim.to_pos = (GRID_SIZE - 1 - anim.to_pos[1], temp)
        
        return moved
    
    def move_tiles(self, direction, tile_colors):
        """Moves tiles in the specified direction and merges equal tiles."""
        # Clear previous animations
        self.tile_animations = []
        
        if direction == "left":
            return self.move_left(tile_colors)
        elif direction == "right":
            return self.move_right(tile_colors)
        elif direction == "up":
            return self.move_up(tile_colors)
        elif direction == "down":
            return self.move_down(tile_colors)
        
        return False
    
    def check_game_over(self):
        """Checks if no moves are left."""
        # Check for empty cells
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == 0:
                    return False
        
        # Check for possible merges horizontally
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        
        # Check for possible merges vertically
        for i in range(GRID_SIZE - 1):
            for j in range(GRID_SIZE):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    return False
        
        return True
    
    def check_win(self):
        """Check if the player has reached 2048."""
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i][j] >= 2048:
                    return True
        return False 