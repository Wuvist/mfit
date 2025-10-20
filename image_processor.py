"""
Image processing module for body landmark detection.

Uses MediaPipe Pose to detect body landmarks from images.
"""

import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path
from typing import Dict, Optional, Tuple


# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose


def get_landmarks(image_path: str) -> Dict[str, Tuple[float, float]]:
    """
    Detect body landmarks from an image using MediaPipe Pose.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary mapping landmark names to (x, y) pixel coordinates

    Raises:
        FileNotFoundError: If the image file does not exist
        ValueError: If the image cannot be loaded or landmarks cannot be detected
    """
    # Validate image path
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    if path.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
        raise ValueError(f"Unsupported image format: {path.suffix}. Use .jpg, .jpeg, or .png")

    # Load image
    image = cv2.imread(str(path))
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")

    # Get image dimensions
    height, width, _ = image.shape

    # Convert BGR to RGB (required by MediaPipe)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize MediaPipe Pose with specified confidence threshold
    with mp_pose.Pose(
        static_image_mode=True,
        min_detection_confidence=0.5,
        model_complexity=2  # Use highest quality model for best accuracy
    ) as pose:
        # Process the image
        results = pose.process(image_rgb)

        # Check if landmarks were detected
        if not results.pose_landmarks:
            raise ValueError(
                "No body landmarks detected. Please ensure:\n"
                "  - Full body is visible from head to feet\n"
                "  - Person is standing in A-pose (arms slightly out)\n"
                "  - Good lighting with plain background\n"
                "  - Camera is at mid-torso height"
            )

        # Convert normalized landmarks to pixel coordinates
        landmarks = {}
        for idx, landmark in enumerate(results.pose_landmarks.landmark):
            # Get landmark name from MediaPipe
            landmark_name = mp_pose.PoseLandmark(idx).name

            # Convert normalized coordinates (0-1) to pixel coordinates
            x_px = landmark.x * width
            y_px = landmark.y * height

            # Store as tuple
            landmarks[landmark_name] = (x_px, y_px)

    return landmarks


def visualize_landmarks(image_path: str, landmarks: Dict[str, Tuple[float, float]],
                        output_path: Optional[str] = None, show_landmark_label: bool = False) -> np.ndarray:
    """
    Draw detected landmarks on the image for visualization.

    Args:
        image_path: Path to the original image
        landmarks: Dictionary of landmark coordinates from get_landmarks()
        output_path: Optional path to save the annotated image
        show_landmark_label: If True, display landmark names on the image

    Returns:
        Annotated image as numpy array
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")

    # Draw landmarks
    for landmark_name, (x, y) in landmarks.items():
        cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), -1)

        # Draw landmark label if requested
        if show_landmark_label:
            cv2.putText(image, landmark_name, (int(x) + 10, int(y) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1, cv2.LINE_AA)

    # Save if output path provided
    if output_path:
        cv2.imwrite(output_path, image)

    return image
