"""
Simple test script for the get_landmarks function.

Usage:
    pixi run python test_landmarks.py <path_to_image>

Example:
    pixi run python test_landmarks.py test_front.jpg
"""

import sys
from image_processor import get_landmarks, visualize_landmarks


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_landmarks.py <path_to_image>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        print(f"Processing image: {image_path}")
        print("-" * 60)

        # Get landmarks
        landmarks = get_landmarks(image_path)

        print(f"Successfully detected {len(landmarks)} landmarks!\n")

        # Print some key landmarks
        key_landmarks = [
            'NOSE', 'LEFT_SHOULDER', 'RIGHT_SHOULDER',
            'LEFT_HIP', 'RIGHT_HIP', 'LEFT_ANKLE', 'RIGHT_ANKLE'
        ]

        print("Key landmark coordinates (in pixels):")
        for landmark_name in key_landmarks:
            if landmark_name in landmarks:
                x, y = landmarks[landmark_name]
                print(f"  {landmark_name:20s}: ({x:7.2f}, {y:7.2f})")

        print("\n" + "-" * 60)
        print(f"Total landmarks detected: {len(landmarks)}")
        print("\nAll landmark names:")
        for name in sorted(landmarks.keys()):
            print(f"  - {name}")

        # Optionally create visualization
        print("\n" + "-" * 60)
        output_path = image_path.rsplit('.', 1)[0] + '_annotated.jpg'
        visualize_landmarks(image_path, landmarks, output_path)
        print(f"Annotated image saved to: {output_path}")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
