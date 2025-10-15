"""
Measurement calculation module for body dimensions.

Converts landmark coordinates to real-world measurements using calibration
and calculates both linear and circumferential body measurements.
"""

import math
from typing import Dict, Tuple, Optional


def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.

    Args:
        p1: First point as (x, y) tuple
        p2: Second point as (x, y) tuple

    Returns:
        Distance in pixels
    """
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def ramanujan_ellipse_circumference(a: float, b: float) -> float:
    """
    Calculate ellipse circumference using Ramanujan's second approximation.

    Formula: C ≈ π * [3(a+b) - sqrt((3a+b)*(a+3b))]

    Args:
        a: Semi-major axis (or first semi-axis)
        b: Semi-minor axis (or second semi-axis)

    Returns:
        Approximate circumference
    """
    h = ((a - b) ** 2) / ((a + b) ** 2)
    # Ramanujan's second approximation
    circumference = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))
    return circumference


def calibrate_pixel_to_cm(front_landmarks: Dict[str, Tuple[float, float]],
                          user_height_cm: float) -> float:
    """
    Calculate the pixel-to-cm ratio using the user's known height.

    The ratio is calculated as: user_height_cm / height_in_pixels
    where height_in_pixels is the vertical distance between the highest
    and lowest body landmarks in the front-view photo.

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        user_height_cm: User's actual height in centimeters

    Returns:
        Pixel-to-cm conversion ratio

    Raises:
        ValueError: If landmarks are missing or invalid
    """
    if not front_landmarks:
        raise ValueError("Front landmarks dictionary is empty")

    if user_height_cm <= 0:
        raise ValueError(f"Invalid height: {user_height_cm}. Height must be positive.")

    # Find the highest and lowest points in the image
    # Typically: highest = top of head (NOSE or between eyes), lowest = feet (ANKLE)
    y_coordinates = [coord[1] for coord in front_landmarks.values()]

    if not y_coordinates:
        raise ValueError("No y-coordinates found in landmarks")

    min_y = min(y_coordinates)  # Top of body (lowest y-value)
    max_y = max(y_coordinates)  # Bottom of body (highest y-value)

    height_in_pixels = max_y - min_y

    if height_in_pixels <= 0:
        raise ValueError(f"Invalid height in pixels: {height_in_pixels}")

    pixel_to_cm_ratio = user_height_cm / height_in_pixels

    return pixel_to_cm_ratio


# ============================================================================
# LINEAR MEASUREMENTS (from front photo)
# ============================================================================

def calculate_shoulder_width(front_landmarks: Dict[str, Tuple[float, float]],
                             pixel_to_cm: float) -> float:
    """
    Calculate shoulder width from left to right shoulder.

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        pixel_to_cm: Pixel-to-cm conversion ratio

    Returns:
        Shoulder width in centimeters
    """
    left_shoulder = front_landmarks['LEFT_SHOULDER']
    right_shoulder = front_landmarks['RIGHT_SHOULDER']

    distance_px = euclidean_distance(left_shoulder, right_shoulder)
    return distance_px * pixel_to_cm


def calculate_sleeve_length(front_landmarks: Dict[str, Tuple[float, float]],
                            pixel_to_cm: float,
                            side: str = 'LEFT') -> float:
    """
    Calculate sleeve length from shoulder to wrist.

    Path: shoulder → elbow → wrist

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        pixel_to_cm: Pixel-to-cm conversion ratio
        side: 'LEFT' or 'RIGHT'

    Returns:
        Sleeve length in centimeters
    """
    shoulder = front_landmarks[f'{side}_SHOULDER']
    elbow = front_landmarks[f'{side}_ELBOW']
    wrist = front_landmarks[f'{side}_WRIST']

    # Calculate distances along the arm
    shoulder_to_elbow = euclidean_distance(shoulder, elbow)
    elbow_to_wrist = euclidean_distance(elbow, wrist)

    total_length_px = shoulder_to_elbow + elbow_to_wrist
    return total_length_px * pixel_to_cm


def calculate_inseam(front_landmarks: Dict[str, Tuple[float, float]],
                     pixel_to_cm: float) -> float:
    """
    Calculate inseam length from crotch to ankle.

    Uses average of left and right legs for better accuracy.

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        pixel_to_cm: Pixel-to-cm conversion ratio

    Returns:
        Inseam length in centimeters
    """
    # Use hip landmarks as proxy for crotch
    left_hip = front_landmarks['LEFT_HIP']
    right_hip = front_landmarks['RIGHT_HIP']
    crotch_x = (left_hip[0] + right_hip[0]) / 2
    crotch_y = max(left_hip[1], right_hip[1])  # Lower of the two hips
    crotch = (crotch_x, crotch_y)

    # Calculate for both legs and average
    left_ankle = front_landmarks['LEFT_ANKLE']
    right_ankle = front_landmarks['RIGHT_ANKLE']

    left_inseam_px = euclidean_distance(crotch, left_ankle)
    right_inseam_px = euclidean_distance(crotch, right_ankle)

    avg_inseam_px = (left_inseam_px + right_inseam_px) / 2
    return avg_inseam_px * pixel_to_cm


def calculate_outseam(front_landmarks: Dict[str, Tuple[float, float]],
                      pixel_to_cm: float) -> float:
    """
    Calculate outseam length from waist to ankle.

    Uses average of left and right legs for better accuracy.

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        pixel_to_cm: Pixel-to-cm conversion ratio

    Returns:
        Outseam length in centimeters
    """
    # Use hip landmarks as waist reference
    left_hip = front_landmarks['LEFT_HIP']
    right_hip = front_landmarks['RIGHT_HIP']

    left_ankle = front_landmarks['LEFT_ANKLE']
    right_ankle = front_landmarks['RIGHT_ANKLE']

    left_outseam_px = euclidean_distance(left_hip, left_ankle)
    right_outseam_px = euclidean_distance(right_hip, right_ankle)

    avg_outseam_px = (left_outseam_px + right_outseam_px) / 2
    return avg_outseam_px * pixel_to_cm


# ============================================================================
# CIRCUMFERENTIAL MEASUREMENTS (using both front and side photos)
# ============================================================================

def calculate_neck_circumference(front_landmarks: Dict[str, Tuple[float, float]],
                                 side_landmarks: Dict[str, Tuple[float, float]],
                                 pixel_to_cm: float) -> float:
    """
    Calculate neck circumference using ellipse approximation.

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        side_landmarks: Dictionary of landmark coordinates from side photo
        pixel_to_cm: Pixel-to-cm conversion ratio

    Returns:
        Neck circumference in centimeters
    """
    # Width: distance between left and right shoulders divided by factor
    # (neck is narrower than shoulders)
    left_shoulder_front = front_landmarks['LEFT_SHOULDER']
    right_shoulder_front = front_landmarks['RIGHT_SHOULDER']
    shoulder_width_px = euclidean_distance(left_shoulder_front, right_shoulder_front)

    # Approximate neck width as ~30% of shoulder width
    neck_width_px = shoulder_width_px * 0.30

    # Depth: use shoulder positions from side view
    # Find the front-most and back-most shoulder points
    left_shoulder_side = side_landmarks['LEFT_SHOULDER']
    right_shoulder_side = side_landmarks['RIGHT_SHOULDER']

    # In side view, x-coordinate represents depth
    x_coords = [left_shoulder_side[0], right_shoulder_side[0]]
    neck_depth_px = (max(x_coords) - min(x_coords)) * 0.30  # Approximate neck depth

    # If depth is too small, use a ratio of width
    if neck_depth_px < neck_width_px * 0.3:
        neck_depth_px = neck_width_px * 0.7  # Typical neck depth/width ratio

    # Calculate semi-axes
    a = (neck_width_px / 2) * pixel_to_cm
    b = (neck_depth_px / 2) * pixel_to_cm

    return ramanujan_ellipse_circumference(a, b)


def calculate_chest_circumference(front_landmarks: Dict[str, Tuple[float, float]],
                                  side_landmarks: Dict[str, Tuple[float, float]],
                                  pixel_to_cm: float) -> float:
    """
    Calculate chest circumference using ellipse approximation.

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        side_landmarks: Dictionary of landmark coordinates from side photo
        pixel_to_cm: Pixel-to-cm conversion ratio

    Returns:
        Chest circumference in centimeters
    """
    # Width: distance between left and right shoulders (approximately chest level)
    left_shoulder = front_landmarks['LEFT_SHOULDER']
    right_shoulder = front_landmarks['RIGHT_SHOULDER']
    chest_width_px = euclidean_distance(left_shoulder, right_shoulder) * 1.1  # Slightly wider

    # Depth: distance from front to back at shoulder level in side view
    left_shoulder_side = side_landmarks['LEFT_SHOULDER']
    right_shoulder_side = side_landmarks['RIGHT_SHOULDER']

    # Use average y-coordinate of shoulders to find chest level
    chest_y = (left_shoulder_side[1] + right_shoulder_side[1]) / 2

    # In side view, find body extent at chest level
    # Filter landmarks around chest height (±10% tolerance)
    tolerance = abs(left_shoulder_side[1] - side_landmarks['LEFT_HIP'][1]) * 0.2
    chest_level_points = [
        coord[0] for name, coord in side_landmarks.items()
        if abs(coord[1] - chest_y) < tolerance
    ]

    if chest_level_points:
        chest_depth_px = max(chest_level_points) - min(chest_level_points)
    else:
        # Fallback: use shoulder depth
        chest_depth_px = abs(left_shoulder_side[0] - right_shoulder_side[0])

    # Calculate semi-axes
    a = (chest_width_px / 2) * pixel_to_cm
    b = (chest_depth_px / 2) * pixel_to_cm

    return ramanujan_ellipse_circumference(a, b)


def calculate_waist_circumference(front_landmarks: Dict[str, Tuple[float, float]],
                                  side_landmarks: Dict[str, Tuple[float, float]],
                                  pixel_to_cm: float) -> float:
    """
    Calculate waist circumference using ellipse approximation.

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        side_landmarks: Dictionary of landmark coordinates from side photo
        pixel_to_cm: Pixel-to-cm conversion ratio

    Returns:
        Waist circumference in centimeters
    """
    # Width: distance between hips at waist level
    left_hip = front_landmarks['LEFT_HIP']
    right_hip = front_landmarks['RIGHT_HIP']
    waist_width_px = euclidean_distance(left_hip, right_hip)

    # Depth: body thickness at hip level in side view
    left_hip_side = side_landmarks['LEFT_HIP']
    right_hip_side = side_landmarks['RIGHT_HIP']
    waist_y = (left_hip_side[1] + right_hip_side[1]) / 2

    # Find body extent at waist level
    tolerance = abs(left_hip_side[1] - side_landmarks['LEFT_SHOULDER'][1]) * 0.1
    waist_level_points = [
        coord[0] for name, coord in side_landmarks.items()
        if abs(coord[1] - waist_y) < tolerance
    ]

    if waist_level_points:
        waist_depth_px = max(waist_level_points) - min(waist_level_points)
    else:
        # Fallback: use hip depth
        waist_depth_px = abs(left_hip_side[0] - right_hip_side[0])

    # Calculate semi-axes
    a = (waist_width_px / 2) * pixel_to_cm
    b = (waist_depth_px / 2) * pixel_to_cm

    return ramanujan_ellipse_circumference(a, b)


def calculate_hip_circumference(front_landmarks: Dict[str, Tuple[float, float]],
                                side_landmarks: Dict[str, Tuple[float, float]],
                                pixel_to_cm: float) -> float:
    """
    Calculate hip circumference using ellipse approximation.

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        side_landmarks: Dictionary of landmark coordinates from side photo
        pixel_to_cm: Pixel-to-cm conversion ratio

    Returns:
        Hip circumference in centimeters
    """
    # Width: distance between left and right hips
    left_hip = front_landmarks['LEFT_HIP']
    right_hip = front_landmarks['RIGHT_HIP']
    hip_width_px = euclidean_distance(left_hip, right_hip)

    # Depth: body thickness at hip level in side view
    left_hip_side = side_landmarks['LEFT_HIP']
    right_hip_side = side_landmarks['RIGHT_HIP']
    hip_y = (left_hip_side[1] + right_hip_side[1]) / 2

    # Find body extent at hip level
    tolerance = abs(left_hip_side[1] - side_landmarks['LEFT_KNEE'][1]) * 0.2
    hip_level_points = [
        coord[0] for name, coord in side_landmarks.items()
        if abs(coord[1] - hip_y) < tolerance
    ]

    if hip_level_points:
        hip_depth_px = max(hip_level_points) - min(hip_level_points)
    else:
        # Fallback
        hip_depth_px = abs(left_hip_side[0] - right_hip_side[0])

    # Calculate semi-axes
    a = (hip_width_px / 2) * pixel_to_cm
    b = (hip_depth_px / 2) * pixel_to_cm

    return ramanujan_ellipse_circumference(a, b)


def calculate_bicep_circumference(front_landmarks: Dict[str, Tuple[float, float]],
                                  side_landmarks: Dict[str, Tuple[float, float]],
                                  pixel_to_cm: float,
                                  side: str = 'LEFT') -> float:
    """
    Calculate bicep circumference using ellipse approximation.

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        side_landmarks: Dictionary of landmark coordinates from side photo
        pixel_to_cm: Pixel-to-cm conversion ratio
        side: 'LEFT' or 'RIGHT'

    Returns:
        Bicep circumference in centimeters
    """
    # Width: visible width of upper arm in front view
    shoulder = front_landmarks[f'{side}_SHOULDER']
    elbow = front_landmarks[f'{side}_ELBOW']

    # Midpoint between shoulder and elbow (bicep location)
    bicep_x_front = (shoulder[0] + elbow[0]) / 2
    bicep_y_front = (shoulder[1] + elbow[1]) / 2

    # Estimate width as a fraction of arm length
    arm_length_px = euclidean_distance(shoulder, elbow)
    bicep_width_px = arm_length_px * 0.20  # Typical bicep width relative to upper arm length

    # Depth: use side view
    shoulder_side = side_landmarks[f'{side}_SHOULDER']
    elbow_side = side_landmarks[f'{side}_ELBOW']

    # Estimate depth similarly
    arm_length_side_px = euclidean_distance(shoulder_side, elbow_side)
    bicep_depth_px = arm_length_side_px * 0.20

    # Calculate semi-axes
    a = (bicep_width_px / 2) * pixel_to_cm
    b = (bicep_depth_px / 2) * pixel_to_cm

    return ramanujan_ellipse_circumference(a, b)


def calculate_thigh_circumference(front_landmarks: Dict[str, Tuple[float, float]],
                                  side_landmarks: Dict[str, Tuple[float, float]],
                                  pixel_to_cm: float,
                                  side: str = 'LEFT') -> float:
    """
    Calculate thigh circumference using ellipse approximation.

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        side_landmarks: Dictionary of landmark coordinates from side photo
        pixel_to_cm: Pixel-to-cm conversion ratio
        side: 'LEFT' or 'RIGHT'

    Returns:
        Thigh circumference in centimeters
    """
    # Width: visible width of thigh in front view
    hip = front_landmarks[f'{side}_HIP']
    knee = front_landmarks[f'{side}_KNEE']

    # Use distance slightly below hip as thigh width
    thigh_length_px = euclidean_distance(hip, knee)
    thigh_width_px = thigh_length_px * 0.25  # Typical thigh width relative to length

    # Depth: use side view
    hip_side = side_landmarks[f'{side}_HIP']
    knee_side = side_landmarks[f'{side}_KNEE']

    thigh_length_side_px = euclidean_distance(hip_side, knee_side)
    thigh_depth_px = thigh_length_side_px * 0.25

    # Calculate semi-axes
    a = (thigh_width_px / 2) * pixel_to_cm
    b = (thigh_depth_px / 2) * pixel_to_cm

    return ramanujan_ellipse_circumference(a, b)


# ============================================================================
# MAIN CALCULATION FUNCTION
# ============================================================================

def calculate_all_measurements(
    front_landmarks: Dict[str, Tuple[float, float]],
    side_landmarks: Dict[str, Tuple[float, float]],
    user_height_cm: float
) -> Dict[str, float]:
    """
    Calculate all body measurements from front and side photos.

    Args:
        front_landmarks: Dictionary of landmark coordinates from front photo
        side_landmarks: Dictionary of landmark coordinates from side photo
        user_height_cm: User's actual height in centimeters

    Returns:
        Dictionary with all measurements in centimeters

    Raises:
        ValueError: If landmarks are missing or invalid
    """
    # Calibrate pixel-to-cm ratio using front photo
    pixel_to_cm = calibrate_pixel_to_cm(front_landmarks, user_height_cm)

    # Calculate all measurements
    measurements = {
        # User input
        'height': user_height_cm,

        # Linear measurements
        'shoulder_width': calculate_shoulder_width(front_landmarks, pixel_to_cm),
        'left_sleeve_length': calculate_sleeve_length(front_landmarks, pixel_to_cm, 'LEFT'),
        'right_sleeve_length': calculate_sleeve_length(front_landmarks, pixel_to_cm, 'RIGHT'),
        'inseam': calculate_inseam(front_landmarks, pixel_to_cm),
        'outseam': calculate_outseam(front_landmarks, pixel_to_cm),

        # Circumferential measurements
        'neck_circumference': calculate_neck_circumference(
            front_landmarks, side_landmarks, pixel_to_cm
        ),
        'chest_circumference': calculate_chest_circumference(
            front_landmarks, side_landmarks, pixel_to_cm
        ),
        'waist_circumference': calculate_waist_circumference(
            front_landmarks, side_landmarks, pixel_to_cm
        ),
        'hip_circumference': calculate_hip_circumference(
            front_landmarks, side_landmarks, pixel_to_cm
        ),
        'left_bicep_circumference': calculate_bicep_circumference(
            front_landmarks, side_landmarks, pixel_to_cm, 'LEFT'
        ),
        'right_bicep_circumference': calculate_bicep_circumference(
            front_landmarks, side_landmarks, pixel_to_cm, 'RIGHT'
        ),
        'left_thigh_circumference': calculate_thigh_circumference(
            front_landmarks, side_landmarks, pixel_to_cm, 'LEFT'
        ),
        'right_thigh_circumference': calculate_thigh_circumference(
            front_landmarks, side_landmarks, pixel_to_cm, 'RIGHT'
        ),
    }

    return measurements
