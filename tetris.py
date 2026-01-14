#!/usr/bin/env python3
"""
Tetris Game in Python with Pygame

How to run:
-----------
1. Install Pygame: pip install pygame
2. Run the game:   python tetris.py

Controls:
---------
- Left Arrow:  Move piece left
- Right Arrow: Move piece right
- Down Arrow:  Soft drop (faster fall)
- Up Arrow:    Rotate clockwise
- Space:       Hard drop (instant drop)
- P:           Pause/Resume
- R:           Restart (after game over)
- ESC:         Quit
"""

import pygame
import random
from typing import List, Tuple, Optional

# =============================================================================
# CONSTANTS
# =============================================================================

# Board dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
CELL_SIZE = 30

# Window dimensions
SIDEBAR_WIDTH = 150
WINDOW_WIDTH = BOARD_WIDTH * CELL_SIZE + SIDEBAR_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT * CELL_SIZE

# Colors (RGB) - Chiikawa soft aesthetic
BLACK = (245, 245, 245)        # Off-white (soft background)
WHITE = (80, 80, 80)           # Dark gray (for text visibility)
GRAY = (200, 200, 200)         # Light gray
DARK_GRAY = (230, 230, 235)    # Very light gray

# Tetromino colors (Chiikawa-themed soft pastels)
COLORS = {
    'I': (173, 216, 230),  # Light blue (Chiikawa's soft blue)
    'O': (255, 250, 205),  # Lemon chiffon (soft yellow)
    'T': (221, 160, 221),  # Plum (soft purple/pink)
    'S': (189, 252, 201),  # Mint green (soft green)
    'Z': (255, 182, 193),  # Light pink (soft red/pink)
    'J': (176, 196, 222),  # Light steel blue (soft blue)
    'L': (255, 218, 185),  # Peach puff (soft orange)
}

# Game timing (milliseconds)
FALL_SPEED = 500          # Normal fall speed
SOFT_DROP_SPEED = 50      # Speed when holding down
LOCK_DELAY = 500          # Delay before piece locks

# =============================================================================
# PIECE DEFINITIONS
# =============================================================================

# Each piece is defined as a list of rotation states
# Each rotation state is a list of (row, col) offsets from the piece origin
TETROMINOES = {
    'I': [
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 1), (1, 1), (2, 1), (3, 1)],
    ],
    'O': [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ],
    'T': [
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (2, 1)],
    ],
    'S': [
        [(0, 1), (0, 2), (1, 0), (1, 1)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 1), (1, 2), (2, 0), (2, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1)],
    ],
    'Z': [
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 2), (1, 1), (1, 2), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(0, 1), (1, 0), (1, 1), (2, 0)],
    ],
    'J': [
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (0, 2), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 0), (2, 1)],
    ],
    'L': [
        [(0, 2), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
    ],
}


# =============================================================================
# PIECE CLASS
# =============================================================================

class Piece:
    """Represents a falling Tetris piece."""

    def __init__(self, piece_type: str, image: Optional[pygame.Surface] = None):
        self.type = piece_type
        self.rotations = TETROMINOES[piece_type]
        self.rotation_index = 0
        self.color = COLORS[piece_type]
        self.image = image

        # Starting position (top center of board)
        self.row = 0
        self.col = BOARD_WIDTH // 2 - 2

    def get_cells(self) -> List[Tuple[int, int]]:
        """Get the absolute board positions of all cells in this piece."""
        cells = []
        for dr, dc in self.rotations[self.rotation_index]:
            cells.append((self.row + dr, self.col + dc))
        return cells

    def get_cells_at(self, row: int, col: int, rotation: int) -> List[Tuple[int, int]]:
        """Get cells at a hypothetical position and rotation."""
        cells = []
        for dr, dc in self.rotations[rotation]:
            cells.append((row + dr, col + dc))
        return cells

    def rotate_cw(self) -> int:
        """Return the next clockwise rotation index."""
        return (self.rotation_index + 1) % 4

    def rotate_ccw(self) -> int:
        """Return the next counter-clockwise rotation index."""
        return (self.rotation_index - 1) % 4


# =============================================================================
# BOARD CLASS
# =============================================================================

class Board:
    """Represents the Tetris game board."""

    def __init__(self):
        # Grid stores piece type strings or None for empty cells
        # grid[row][col], row 0 is top
        self.grid: List[List[Optional[str]]] = [
            [None for _ in range(BOARD_WIDTH)]
            for _ in range(BOARD_HEIGHT)
        ]

    def is_valid_position(self, cells: List[Tuple[int, int]]) -> bool:
        """Check if all cells are within bounds and not occupied."""
        for row, col in cells:
            # Check horizontal bounds
            if col < 0 or col >= BOARD_WIDTH:
                return False
            # Check vertical bounds (allow above top for spawning)
            if row >= BOARD_HEIGHT:
                return False
            # Check if cell is occupied (only for visible rows)
            if row >= 0 and self.grid[row][col] is not None:
                return False
        return True

    def lock_piece(self, piece: Piece) -> None:
        """Lock a piece onto the board."""
        for row, col in piece.get_cells():
            if 0 <= row < BOARD_HEIGHT and 0 <= col < BOARD_WIDTH:
                self.grid[row][col] = piece.type

    def clear_lines(self) -> int:
        """Clear completed lines and return the number of lines cleared."""
        lines_cleared = 0
        row = BOARD_HEIGHT - 1

        while row >= 0:
            # Check if row is complete
            if all(cell is not None for cell in self.grid[row]):
                lines_cleared += 1
                # Remove the row
                del self.grid[row]
                # Add empty row at top
                self.grid.insert(0, [None for _ in range(BOARD_WIDTH)])
                # Don't decrement row - check same position again
            else:
                row -= 1

        return lines_cleared

    def draw(self, surface: pygame.Surface, piece_images: dict = None) -> None:
        """Draw the board grid and locked pieces."""
        # Draw background
        board_rect = pygame.Rect(0, 0, BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE)
        pygame.draw.rect(surface, BLACK, board_rect)

        # Draw grid lines
        for row in range(BOARD_HEIGHT + 1):
            y = row * CELL_SIZE
            pygame.draw.line(surface, DARK_GRAY, (0, y), (BOARD_WIDTH * CELL_SIZE, y))
        for col in range(BOARD_WIDTH + 1):
            x = col * CELL_SIZE
            pygame.draw.line(surface, DARK_GRAY, (x, 0), (x, BOARD_HEIGHT * CELL_SIZE))

        # Draw locked pieces
        for row in range(BOARD_HEIGHT):
            for col in range(BOARD_WIDTH):
                piece_type = self.grid[row][col]
                if piece_type is not None:
                    color = COLORS[piece_type]
                    image = piece_images.get(piece_type) if piece_images else None
                    self._draw_cell(surface, row, col, color, image)

    def _draw_cell(self, surface: pygame.Surface, row: int, col: int,
                   color: Tuple[int, int, int], image: Optional[pygame.Surface] = None) -> None:
        """Draw a single cell with a 3D effect and optional character image."""
        x = col * CELL_SIZE
        y = row * CELL_SIZE

        # Main cell
        rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
        pygame.draw.rect(surface, color, rect)

        # Highlight (top-left)
        highlight = tuple(min(c + 50, 255) for c in color)
        pygame.draw.line(surface, highlight, (x + 1, y + 1), (x + CELL_SIZE - 2, y + 1))
        pygame.draw.line(surface, highlight, (x + 1, y + 1), (x + 1, y + CELL_SIZE - 2))

        # Shadow (bottom-right)
        shadow = tuple(max(c - 50, 0) for c in color)
        pygame.draw.line(surface, shadow, (x + 1, y + CELL_SIZE - 2),
                        (x + CELL_SIZE - 2, y + CELL_SIZE - 2))
        pygame.draw.line(surface, shadow, (x + CELL_SIZE - 2, y + 1),
                        (x + CELL_SIZE - 2, y + CELL_SIZE - 2))

        # Draw character image centered on the cell
        if image:
            img_rect = image.get_rect()
            img_rect.center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
            surface.blit(image, img_rect)


# =============================================================================
# GAME CLASS
# =============================================================================

class Game:
    """Main game controller."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chiikawa Tetris")

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Load Chiikawa character images
        self.piece_images = {}
        image_files = {
            'I': 'images/chiikawa.png',
            'O': 'images/hachiware.png',
            'T': 'images/usagi.png',
            'S': 'images/momonga.png',
            'Z': 'images/kurimanju.png',
            'J': 'images/armor.png',
            'L': 'images/ramen.png',
        }

        for piece_type, filepath in image_files.items():
            try:
                img = pygame.image.load(filepath)
                img = pygame.transform.smoothscale(img, (20, 20))
                self.piece_images[piece_type] = img
            except Exception as e:
                print(f"Warning: Could not load {filepath}: {e}")
                self.piece_images[piece_type] = None

        self.reset_game()

    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board = Board()
        self.current_piece: Optional[Piece] = None
        self.next_piece: Optional[Piece] = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False

        # Timing
        self.last_fall_time = pygame.time.get_ticks()
        self.fall_speed = FALL_SPEED

        # Generate the piece bag for randomization
        self.piece_bag: List[str] = []

        # Spawn first pieces
        self.spawn_piece()

    def get_next_piece_type(self) -> str:
        """Get next piece type using 7-bag randomization."""
        if not self.piece_bag:
            self.piece_bag = list(TETROMINOES.keys())
            random.shuffle(self.piece_bag)
        return self.piece_bag.pop()

    def spawn_piece(self) -> bool:
        """Spawn a new piece at the top. Returns False if game over."""
        if self.next_piece is None:
            piece_type = self.get_next_piece_type()
            self.next_piece = Piece(piece_type, self.piece_images.get(piece_type))

        self.current_piece = self.next_piece
        piece_type = self.get_next_piece_type()
        self.next_piece = Piece(piece_type, self.piece_images.get(piece_type))

        # Check if the spawn position is valid
        if not self.board.is_valid_position(self.current_piece.get_cells()):
            self.game_over = True
            return False

        self.last_fall_time = pygame.time.get_ticks()
        return True

    def move_piece(self, d_row: int, d_col: int) -> bool:
        """Try to move the current piece. Returns True if successful."""
        if self.current_piece is None:
            return False

        new_cells = self.current_piece.get_cells_at(
            self.current_piece.row + d_row,
            self.current_piece.col + d_col,
            self.current_piece.rotation_index
        )

        if self.board.is_valid_position(new_cells):
            self.current_piece.row += d_row
            self.current_piece.col += d_col
            return True
        return False

    def rotate_piece(self, clockwise: bool = True) -> bool:
        """Try to rotate the current piece. Returns True if successful."""
        if self.current_piece is None:
            return False

        new_rotation = (self.current_piece.rotate_cw() if clockwise
                       else self.current_piece.rotate_ccw())

        # Try rotation at current position
        new_cells = self.current_piece.get_cells_at(
            self.current_piece.row,
            self.current_piece.col,
            new_rotation
        )

        if self.board.is_valid_position(new_cells):
            self.current_piece.rotation_index = new_rotation
            return True

        # Wall kick: try shifting left/right
        for offset in [1, -1, 2, -2]:
            new_cells = self.current_piece.get_cells_at(
                self.current_piece.row,
                self.current_piece.col + offset,
                new_rotation
            )
            if self.board.is_valid_position(new_cells):
                self.current_piece.rotation_index = new_rotation
                self.current_piece.col += offset
                return True

        return False

    def hard_drop(self) -> None:
        """Drop the piece instantly to the bottom."""
        if self.current_piece is None:
            return

        # Count cells dropped for scoring
        cells_dropped = 0
        while self.move_piece(1, 0):
            cells_dropped += 1

        # Award points for hard drop
        self.score += cells_dropped * 2

        self.lock_piece()

    def lock_piece(self) -> None:
        """Lock the current piece and spawn a new one."""
        if self.current_piece is None:
            return

        self.board.lock_piece(self.current_piece)

        # Clear lines
        lines = self.board.clear_lines()
        if lines > 0:
            self.lines_cleared += lines
            self.score += self.calculate_score(lines)
            # Level up every 10 lines
            self.level = self.lines_cleared // 10 + 1
            # Speed up (but not below 100ms)
            self.fall_speed = max(100, FALL_SPEED - (self.level - 1) * 50)

        self.spawn_piece()

    def calculate_score(self, lines: int) -> int:
        """Calculate score for cleared lines."""
        # Classic Tetris scoring
        scores = {1: 100, 2: 300, 3: 500, 4: 800}
        return scores.get(lines, 0) * self.level

    def get_ghost_position(self) -> List[Tuple[int, int]]:
        """Get the position where the piece would land (ghost piece)."""
        if self.current_piece is None:
            return []

        ghost_row = self.current_piece.row
        while True:
            new_cells = self.current_piece.get_cells_at(
                ghost_row + 1,
                self.current_piece.col,
                self.current_piece.rotation_index
            )
            if self.board.is_valid_position(new_cells):
                ghost_row += 1
            else:
                break

        return self.current_piece.get_cells_at(
            ghost_row,
            self.current_piece.col,
            self.current_piece.rotation_index
        )

    def update(self) -> None:
        """Update game state."""
        if self.game_over or self.paused:
            return

        current_time = pygame.time.get_ticks()

        # Automatic piece falling
        if current_time - self.last_fall_time >= self.fall_speed:
            if not self.move_piece(1, 0):
                self.lock_piece()
            self.last_fall_time = current_time

    def handle_input(self, event: pygame.event.Event) -> None:
        """Handle keyboard input."""
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

        if self.game_over:
            if event.key == pygame.K_r:
                self.reset_game()
            return

        if event.key == pygame.K_p:
            self.paused = not self.paused
            return

        if self.paused:
            return

        if event.key == pygame.K_LEFT:
            self.move_piece(0, -1)
        elif event.key == pygame.K_RIGHT:
            self.move_piece(0, 1)
        elif event.key == pygame.K_DOWN:
            if self.move_piece(1, 0):
                self.score += 1  # Soft drop bonus
                self.last_fall_time = pygame.time.get_ticks()
        elif event.key == pygame.K_UP:
            self.rotate_piece(clockwise=True)
        elif event.key == pygame.K_SPACE:
            self.hard_drop()

    def draw(self) -> None:
        """Draw the entire game."""
        self.screen.fill(DARK_GRAY)

        # Draw board
        self.board.draw(self.screen, self.piece_images)

        # Draw ghost piece
        if self.current_piece and not self.game_over:
            ghost_cells = self.get_ghost_position()
            for row, col in ghost_cells:
                if row >= 0:
                    x = col * CELL_SIZE
                    y = row * CELL_SIZE
                    rect = pygame.Rect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4)
                    pygame.draw.rect(self.screen, GRAY, rect, 2)

        # Draw current piece
        if self.current_piece and not self.game_over:
            for row, col in self.current_piece.get_cells():
                if row >= 0:
                    self.board._draw_cell(self.screen, row, col,
                                         self.current_piece.color,
                                         self.current_piece.image)

        # Draw sidebar
        self._draw_sidebar()

        # Draw pause overlay
        if self.paused:
            self._draw_overlay("PAUSED", "Press P to resume")

        # Draw game over overlay
        if self.game_over:
            self._draw_overlay("GAME OVER", "Press R to restart")

        pygame.display.flip()

    def _draw_sidebar(self) -> None:
        """Draw the sidebar with score and next piece."""
        sidebar_x = BOARD_WIDTH * CELL_SIZE + 10

        # Score
        score_text = self.font.render("Score", True, WHITE)
        self.screen.blit(score_text, (sidebar_x, 20))
        score_value = self.font.render(str(self.score), True, WHITE)
        self.screen.blit(score_value, (sidebar_x, 50))

        # Level
        level_text = self.font.render("Level", True, WHITE)
        self.screen.blit(level_text, (sidebar_x, 100))
        level_value = self.font.render(str(self.level), True, WHITE)
        self.screen.blit(level_value, (sidebar_x, 130))

        # Lines
        lines_text = self.font.render("Lines", True, WHITE)
        self.screen.blit(lines_text, (sidebar_x, 180))
        lines_value = self.font.render(str(self.lines_cleared), True, WHITE)
        self.screen.blit(lines_value, (sidebar_x, 210))

        # Next piece
        next_text = self.font.render("Next", True, WHITE)
        self.screen.blit(next_text, (sidebar_x, 280))

        if self.next_piece:
            # Draw next piece preview
            preview_x = sidebar_x + 20
            preview_y = 320
            for dr, dc in self.next_piece.rotations[0]:
                x = preview_x + dc * 20
                y = preview_y + dr * 20
                # Draw colored background
                rect = pygame.Rect(x, y, 18, 18)
                pygame.draw.rect(self.screen, self.next_piece.color, rect)
                # Draw character image if available
                if self.next_piece.image:
                    scaled_img = pygame.transform.smoothscale(self.next_piece.image, (16, 16))
                    img_rect = scaled_img.get_rect()
                    img_rect.center = (x + 9, y + 9)
                    self.screen.blit(scaled_img, img_rect)

        # Controls help
        controls = [
            "Controls:",
            "← → Move",
            "↓ Soft drop",
            "↑ Rotate",
            "Space Hard drop",
            "P Pause",
        ]
        y = 420
        for line in controls:
            text = self.small_font.render(line, True, GRAY)
            self.screen.blit(text, (sidebar_x, y))
            y += 22

    def _draw_overlay(self, title: str, subtitle: str) -> None:
        """Draw a semi-transparent overlay with text."""
        # Semi-transparent background
        overlay = pygame.Surface((BOARD_WIDTH * CELL_SIZE, BOARD_HEIGHT * CELL_SIZE))
        overlay.fill(BLACK)
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        # Title
        title_text = self.font.render(title, True, WHITE)
        title_rect = title_text.get_rect(
            center=(BOARD_WIDTH * CELL_SIZE // 2, BOARD_HEIGHT * CELL_SIZE // 2 - 20)
        )
        self.screen.blit(title_text, title_rect)

        # Subtitle
        subtitle_text = self.small_font.render(subtitle, True, GRAY)
        subtitle_rect = subtitle_text.get_rect(
            center=(BOARD_WIDTH * CELL_SIZE // 2, BOARD_HEIGHT * CELL_SIZE // 2 + 20)
        )
        self.screen.blit(subtitle_text, subtitle_rect)

    def run(self) -> None:
        """Main game loop."""
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_input(event)

            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    game = Game()
    game.run()
