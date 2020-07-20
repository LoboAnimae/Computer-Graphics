""" Code adapted from Denn1s' user on GitHub.
    All Copyright goes to such user.
"""
from math import sqrt
import numpy


def glLine(x1: float, x2: float, y1: float, y2: float):
    """ Standard implementation of a line drawer.
        Allows the program to paint the points inside of
        a mathematical expression. 

        Most of it is adapted from an example. 

    Args:
        x1 (float): First X Coordinate
        x2 (float): Second X Coordinate
        y1 (float): First Y Coordinate
        y2 (float): Second Y Coordinate

    Returns:
        Array: An array with all the points to be redrawn on the screen.
    """
    dyx = [abs(y2 - y1), abs(x2 - x1)]
    if dyx[0] > dyx[1]:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
    sep = 0
    th = 0.5 * 2 * dyx[1]
    dyx = [abs(y2 - y1), abs(x2 - x1)]
    y = y1
    line = []

    for x in numpy.arange(x1, x2 + 0.01, 0.01):
        line.append((round(float(y), 3), round(float(x), 3))) if dyx[0] > dyx[1] else line.append(
            (round(float(x), 3), round(float(y), 3)))
        sep += dyx[0] * 2
        if sep >= (0.5 * 2 * dyx[1]):
            y += 0.01 if y1 < y2 else -0.01
            th += 1 * 2 * dyx[1]
    return line
