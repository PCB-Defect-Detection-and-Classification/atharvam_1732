# 🛠️ Technical Report: AI-Based PCB Defect Detection System

**Project:** Automated PCB Defect Detection & Classification
**Version:** 1.0 (Final Release)
**Date:** December 2025
**Author:** Atharva Mundke
**Context:** Internship Capstone Project

---

## 1. Executive Summary
This report documents the design, implementation, and evaluation of an automated optical inspection (AOI) system for Printed Circuit Boards (PCBs). The objective was to eliminate manual inspection errors by developing a computer vision pipeline capable of detecting six specific manufacturing defects.

The final system integrates a robust feature-matching alignment algorithm with a custom-tuned Convolutional Neural Network (EfficientNetB0). It achieves a **Validation Accuracy of 97.80%** and demonstrates **100% Recall** on critical failure modes (Open Circuits and Shorts), proving its viability for deployment in quality assurance workflows.

---

## 2. System Architecture

The solution implements a two-stage sequential architecture:
1.  **Stage 1: ROI Localization (Computer Vision)** - Deterministic algorithms locate potential anomalies.
2.  **Stage 2: Defect Classification (Deep Learning)** - Probabilistic models classify the anomaly type.

### 2.1. The Processing Pipeline
1.  **Reference Alignment (Registration):**
    * **Algorithm:** ORB (Oriented FAST and Rotated BRIEF).
    * **Mechanism:** Feature keypoints are extracted from both the "Golden Template" and the "Test Board." A Homography matrix is computed to warp the Test Board, aligning it pixel-perfectly with the reference template.
    * **Justification:** ORB provides rotational invariance and is computationally superior to SIFT for real-time applications.

2.  **Anomaly Extraction:**
    * **Technique:** Image Subtraction & Morphological Filtering.
    * **Mechanism:** `absdiff(Template, Test)` computes the pixel-wise difference. A series of morphological operations (Erosion/Dilation) removes environmental noise (e.g., dust, lighting glare) while preserving significant defect contours.

---

## 3. Technical Innovations & Optimization

### 3.1. The "Heavy Head" Architecture
**Challenge:** The baseline EfficientNetB0 model exhibited high confusion rates between geometrically similar classes (e.g., *Spur* vs. *Spurious Copper*), plateauing at ~92% accuracy.

**Solution:** A custom classification head was engineered to increase model capacity.
* **Backbone:** EfficientNetB0 (ImageNet Weights, Frozen).
* **Custom Head:**
    * `GlobalAveragePooling2D`
    * `Dense(256, activation='relu')` **(Feature Projection Layer)**
    * `Dropout(0.3)` **(Regularization)**
    * `Dense(6, activation='softmax')`

**Impact:** The addition of the 256-unit dense layer introduced necessary non-linearity, allowing the model to learn complex decision boundaries. This architectural change directly contributed to the final **97.8% accuracy**.

### 3.2. "Dual-Box" Inference Strategy
**Challenge:** During inference, "Open Circuits" were frequently misclassified as "Shorts" due to aspect ratio distortion when tight bounding boxes were resized to the model's input size (128x128).

**Solution:** A decoupled inference logic was implemented:
* **Visualization Box:** Tight crop (`padding=5px`) for precise UI rendering.
* **Inference Box:** Fixed-context crop (`padding=20px`) for the Neural Network.

**Impact:** By guaranteeing sufficient context (surrounding copper tracks), the model could reliably distinguish between a break in a track (Open) and a bridge between tracks (Short), achieving **0 misclassifications** between these critical categories.

---

## 4. Performance Evaluation

### 4.1. Metrics
The model was evaluated on a held-out validation set derived from the DeepPCB dataset.

* **Final Validation Accuracy:** **97.80%**
* **Training Accuracy:** 99.1%
* **Loss Function:** Categorical Cross-Entropy
* **Optimizer:** Adam (`lr=0.001`) with `ReduceLROnPlateau` scheduling.

### 4.2. Critical Class Performance
| Defect Type | Precision | Recall | Significance |
| :--- | :--- | :--- | :--- |
| **Open Circuit** | 98.5% | **100%** | Critical (Electrical Failure) |
| **Short** | 99.0% | **100%** | Critical (Electrical Failure) |
| **Mouse Bite** | 97.2% | 96.5% | Structural Weakness |

---

## 5. Technology Stack
* **Language:** Python 3.11.9
* **Computer Vision:** OpenCV 4.8
* **Deep Learning:** TensorFlow/Keras 2.14
* **Web Interface:** Streamlit
* **Deployment:** Streamlit Cloud (CI/CD via GitHub)

---

## 6. Conclusion
The project successfully delivers an automated inspection tool that meets the internship requirements for accuracy and usability. The integration of the "Dual-Box" strategy and the "Heavy Head" architecture solved the initial stability issues, resulting in a reliable system capable of identifying defects with **97.8% accuracy**.