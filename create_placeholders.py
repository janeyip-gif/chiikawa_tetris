#!/usr/bin/env python3
"""
Create placeholder images for Chiikawa characters.
These are temporary placeholders - replace with actual character images later!

To create proper images:
1. Find Chiikawa character PNG images (24x24 pixels recommended)
2. Save them in the images/ directory with the correct names
3. Make sure they have transparent backgrounds

Suggested characters:
- chiikawa.png: Chiikawa (main character)
- hachiware.png: Hachiware (black & white cat)
- usagi.png: Usagi (rabbit)
- momonga.png: Momonga (flying squirrel)
- kurimanju.png: Kurimanju (chestnut)
- armor.png: Armor-san
- ramen.png: Ramen Master
"""

import pygame
import os

# Initialize pygame
pygame.init()

# Character info: (name, color for placeholder)
characters = {
    'chiikawa': (173, 216, 230),    # Light blue
    'hachiware': (255, 250, 205),   # Lemon chiffon
    'usagi': (221, 160, 221),       # Plum
    'momonga': (189, 252, 201),     # Mint green
    'kurimanju': (255, 182, 193),   # Light pink
    'armor': (176, 196, 222),       # Light steel blue
    'ramen': (255, 218, 185),       # Peach puff
}

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Create placeholder images
size = 24
for name, color in characters.items():
    # Create a surface
    surface = pygame.Surface((size, size), pygame.SRCALPHA)

    # Draw a circle
    pygame.draw.circle(surface, color, (size // 2, size // 2), size // 2 - 2)

    # Add a white outline
    pygame.draw.circle(surface, (255, 255, 255), (size // 2, size // 2), size // 2 - 2, 2)

    # Save the image
    filepath = f'images/{name}.png'
    pygame.image.save(surface, filepath)
    print(f'Created placeholder: {filepath}')

print('\nPlaceholder images created!')
print('Replace these with actual Chiikawa character images for the best effect.')
print('Recommended size: 24x24 pixels with transparent background')
