# Chiikawa Tetris 🎮✨

A classic Tetris game with a cute Chiikawa theme! Built with Python and Pygame, featuring soft pastel colors and adorable character sprites.

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green.svg)

## ✨ Features

- Classic 10x20 Tetris board with visible grid
- All 7 standard tetrominoes (I, O, T, S, Z, J, L)
- **Chiikawa-themed pastel color scheme** 🌸
- **Cute character images on each block** 🐱🐰
- Ghost piece showing where the piece will land
- Next piece preview with character sprites
- Score, level, and lines tracking
- Increasing difficulty (faster drops at higher levels)
- Pause functionality

## 🎨 Chiikawa Theme

Each Tetris piece features a different character:
- **I piece** (Light Blue): Chiikawa
- **O piece** (Soft Yellow): Hachiware
- **T piece** (Soft Purple): Usagi
- **S piece** (Mint Green): Momonga
- **Z piece** (Light Pink): Kurimanju
- **J piece** (Light Steel Blue): Armor-san
- **L piece** (Peach): Ramen Master

The game uses soft, pastel colors inspired by the Chiikawa aesthetic for a gentle, cute gaming experience!

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/janeyip-gif/chiikawa_tetris.git
   cd chiikawa_tetris
   ```

2. Install Pygame:
   ```bash
   pip3 install pygame
   ```

3. Run the game:
   ```bash
   python3 tetris.py
   ```

### 🖼️ Customizing Character Images

The game comes with placeholder character images. To use your own Chiikawa character images:

1. Replace the PNG files in the `images/` directory with your own 24x24 pixel images
2. Make sure they have transparent backgrounds for the best effect
3. Keep the same filenames: `chiikawa.png`, `hachiware.png`, `usagi.png`, `momonga.png`, `kurimanju.png`, `armor.png`, `ramen.png`

## 🎮 Controls

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

## 🏆 Scoring

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
