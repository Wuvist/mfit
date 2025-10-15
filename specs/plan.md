# **Technical Implementation Plan: Tailor-Made Measurement Assistant**

Version: 1.0  
Date: 2025-10-15  
Related Document: Product Requirement Document v1.1

## **1\. Overview**

This document outlines the technical approach for developing the "Tailor-Made Measurement Assistant" console application. It details the project architecture, development phases, key algorithms, and testing strategy required to meet the specifications laid out in the PRD.

## **2\. Project Timeline & Milestones**

The project will be developed over a 4-week period, broken down into the following phases:

* **Week 1: Core Logic & Landmark Detection.**  
  * **Milestone:** Successfully detect and extract all necessary body landmarks from both front and side view images. Calibrate pixel-to-cm ratio.  
* **Week 2: Measurement Calculation.**  
  * **Milestone:** Implement and verify the mathematical formulas for all linear and circumferential measurements.  
* **Week 3: Application Workflow & User Interface.**  
  * **Milestone:** Develop the complete console user flow, from displaying instructions to exporting the final results.  
* **Week 4: Integration, Testing, and Refinement.**  
  * **Milestone:** A fully integrated and tested application that meets the accuracy and performance requirements.

## **3\. Software Architecture**

The application will be built with a modular architecture in Python to separate concerns and improve maintainability.

### **3.1. File Structure**

tailor-made-assistant/  
│  
├── main.py                 \# Main application entry point and orchestrator  
├── image\_processor.py      \# Handles image loading and landmark detection  
├── calculator.py           \# Contains all measurement calculation logic  
├── ui\_handler.py           \# Manages all console input and output  
├── utils.py                \# Helper functions (e.g., distance formulas)  
└── requirements.txt        \# Project dependencies

### **3.2. Data Flow Diagram**

1. **Start (main.py)** \-\> ui\_handler.py: Display welcome message and instructions.  
2. ui\_handler.py \-\> **User**: Prompt for front/side image paths and height.  
3. **User** \-\> ui\_handler.py: Provides input.  
4. ui\_handler.py \-\> main.py: Returns validated user inputs.  
5. main.py \-\> image\_processor.py: Passes image paths.  
6. image\_processor.py \-\> main.py: Returns dictionaries of landmark coordinates for both images.  
7. main.py \-\> calculator.py: Passes landmark data and user height.  
8. calculator.py \-\> main.py: Returns a dictionary of calculated body measurements.  
9. main.py \-\> ui\_handler.py: Passes the final measurements.  
10. ui\_handler.py \-\> **User**: Prints formatted results to the console.  
11. ui\_handler.py \-\> **User**: Prompts to save the file.  
12. **End**

## **4\. Key Algorithms & Logic**

### **4.1. Landmark Detection (image\_processor.py)**

* **Tool:** Use the mediapipe.solutions.pose model.  
* **Process:**  
  1. Initialize mp.solutions.pose.Pose with a high detection confidence (e.g., min\_detection\_confidence=0.5).  
  2. Load an image using cv2.imread().  
  3. Convert the image color from BGR to RGB, as MediaPipe expects RGB.  
  4. Process the image using the pose.process(image) method.  
  5. Check if results.pose\_landmarks exists. If not, raise an error indicating landmarks could not be found.  
  6. Iterate through the results.pose\_landmarks.landmark array and store the x, y coordinates for each required landmark in a dictionary. The image dimensions will be used to convert from normalized coordinates to pixel coordinates.

### **4.2. Measurement Calibration (calculator.py)**

* **Input:** User's height in cm (user\_height\_cm), and the top/bottom landmarks from the front image (e.g., top of head, heels).  
* **Process:**  
  1. Calculate the total height of the person in pixels (height\_px) by finding the vertical distance between the highest and lowest body landmarks in the front-view photo.  
  2. Calculate the pixel\_to\_cm\_ratio \= user\_height\_cm / height\_px. This ratio will be the conversion factor for all subsequent measurements.

### **4.3. Linear Measurements (calculator.py)**

* **Logic:** Use the Euclidean distance formula for any two points (landmarks) (x1, y1) and (x2, y2).  
* **Formula:** distance\_px \= sqrt((x2 \- x1)² \+ (y2 \- y1)²).  
* **Final Measurement:** measurement\_cm \= distance\_px \* pixel\_to\_cm\_ratio.  
* **Specifics:**  
  * **Sleeve Length:** This will be a multi-point calculation: distance from shoulder-to-elbow \+ distance from elbow-to-wrist.

### **4.4. Circumferential Measurements (calculator.py)**

* **Logic:** Model each body part as an ellipse. The width of the ellipse (d1) is derived from the front photo, and the depth (d2) is derived from the side photo.  
* **Process:**  
  1. For a given body part (e.g., waist), calculate the horizontal pixel distance between the left and right landmarks in the front photo. This is the major axis diameter.  
  2. Calculate the horizontal pixel distance between the front and back landmarks (or approximate depth) in the side photo. This is the minor axis diameter.  
  3. Define the semi-axes: a \= (d1 / 2\) and b \= (d2 / 2).  
  4. Use Ramanujan's second approximation for the circumference of an ellipse.  
* **Formula:** Circumference ≈ π \* \[3 \* (a \+ b) \- sqrt((3a \+ b) \* (a \+ 3b))\].  
* **Final Measurement:** circumference\_cm \= circumference\_px \* pixel\_to\_cm\_ratio.

## **5\. Development Phases in Detail**

### **Phase 1: Core Logic (Week 1\)**

* **Tasks:**  
  * Set up the Python environment (python \-m venv .venv).  
  * Install dependencies: pip install opencv-python mediapipe numpy.  
  * Implement get\_landmarks(image\_path) in image\_processor.py. This function will take a path and return a dictionary of landmark coordinates.  
  * Write a test script to run this function on sample images and print the detected coordinates to verify its correctness.

### **Phase 2: Measurement Implementation (Week 2\)**

* **Tasks:**  
  * Implement all measurement functions in calculator.py. Each function will take landmark data as input.  
  * calculate\_linear\_measurement(p1, p2, ratio)  
  * calculate\_circumference(diameter\_front, diameter\_side, ratio)  
  * Create a main calculate\_all(front\_landmarks, side\_landmarks, user\_height) function that orchestrates all calculations.  
  * Write unit tests to validate the math with dummy landmark data.

### **Phase 3: Console Interface (Week 3\)**

* **Tasks:**  
  * In ui\_handler.py, create functions for:  
    * display\_instructions()  
    * get\_user\_inputs(): Prompts for paths and height, includes loops for validation (file exists, height is numeric).  
    * display\_results(measurements\_dict)  
    * prompt\_to\_save(measurements\_dict)  
  * In main.py, write the main application loop that calls the UI and processing functions in the correct sequence.

### **Phase 4: Integration & Testing (Week 4\)**

* **Tasks:**  
  * Perform end-to-end testing using a set of test images taken according to the guidelines.  
  * Compare the program's output with manually taken measurements to assess accuracy.  
  * Implement robust error handling, such as try...except blocks for file I/O and for cases where MediaPipe fails to detect a person.  
  * Add comments and finalize documentation.

## **6\. Risks and Mitigation**

* **Risk:** Inaccurate measurements due to poor photo quality.  
  * **Mitigation:** The display\_instructions() function in ui\_handler.py is critical and must be clear and comprehensive. The disclaimer in the final output is also mandatory.  
* **Risk:** MediaPipe landmark detection is not 100% accurate and can vary.  
  * **Mitigation:** Use a high confidence threshold. Acknowledge this as a limitation of the underlying technology. The ± 1.5 cm accuracy target is a goal, not a guarantee.  
* **Risk:** The ellipse model for circumference is a simplification.  
  * **Mitigation:** This is an accepted approximation for this version. The PRD does not require a more complex model. This should be noted in the final disclaimer.