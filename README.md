# Tetris

A classic Tetris game built with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green.svg)

## Features

- Classic 10x20 Tetris board with visible grid
- All 7 standard tetrominoes (I, O, T, S, Z, J, L)
- Ghost piece showing where the piece will land
- Next piece preview
- Score, level, and lines tracking
- Increasing difficulty (faster drops at higher levels)
- Pause functionality

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Kasincc/tetris.git
   cd tetris
   ```

2. Install Pygame:
   ```bash
   pip install pygame
   ```

3. Run the game:
   ```bash
   python tetris.py
   ```

## Controls

| Key | Action |
|-----|--------|
| Left Arrow | Move piece left |
| Right Arrow | Move piece right |
| Down Arrow | Soft drop (faster fall) |
| Up Arrow | Rotate clockwise |
| Space | Hard drop (instant drop) |
| P | Pause/Resume |
| R | Restart (after game over) |
| ESC | Quit |

## Scoring

- **Soft drop**: 1 point per cell
- **Hard drop**: 2 points per cell
- **Line clears** (multiplied by level):
  - 1 line: 100 points
  - 2 lines: 300 points
  - 3 lines: 500 points
  - 4 lines (Tetris): 800 points

Level increases every 10 lines cleared, making pieces fall faster.

## License

MIT License
