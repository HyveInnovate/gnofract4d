#!/usr/bin/env python3

COLOR_MAP = [
    (0.0, 0, 0, 0, 255),
    (1 / 256.0, 255, 255, 255, 255),
    (1.0, 255, 255, 255, 255)
]
LOCATION_PARAMS = [
    0.0, 0.0, 0.0, 0.0, # X Y Z W
    4.0, # Size or zoom
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0 # XY XZ XW YZ YW ZW planes (4D stuff)
]
TILE_SIZE = 64
