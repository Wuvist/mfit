"""
Utility functions for the mfit application.

Contains helper functions used across multiple modules.
"""

import math
import os
from typing import Tuple, List
from pathlib import Path


def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.

    Args:
        p1: First point as (x, y) tuple
        p2: Second point as (x, y) tuple

    Returns:
        Distance between the points
    """
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def validate_image_path(image_path: str) -> bool:
    """
    Validate that an image path exists and has a supported format.

    Args:
        image_path: Path to the image file

    Returns:
        True if valid, False otherwise
    """
    path = Path(image_path)

    if not path.exists():
        return False

    if path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
        return False

    return True


def validate_height(height_cm: float) -> bool:
    """
    Validate that a height value is within reasonable range.

    Args:
        height_cm: Height in centimeters

    Returns:
        True if valid, False otherwise
    """
    return 100 <= height_cm <= 250


def format_measurement(value: float, unit: str = "cm", decimal_places: int = 1) -> str:
    """
    Format a measurement value with unit.

    Args:
        value: Measurement value
        unit: Unit of measurement (default: "cm")
        decimal_places: Number of decimal places (default: 1)

    Returns:
        Formatted string
    """
    return f"{value:.{decimal_places}f} {unit}"


def get_midpoint(p1: Tuple[float, float], p2: Tuple[float, float]) -> Tuple[float, float]:
    """
    Calculate the midpoint between two points.

    Args:
        p1: First point as (x, y) tuple
        p2: Second point as (x, y) tuple

    Returns:
        Midpoint as (x, y) tuple
    """
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)


def clear_screen():
    """
    Clear the console screen.
    """
    os.system('clear' if os.name != 'nt' else 'cls')


def print_header(title: str, width: int = 70):
    """
    Print a formatted header.

    Args:
        title: Header title
        width: Total width of the header (default: 70)
    """
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width + "\n")


def print_section(title: str, width: int = 70):
    """
    Print a section separator.

    Args:
        title: Section title
        width: Total width (default: 70)
    """
    print("\n" + "-" * width)
    print(title)
    print("-" * width)
