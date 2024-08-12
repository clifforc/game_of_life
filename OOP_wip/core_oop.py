from time import sleep
from typing import List, Tuple

import pygame
import numpy as np
from scipy.signal import convolve2d

import constants as c

# Set pygame window name
pygame.display.set_caption('Game of life')


class Cell:
    """
    Represent single cell in the game grid.

    This class handles the properties and drawing of individual cells.
    """
    def __init__(self, row: int, col: int, size: int, state: int = 0):
        """
        Initialize a Cell object.

        :param row: Row posotion of the cell in the grid.
        :param col: Column position of the cell in the grid.
        :param size: Size of the Cell in pixels.
        :param state: Initial state of the cell (0 - dead, 1 - alive).
        Default = 0.
        """
        self.row: int = row
        self.col: int = col
        self.size: int = size
        self.state: int = state

    def draw_cell(self, screen: pygame.Surface, color: Tuple[int, int, int]) -> None:
        """
        Draw Cell on the screen.

        :param screen: The surfase to draw the cell on.
        :param color: RGB color for the cell.
        """
        pygame.draw.rect(screen, color, (self.col * self.size,
                                         self.row * self.size,
                                         self.size - 1, self.size - 1))

