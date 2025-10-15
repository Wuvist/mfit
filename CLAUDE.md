# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**mfit** (Measurement Fit) is a Python console application that captures body measurements for clothing tailoring by analyzing two photographs (front and side view) along with a known height measurement. The system uses computer vision to detect body landmarks and calculate key dimensions required by tailors.

**Target Accuracy:** ± 1.5 cm compared to manual measurements
**Performance Target:** < 20 seconds processing time

## Package Management

This project uses **Pixi** (https://pixi.sh) for environment and dependency management.

**Key Commands:**
- `pixi install` - Install/update all dependencies
- `pixi run <task>` - Run a defined task (once tasks are added to pixi.toml)
- `pixi shell` - Activate the project environment

Dependencies are declared in `pixi.toml` and locked in `pixi.lock`. The project targets Python 3.12 on macOS ARM64.

## Architecture

The application follows a modular architecture with clear separation of concerns:

### Planned Module Structure

```
main.py              # Entry point and orchestrator
image_processor.py   # Image loading and MediaPipe landmark detection
calculator.py        # All measurement calculation logic
ui_handler.py        # Console I/O and user interaction
utils.py            # Helper functions (distance formulas, etc.)
```

### Core Dependencies

- **OpenCV-Python (cv2)** - Image handling
- **MediaPipe** - Pose and landmark detection
- **NumPy** - Numerical calculations

### Data Flow

1. `ui_handler.py` displays instructions and collects inputs (2 image paths + height in cm)
2. `image_processor.py` detects body landmarks using MediaPipe Pose
3. `calculator.py` calibrates pixel-to-cm ratio using user height, then calculates measurements
4. `ui_handler.py` displays results and optionally exports to .txt file

## Key Technical Details

### Landmark Detection (image_processor.py)

- Uses `mediapipe.solutions.pose` with min_detection_confidence=0.5
- Images must be converted from BGR to RGB before processing
- Returns dictionary of landmark coordinates (converted from normalized to pixel coordinates)

### Calibration (calculator.py)

The pixel-to-cm ratio is calculated as:
```
pixel_to_cm_ratio = user_height_cm / height_in_pixels
```
where `height_in_pixels` is the vertical distance between the highest and lowest body landmarks in the front-view photo.

### Measurement Types

**Linear Measurements** (from front photo):
- Shoulder Width, Sleeve Length (shoulder→elbow→wrist), Inseam, Outseam
- Formula: `distance_cm = euclidean_distance_px * pixel_to_cm_ratio`

**Circumferential Measurements** (using both photos):
- Neck, Chest, Waist, Hips, Biceps (both), Thighs (both)
- Models body parts as ellipses using width from front photo and depth from side photo
- Uses Ramanujan's second approximation: `C ≈ π * [3(a+b) - sqrt((3a+b)*(a+3b))]`
  where `a` and `b` are the semi-axes

### Required Measurements Output

All measurements in centimeters (cm):
- Height, Shoulder Width
- Chest/Waist/Hip Circumference
- Right/Left Sleeve Length
- Right/Left Bicep Circumference
- Right/Left Thigh Circumference
- Inseam, Outseam

## Privacy & Security Requirements

- **All processing must be local** - No image upload or external transmission
- Images must be discarded from memory after session ends
- No persistent storage of user photos

## User Guidelines (Displayed at Startup)

The application must display these non-skippable instructions:
- Wear form-fitting clothing (athletic wear, leggings)
- Stand straight in neutral A-Pose (arms slightly out)
- Camera at mid-torso height, level (not tilted)
- Full body visible from head to feet
- Plain background with even lighting, no shadows

## Input Validation

- Image paths: must exist and be recognized formats (.jpg, .png)
- Height: positive numerical value, reasonable range (100-250 cm)

## Error Handling

- Handle cases where MediaPipe fails to detect landmarks
- Use try-except blocks for file I/O operations
- Provide clear error messages when photos don't meet quality requirements

## Output Format

Results must include:
1. Formatted list of all measurements printed to console
2. Mandatory disclaimer: "These measurements are estimates. Accuracy depends on photo quality. For best results, follow all guidelines carefully."
3. Optional export to .txt file for record-keeping
