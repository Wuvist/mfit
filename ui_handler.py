"""
User interface handler for console I/O and user interaction.

Handles displaying instructions, collecting inputs, and presenting results.
"""

import sys
import os
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime


def clear_screen():
    """Clear the console screen."""
    os.system('clear' if os.name != 'nt' else 'cls')


def print_separator(width: int = 80, char: str = "="):
    """Print a separator line."""
    print(char * width)


def print_header(title: str, width: int = 80):
    """Print a formatted header."""
    print_separator(width)
    print(title.center(width))
    print_separator(width)


def display_welcome():
    """Display welcome message and application title."""
    clear_screen()
    print_header("MFIT - Measurement Fit")
    print("\nBody Measurement Capture System for Clothing Tailoring")
    print("Analyzes front and side photos to calculate body dimensions")
    print("\nTarget Accuracy: ± 1.5 cm")
    print_separator(80, "-")


def display_guidelines():
    """
    Display non-skippable photography guidelines.

    These guidelines are critical for measurement accuracy and must be
    shown to the user before they proceed.
    """
    print("\n")
    print_header("PHOTOGRAPHY GUIDELINES - PLEASE READ CAREFULLY", 80)
    print("\nFor accurate measurements, you MUST follow these guidelines:\n")

    print("1. CLOTHING:")
    print("   • Wear form-fitting athletic wear or compression clothing")
    print("   • Leggings or tight pants preferred")
    print("   • Avoid loose or baggy clothing\n")

    print("2. POSE:")
    print("   • Stand straight with good posture")
    print("   • Neutral A-Pose: arms slightly away from body (about 15-30 degrees)")
    print("   • Keep arms relaxed, not tense")
    print("   • Look straight ahead\n")

    print("3. CAMERA SETUP:")
    print("   • Position camera at mid-torso height")
    print("   • Keep camera level (not tilted up or down)")
    print("   • Distance: 2-3 meters from subject")
    print("   • Use timer or assistant to take photos\n")

    print("4. FRAMING:")
    print("   • Full body must be visible from head to feet")
    print("   • Include small margin above head and below feet")
    print("   • Center the person in the frame\n")

    print("5. ENVIRONMENT:")
    print("   • Plain, uncluttered background (wall preferred)")
    print("   • Even, diffused lighting (avoid harsh shadows)")
    print("   • Natural daylight or well-lit room\n")

    print("6. TWO PHOTOS REQUIRED:")
    print("   • FRONT VIEW: Face camera directly")
    print("   • SIDE VIEW: Stand perpendicular (90°), left or right side\n")

    print_separator(80, "-")
    print("\nNOTE: All processing is done locally. Your photos are never uploaded")
    print("      or transmitted. Images are discarded after the session ends.")
    print_separator(80, "-")


def get_user_consent() -> bool:
    """
    Get user consent to proceed after reading guidelines.

    Returns:
        True if user agrees to proceed, False otherwise
    """
    print("\n")
    while True:
        response = input("Have you read and understood the guidelines? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            print("\nPlease read the guidelines carefully before proceeding.")
            print("Type 'yes' when ready to continue, or press Ctrl+C to exit.")
        else:
            print("Please enter 'yes' or 'no'")


def validate_image_path(path_str: str, photo_type: str) -> Tuple[bool, str]:
    """
    Validate an image file path.

    Args:
        path_str: Path string to validate
        photo_type: Description of photo type (e.g., "front", "side")

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not path_str or path_str.strip() == "":
        return False, "Path cannot be empty"

    path = Path(path_str.strip())

    if not path.exists():
        return False, f"File not found: {path_str}"

    if not path.is_file():
        return False, f"Path is not a file: {path_str}"

    valid_extensions = ['.jpg', '.jpeg', '.png']
    if path.suffix.lower() not in valid_extensions:
        return False, f"Unsupported format. Please use {', '.join(valid_extensions)}"

    return True, ""


def get_image_path(photo_type: str) -> str:
    """
    Get and validate image path from user.

    Args:
        photo_type: Type of photo ("front" or "side")

    Returns:
        Valid image path as string
    """
    print(f"\n{photo_type.upper()} VIEW PHOTO:")

    while True:
        path_str = input(f"Enter path to {photo_type} view image: ").strip()

        is_valid, error_msg = validate_image_path(path_str, photo_type)

        if is_valid:
            return path_str
        else:
            print(f"  ✗ Error: {error_msg}")
            print("  Please try again.")


def get_height() -> float:
    """
    Get and validate height from user.

    Returns:
        Height in centimeters as float
    """
    print("\nHEIGHT MEASUREMENT:")
    print("Enter your height in centimeters (e.g., 175 for 175 cm)")

    while True:
        height_str = input("Height (cm): ").strip()

        try:
            height = float(height_str)

            if height <= 0:
                print("  ✗ Error: Height must be a positive number")
                continue

            if height < 100 or height > 250:
                print(f"  ⚠ Warning: {height} cm is outside typical range (100-250 cm)")
                confirm = input("  Is this correct? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    return height
                else:
                    print("  Please enter your height again.")
                    continue

            return height

        except ValueError:
            print("  ✗ Error: Please enter a valid number (e.g., 175)")


def collect_inputs() -> Tuple[str, str, float]:
    """
    Collect all required inputs from user.

    Returns:
        Tuple of (front_image_path, side_image_path, height_cm)
    """
    print("\n")
    print_separator(80, "=")
    print("INPUT COLLECTION".center(80))
    print_separator(80, "=")

    front_path = get_image_path("front")
    side_path = get_image_path("side")
    height = get_height()

    # Confirmation
    print("\n")
    print_separator(80, "-")
    print("CONFIRMATION:")
    print(f"  Front photo: {front_path}")
    print(f"  Side photo:  {side_path}")
    print(f"  Height:      {height} cm")
    print_separator(80, "-")

    while True:
        confirm = input("\nProceed with these inputs? (yes/no): ").strip().lower()
        if confirm in ['yes', 'y']:
            return front_path, side_path, height
        elif confirm in ['no', 'n']:
            print("\nRestarting input collection...")
            return collect_inputs()
        else:
            print("Please enter 'yes' or 'no'")


def display_processing():
    """Display processing message."""
    print("\n")
    print_separator(80, "=")
    print("PROCESSING".center(80))
    print_separator(80, "=")
    print("\nAnalyzing images and calculating measurements...")
    print("This may take a few seconds...\n")


def display_measurements(measurements: dict):
    """
    Display all body measurements in a formatted table.

    Args:
        measurements: Dictionary of measurements from calculator
    """
    print("\n")
    print_separator(80, "=")
    print("BODY MEASUREMENTS REPORT".center(80))
    print_separator(80, "=")

    # Basic info
    print(f"\nHeight: {measurements['height']:.1f} cm")

    # Linear measurements
    print("\n┌─ LINEAR MEASUREMENTS " + "─" * 56 + "┐")
    print(f"│ Shoulder Width:              {measurements['shoulder_width']:6.1f} cm" + " " * 26 + "│")
    print(f"│ Left Sleeve Length:           {measurements['left_sleeve_length']:6.1f} cm" + " " * 26 + "│")
    print(f"│ Right Sleeve Length:          {measurements['right_sleeve_length']:6.1f} cm" + " " * 26 + "│")
    print(f"│ Inseam:                       {measurements['inseam']:6.1f} cm" + " " * 26 + "│")
    print(f"│ Outseam:                      {measurements['outseam']:6.1f} cm" + " " * 26 + "│")
    print("└" + "─" * 78 + "┘")

    # Circumferential measurements
    print("\n┌─ CIRCUMFERENTIAL MEASUREMENTS " + "─" * 47 + "┐")
    print(f"│ Neck Circumference:           {measurements['neck_circumference']:6.1f} cm" + " " * 26 + "│")
    print(f"│ Chest Circumference:          {measurements['chest_circumference']:6.1f} cm" + " " * 26 + "│")
    print(f"│ Waist Circumference:          {measurements['waist_circumference']:6.1f} cm" + " " * 26 + "│")
    print(f"│ Hip Circumference:            {measurements['hip_circumference']:6.1f} cm" + " " * 26 + "│")
    print(f"│ Left Bicep Circumference:     {measurements['left_bicep_circumference']:6.1f} cm" + " " * 26 + "│")
    print(f"│ Right Bicep Circumference:    {measurements['right_bicep_circumference']:6.1f} cm" + " " * 26 + "│")
    print(f"│ Left Thigh Circumference:     {measurements['left_thigh_circumference']:6.1f} cm" + " " * 26 + "│")
    print(f"│ Right Thigh Circumference:    {measurements['right_thigh_circumference']:6.1f} cm" + " " * 26 + "│")
    print("└" + "─" * 78 + "┘")

    # Disclaimer
    print("\n" + "!" * 80)
    print("DISCLAIMER:".center(80))
    print("These measurements are estimates. Accuracy depends on photo quality.".center(80))
    print("For best results, follow all guidelines carefully.".center(80))
    print("!" * 80)


def format_measurements_for_file(measurements: dict) -> str:
    """
    Format measurements for text file export.

    Args:
        measurements: Dictionary of measurements from calculator

    Returns:
        Formatted string for file output
    """
    lines = []
    lines.append("=" * 80)
    lines.append("MFIT - BODY MEASUREMENTS REPORT")
    lines.append("=" * 80)
    lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"\nHeight: {measurements['height']:.1f} cm")

    lines.append("\n--- LINEAR MEASUREMENTS ---")
    lines.append(f"Shoulder Width:              {measurements['shoulder_width']:6.1f} cm")
    lines.append(f"Left Sleeve Length:           {measurements['left_sleeve_length']:6.1f} cm")
    lines.append(f"Right Sleeve Length:          {measurements['right_sleeve_length']:6.1f} cm")
    lines.append(f"Inseam:                       {measurements['inseam']:6.1f} cm")
    lines.append(f"Outseam:                      {measurements['outseam']:6.1f} cm")

    lines.append("\n--- CIRCUMFERENTIAL MEASUREMENTS ---")
    lines.append(f"Neck Circumference:           {measurements['neck_circumference']:6.1f} cm")
    lines.append(f"Chest Circumference:          {measurements['chest_circumference']:6.1f} cm")
    lines.append(f"Waist Circumference:          {measurements['waist_circumference']:6.1f} cm")
    lines.append(f"Hip Circumference:            {measurements['hip_circumference']:6.1f} cm")
    lines.append(f"Left Bicep Circumference:     {measurements['left_bicep_circumference']:6.1f} cm")
    lines.append(f"Right Bicep Circumference:    {measurements['right_bicep_circumference']:6.1f} cm")
    lines.append(f"Left Thigh Circumference:     {measurements['left_thigh_circumference']:6.1f} cm")
    lines.append(f"Right Thigh Circumference:    {measurements['right_thigh_circumference']:6.1f} cm")

    lines.append("\n" + "=" * 80)
    lines.append("DISCLAIMER:")
    lines.append("These measurements are estimates. Accuracy depends on photo quality.")
    lines.append("For best results, follow all guidelines carefully.")
    lines.append("=" * 80)

    return "\n".join(lines)


def export_measurements(measurements: dict) -> Optional[str]:
    """
    Offer to export measurements to a text file.

    Args:
        measurements: Dictionary of measurements from calculator

    Returns:
        Path to exported file if saved, None otherwise
    """
    print("\n")
    print_separator(80, "-")

    while True:
        response = input("Would you like to save these measurements to a file? (yes/no): ").strip().lower()

        if response in ['no', 'n']:
            return None
        elif response in ['yes', 'y']:
            break
        else:
            print("Please enter 'yes' or 'no'")

    # Get filename
    default_filename = f"measurements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    print(f"\nDefault filename: {default_filename}")

    while True:
        filename = input("Enter filename (press Enter for default): ").strip()

        if filename == "":
            filename = default_filename

        # Ensure .txt extension
        if not filename.endswith('.txt'):
            filename += '.txt'

        # Check if file exists
        if Path(filename).exists():
            overwrite = input(f"File '{filename}' already exists. Overwrite? (yes/no): ").strip().lower()
            if overwrite not in ['yes', 'y']:
                print("Please enter a different filename.")
                continue

        try:
            with open(filename, 'w') as f:
                f.write(format_measurements_for_file(measurements))
            print(f"\n✓ Measurements saved to: {filename}")
            return filename
        except Exception as e:
            print(f"\n✗ Error saving file: {e}")
            retry = input("Try again with a different filename? (yes/no): ").strip().lower()
            if retry not in ['yes', 'y']:
                return None


def display_error(error_message: str, error_type: str = "Error"):
    """
    Display an error message to the user.

    Args:
        error_message: The error message to display
        error_type: Type of error (e.g., "Error", "Warning")
    """
    print("\n")
    print_separator(80, "!")
    print(f"{error_type.upper()}".center(80))
    print_separator(80, "!")
    print(f"\n{error_message}\n")
    print_separator(80, "!")


def display_completion():
    """Display completion message."""
    print("\n")
    print_separator(80, "=")
    print("SESSION COMPLETE".center(80))
    print_separator(80, "=")
    print("\nThank you for using MFIT!")
    print("All image data has been discarded from memory.")
    print_separator(80, "-")
    print()
