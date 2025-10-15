"""
Test script for the measurement calculator.

Usage:
    pixi run python test_calculator.py <front_image> <side_image> <height_cm>

Example:
    pixi run python test_calculator.py front.jpg side.jpg 175
"""

import sys
from image_processor import get_landmarks
from calculator import calculate_all_measurements


def format_measurements(measurements: dict) -> str:
    """
    Format measurements dictionary into readable output.

    Args:
        measurements: Dictionary of body measurements

    Returns:
        Formatted string with all measurements
    """
    output = []
    output.append("\n" + "=" * 70)
    output.append("BODY MEASUREMENTS REPORT")
    output.append("=" * 70)

    # Basic info
    output.append(f"\nHeight: {measurements['height']:.1f} cm")

    # Linear measurements
    output.append("\n--- Linear Measurements ---")
    output.append(f"Shoulder Width:        {measurements['shoulder_width']:.1f} cm")
    output.append(f"Left Sleeve Length:    {measurements['left_sleeve_length']:.1f} cm")
    output.append(f"Right Sleeve Length:   {measurements['right_sleeve_length']:.1f} cm")
    output.append(f"Inseam:                {measurements['inseam']:.1f} cm")
    output.append(f"Outseam:               {measurements['outseam']:.1f} cm")

    # Circumferential measurements
    output.append("\n--- Circumferential Measurements ---")
    output.append(f"Neck Circumference:    {measurements['neck_circumference']:.1f} cm")
    output.append(f"Chest Circumference:   {measurements['chest_circumference']:.1f} cm")
    output.append(f"Waist Circumference:   {measurements['waist_circumference']:.1f} cm")
    output.append(f"Hip Circumference:     {measurements['hip_circumference']:.1f} cm")
    output.append(f"Left Bicep Circumference:  {measurements['left_bicep_circumference']:.1f} cm")
    output.append(f"Right Bicep Circumference: {measurements['right_bicep_circumference']:.1f} cm")
    output.append(f"Left Thigh Circumference:  {measurements['left_thigh_circumference']:.1f} cm")
    output.append(f"Right Thigh Circumference: {measurements['right_thigh_circumference']:.1f} cm")

    # Disclaimer
    output.append("\n" + "=" * 70)
    output.append("DISCLAIMER:")
    output.append("These measurements are estimates. Accuracy depends on photo quality.")
    output.append("For best results, follow all guidelines carefully.")
    output.append("=" * 70)

    return "\n".join(output)


def main():
    if len(sys.argv) < 4:
        print("Usage: python test_calculator.py <front_image> <side_image> <height_cm>")
        print("\nExample:")
        print("  python test_calculator.py front.jpg side.jpg 175")
        sys.exit(1)

    front_image_path = sys.argv[1]
    side_image_path = sys.argv[2]

    try:
        user_height_cm = float(sys.argv[3])
    except ValueError:
        print(f"Error: Invalid height value '{sys.argv[3]}'. Must be a number.")
        sys.exit(1)

    # Validate height range
    if not (100 <= user_height_cm <= 250):
        print(f"Warning: Height {user_height_cm} cm is outside typical range (100-250 cm)")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)

    print("Processing images...")
    print("-" * 70)

    try:
        # Get landmarks from front image
        print(f"1. Detecting landmarks in front image: {front_image_path}")
        front_landmarks = get_landmarks(front_image_path)
        print(f"   ✓ Detected {len(front_landmarks)} landmarks")

        # Get landmarks from side image
        print(f"2. Detecting landmarks in side image: {side_image_path}")
        side_landmarks = get_landmarks(side_image_path)
        print(f"   ✓ Detected {len(side_landmarks)} landmarks")

        # Calculate all measurements
        print(f"3. Calculating measurements (height: {user_height_cm} cm)...")
        measurements = calculate_all_measurements(
            front_landmarks,
            side_landmarks,
            user_height_cm
        )
        print("   ✓ Calculations complete")

        # Display results
        print(format_measurements(measurements))

        # Offer to save results
        print("\n" + "-" * 70)
        save_option = input("Save results to file? (y/n): ")
        if save_option.lower() == 'y':
            output_file = "measurements.txt"
            with open(output_file, 'w') as f:
                f.write(format_measurements(measurements))
            print(f"Results saved to: {output_file}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"Error: Missing landmark {e}")
        print("This may indicate the pose was not detected correctly.")
        print("Please ensure photos follow the guidelines.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
