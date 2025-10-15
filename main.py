#!/usr/bin/env python3
"""
MFIT - Measurement Fit
Body Measurement Capture System for Clothing Tailoring

Main entry point for the application.
"""

import sys
import traceback
from image_processor import get_landmarks
from calculator import calculate_all_measurements
from ui_handler import (
    display_welcome,
    display_guidelines,
    get_user_consent,
    collect_inputs,
    display_processing,
    display_measurements,
    export_measurements,
    display_error,
    display_completion
)


def main():
    """
    Main application orchestrator.

    Coordinates the flow:
    1. Display welcome and guidelines
    2. Get user consent
    3. Collect inputs (2 images + height)
    4. Process images (detect landmarks)
    5. Calculate measurements
    6. Display results
    7. Optionally export to file
    """
    try:
        # Step 1: Welcome and guidelines
        display_welcome()
        display_guidelines()

        # Step 2: Get user consent
        if not get_user_consent():
            print("\nExiting application.")
            sys.exit(0)

        # Step 3: Collect inputs
        front_image_path, side_image_path, height_cm = collect_inputs()

        # Step 4: Display processing message
        display_processing()

        # Step 5: Process front image
        print("Step 1/3: Detecting landmarks in front view photo...")
        try:
            front_landmarks = get_landmarks(front_image_path)
            print(f"  ✓ Successfully detected {len(front_landmarks)} landmarks in front view")
        except ValueError as e:
            display_error(
                f"Failed to process front view photo:\n{str(e)}\n\n"
                "Please ensure your front view photo follows all guidelines:\n"
                "  - Full body visible from head to feet\n"
                "  - Standing in A-pose (arms slightly out)\n"
                "  - Good lighting and plain background",
                "Processing Error"
            )
            sys.exit(1)
        except Exception as e:
            display_error(f"Unexpected error processing front view photo:\n{str(e)}")
            sys.exit(1)

        # Step 6: Process side image
        print("\nStep 2/3: Detecting landmarks in side view photo...")
        try:
            side_landmarks = get_landmarks(side_image_path)
            print(f"  ✓ Successfully detected {len(side_landmarks)} landmarks in side view")
        except ValueError as e:
            display_error(
                f"Failed to process side view photo:\n{str(e)}\n\n"
                "Please ensure your side view photo follows all guidelines:\n"
                "  - Full body visible from head to feet\n"
                "  - Standing perpendicular to camera (90° angle)\n"
                "  - Same pose as front view (A-pose)\n"
                "  - Good lighting and plain background",
                "Processing Error"
            )
            sys.exit(1)
        except Exception as e:
            display_error(f"Unexpected error processing side view photo:\n{str(e)}")
            sys.exit(1)

        # Step 7: Calculate measurements
        print("\nStep 3/3: Calculating body measurements...")
        try:
            measurements = calculate_all_measurements(
                front_landmarks,
                side_landmarks,
                height_cm
            )
            print("  ✓ All measurements calculated successfully")
        except ValueError as e:
            display_error(
                f"Failed to calculate measurements:\n{str(e)}\n\n"
                "This may indicate an issue with landmark detection.\n"
                "Please ensure both photos follow all guidelines.",
                "Calculation Error"
            )
            sys.exit(1)
        except KeyError as e:
            display_error(
                f"Missing required landmark: {str(e)}\n\n"
                "This indicates the body pose was not detected correctly.\n"
                "Please ensure:\n"
                "  - You are standing in A-pose (arms slightly away from body)\n"
                "  - Full body is visible in both photos\n"
                "  - Photos are clear and well-lit",
                "Landmark Error"
            )
            sys.exit(1)
        except Exception as e:
            display_error(f"Unexpected error during calculations:\n{str(e)}")
            if '--debug' in sys.argv:
                traceback.print_exc()
            sys.exit(1)

        # Step 8: Display results
        display_measurements(measurements)

        # Step 9: Offer to export
        export_measurements(measurements)

        # Step 10: Completion
        display_completion()

        # Clean up (explicit memory cleanup)
        del front_landmarks
        del side_landmarks
        del measurements

        sys.exit(0)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        display_error(f"An unexpected error occurred:\n{str(e)}")
        if '--debug' in sys.argv:
            print("\nDebug traceback:")
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
