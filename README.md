# 2048 Game

A Python implementation of the popular 2048 puzzle game using Pygame.

## Description

This 2048 game is a clone of the classic sliding puzzle game where you combine numbered tiles to create a tile with the number 2048. The game features:

- Clean MVC architecture (Model-View-Controller)
- Multiple color themes
- Score tracking with high score saving
- Smooth animations
- Particle effects

## Screenshots

### Classic Theme
<!-- Add screenshot of classic theme here -->
![Classic Theme](screenshots/classic_theme.png)

### Dark Theme
<!-- Add screenshot of dark theme here -->
![Dark Theme](screenshots/dark_theme.png)

### Other Themes
<!-- Add screenshots of additional themes here -->
![Ocean Theme](screenshots/ocean_theme.png)
![Violet Theme](screenshots/violet_theme.png)
![Forest Theme](screenshots/forest_theme.png)

## Installation

### Prerequisites
- Python 3.x
- Pygame

### Setup
1. Clone the repository
2. Install dependencies:
```
pip install pygame
```
3. Run the game:
```
python main.py
```

## How to Play

- Use the arrow keys (Up, Down, Left, Right) to move all tiles in that direction
- When two tiles with the same number touch, they merge into one tile with the sum of their values
- The game ends when there are no more valid moves
- Try to create a tile with the number 2048!

## Controls

- **Arrow Keys**: Move tiles
- **R**: Restart the game (when game over)
- **Esc**: Exit the game
- **1-5**: Switch between themes:
  - 1: Classic
  - 2: Dark
  - 3: Ocean
  - 4: Violet
  - 5: Forest

## Project Structure

```
- main.py            # Main entry point
- controllers/       # Game logic controllers
- models/            # Data models
- views/             # Visual rendering
- utils/             # Configuration and helper functions
```

## License

This project is open source.

## Acknowledgments

Inspired by the original 2048 game created by Gabriele Cirulli. 