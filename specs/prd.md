# **Product Requirement Document: Tailor-Made Measurement Assistant**

Version: 1.1  
Date: 2025-10-15

## **1\. Executive Summary**

### **1.1. Project Overview**

The "Tailor-Made Measurement Assistant" is a Python-based **console application** designed to digitally capture a user's body measurements for clothing tailoring. By analyzing two user-submitted photographs (a front-facing and a side-facing view) and a known height measurement, the software will calculate key body dimensions typically required by tailors.

### **1.2. Purpose & Goals**

The primary goal is to offer a convenient, accurate, and contactless alternative to the traditional manual measurement process using a measuring tape. This tool aims to empower users to order custom-fit clothing online with confidence and to reduce the friction associated with visiting a physical tailor.

### **1.3. Target Audience**

* **Online Shoppers:** Individuals purchasing custom-made or made-to-measure clothing online.  
* **Fashion Tech Companies:** Businesses looking to integrate a digital measurement solution into their e-commerce platforms.  
* **Individuals:** Anyone needing their body measurements for personal use (e.g., fitness tracking, sewing projects) who may not have assistance for manual measurements.

## **2\. Functional Requirements**

### **2.1. User Input & Setup**

* **Image Input:** The application will prompt the user to enter the file paths for exactly two image files (e.g., .jpg, .png).  
  * One front-facing, full-body photograph.  
  * One side-facing (profile), full-body photograph.  
* **Height Input:** The application will prompt the user to enter their total height in centimeters (cm).  
* **Input Validation:**  
  * The system must validate that the provided file paths exist and the files are in a recognized image format.  
  * The system must validate that the height input is a positive numerical value within a reasonable range (e.g., 100-250 cm).

### **2.2. User Guidance**

When launched, the application must first print a clear, non-skippable set of instructions to the console to ensure measurement accuracy. These instructions will include:

* **Clothing:** "Wear form-fitting clothing, like athletic wear or leggings. Avoid baggy clothes."  
* **Stance:** "Stand straight in a neutral pose with feet shoulder-width apart and arms slightly out to your sides (A-Pose)."  
* **Camera Angle:** "Have someone take the photo at your mid-torso height, or set up your phone on a stable surface. Ensure the camera is level and not tilted."  
* **Framing:** "The photo must include your entire body, from the soles of your feet to the top of your head."  
* **Background:** "Stand in front of a plain, solid-colored background with good, even lighting. Avoid shadows."

### **2.3. Image Processing & Measurement Calculation**

* **Body Landmark Detection:** The system will use a computer vision library (e.g., MediaPipe Pose) to automatically detect and map key body landmarks (joints and key points) on both the front and side images.  
* **Calibration:** The user's provided height in cm will be used as the ground truth. The system will calculate a pixel-to-cm ratio by dividing the user's input height by their total height in pixels as measured in the front-facing photograph.  
* **Measurement Logic:**  
  1. **Linear Measurements (from front photo):** Calculate straight-line distances between relevant landmarks and convert from pixels to cm.  
     * **Shoulder Width:** Between the left and right shoulder landmarks.  
     * **Sleeve Length:** From the shoulder landmark, to the elbow, to the wrist landmark (for both arms).  
     * **Inseam:** From the crotch landmark to the interior ankle landmark.  
     * **Outseam:** From the waist landmark to the exterior ankle landmark.  
  2. **Circumferential Measurements (using both photos):** Estimate circumference by treating the body part as an ellipse, using the width from the front photo and the depth from the side photo.  
     * **Formula:** The system will use an ellipse circumference approximation (e.g., Ramanujan's second approximation) to calculate the final value.  
     * **Required Circumferences:** Neck, Chest/Bust, Waist, Hips, Biceps (both), and Thighs (both).

### **2.4. Output & Data Presentation**

* **Display Results:** The application will print the final calculated measurements to the console in a clear, formatted list.  
* **Measurement List:** The output must include the following measurements, clearly labeled and specified in centimeters (cm):  
  * Height  
  * Shoulder Width  
  * Chest Circumference  
  * Waist Circumference  
  * Hip Circumference  
  * Right Sleeve Length  
  * Left Sleeve Length  
  * Right Bicep Circumference  
  * Left Bicep Circumference  
  * Right Thigh Circumference  
  * Left Thigh Circumference  
  * Inseam  
  * Outseam  
* **Export Functionality:** After displaying the results, the user will be prompted with an option to export the measurement list to a .txt file for easy sharing and record-keeping.

## **3\. Non-Functional Requirements**

### **3.1. Accuracy**

* The system should target a measurement accuracy of **± 1.5 cm** compared to manual measurements taken by a professional, assuming user-provided photos meet the specified guidelines.  
* A disclaimer will be printed with the results: "These measurements are estimates. Accuracy depends on photo quality. For best results, follow all guidelines carefully."

### **3.2. Performance**

* From the point of submitting images and height, the total processing and calculation time should not exceed **20 seconds** on a standard consumer computer.

### **3.3. Usability & User Interaction**

* The application will be a command-line interface (CLI) program.  
* Interaction will be handled through text-based prompts and responses in the console.  
* The user journey will be linear and straightforward: Launch Program \-\> Display Instructions \-\> Prompt for Front Photo Path \-\> Prompt for Side Photo Path \-\> Prompt for Height \-\> Display Results \-\> Prompt to Save to File.

### **3.4. Privacy & Security**

* All image processing must be performed locally on the user's machine.  
* The application **must not** store, transmit, or upload the user's photographs to any external server or database. The images should be discarded from memory after the session is closed.

## **4\. System and Technical Requirements**

### **4.1. Dependencies**

* **Language:** Python 3.8 or higher.  
* **Libraries:**  
  * OpenCV-Python (cv2) for image handling.  
  * MediaPipe for pose and landmark detection.  
  * NumPy for numerical calculations.

### **4.2. Environment**

* The application should be a runnable Python script or a standalone executable that can run on Windows 10/11 and macOS.

## **5\. Future Enhancements (Out of Scope for v1.1)**

* 3D model generation of the user's body for visualization.  
* Advanced clothing fit visualization.  
* Video-based measurement capture for enhanced accuracy.  
* Mobile application (iOS/Android) versions.  
* Direct API integration with e-commerce tailoring platforms.