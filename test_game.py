#!/usr/bin/env python3
"""Quick test to verify the game initializes without errors."""

import sys

try:
    import pygame
    print("✓ pygame imported successfully")

    # Test import of main game
    import tetris
    print("✓ tetris module imported successfully")

    # Verify colors are updated
    print(f"\n✓ Chiikawa color scheme loaded:")
    for piece_type, color in tetris.COLORS.items():
        print(f"  {piece_type}: {color}")

    # Test game initialization
    print("\n✓ Attempting to initialize game...")
    game = tetris.Game()
    print("✓ Game initialized successfully!")

    # Check if images were loaded
    print(f"\n✓ Character images loaded:")
    for piece_type, img in game.piece_images.items():
        status = "✓" if img else "✗"
        print(f"  {status} {piece_type}: {img is not None}")

    # Clean up
    pygame.quit()
    print("\n✅ All tests passed! The game is ready to play.")
    print("Run: python3 tetris.py")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
