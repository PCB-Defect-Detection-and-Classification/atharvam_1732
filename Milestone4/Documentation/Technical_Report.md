# 🛠️ Technical Report: AI-Based PCB Defect Detection System

**Project:** Automated PCB Defect Detection & Classification
**Version:** 1.0 (Final Release)
**Date:** December 2025
**Author:** Atharva Mundke
**Context:** Internship Capstone Project

---

## 1. Executive Summary
This report documents the design, implementation, and evaluation of an automated optical inspection (AOI) system for Printed Circuit Boards (PCBs). The objective was to eliminate manual inspection errors by developing a computer vision pipeline capable of detecting six specific manufacturing defects.

The final system evolves beyond a simple prototype into an **Industrial-Grade QA Platform**. It integrates a robust feature-matching alignment algorithm with a custom-tuned Convolutional Neural Network (EfficientNetB0) and a persistent SQLite database backbone. The system achieves a **Validation Accuracy of 97.80%**, demonstrates **100% Recall** on critical failure modes, and provides real-time financial impact analysis for manufacturing decision-making.

---

## 2. System Architecture

The solution implements a three-stage sequential architecture:
1.  **Stage 1: ROI Localization (Computer Vision)** - Deterministic algorithms locate potential anomalies.
2.  **Stage 2: Defect Classification (Deep Learning)** - Probabilistic models classify the anomaly type.
3.  **Stage 3: Business Intelligence (Analytics)** - Rule-based engines calculate financial impact and store audit logs.

### 2.1. The Processing Pipeline
1.  **Reference Alignment (Registration):**
    * **Algorithm:** ORB (Oriented FAST and Rotated BRIEF).
    * **Mechanism:** Feature keypoints are extracted from both the "Golden Template" and the "Test Board." A Homography matrix is computed to warp the Test Board, aligning it pixel-perfectly with the reference template.
    * **Justification:** ORB provides rotational invariance and is computationally superior to SIFT for real-time applications.

2.  **Anomaly Extraction:**
    * **Technique:** Image Subtraction & Morphological Filtering.
    * **Mechanism:** `absdiff(Template, Test)` computes the pixel-wise difference. A series of morphological operations (Erosion/Dilation) removes environmental noise (e.g., dust, lighting glare) while preserving significant defect contours.

---

## 3. Data & Business Intelligence Architecture

### 3.1. Smart Costing & BER Logic
**Challenge:** Raw defect counts do not translate to manufacturing decisions.
**Solution:** Implemented a "Beyond Economic Repair" (BER) decision engine.
* **Cost Matrix:** Each defect type is assigned a repair cost (e.g., Mouse Bite = $11.25) and time penalty.
* **Scrap Logic:** Boards are flagged as `SCRAP` if:
    * Total Repair Cost > 75% of Board Value ($50.00).
    * Critical Defect (Missing Hole) is detected.
* **Impact:** Provides immediate "Go/No-Go" decisions for line operators.

### 3.2. Enterprise "Memory" (SQLite Backbone)
**Challenge:** Prototype scripts lose data upon restart.
**Solution:** Integrated a persistent **SQLite Database** (`pcb_production.db`).
* **Schema:** `inspections` table stores Timestamp, Filename, Defect Count, Health Score, QC Status, Cost, and Scrap Boolean.
* **Analytics:** A dedicated dashboard queries this database to visualize:
    * **Yield Rates:** (Pass vs. Fail/Scrap).
    * **Financial Loss:** Cumulative cost of scrapped boards.
    * **Defect Mix:** Pareto chart of most common defect types.
* **Impact:** Enables long-term trend analysis and auditability.

### 3.3. Batch Processing Engine
**Challenge:** Manual single-file uploads are inefficient for high-volume testing.
**Solution:** Developed a ZIP-based batch processor.
* **Mechanism:** Iterates through archives, running the full alignment/inference pipeline on each image in memory.
* **Output:** Generates a **Master CSV Report** aggregating status and costs for the entire batch.
* **Deep Dive:** Allows "Lazy Loading" of specific files from the batch for visual inspection without re-uploading.

---

## 4. Technical Innovations & Optimization

### 4.1. The "Heavy Head" Architecture
**Challenge:** The baseline EfficientNetB0 model exhibited high confusion rates between geometrically similar classes (e.g., *Spur* vs. *Spurious Copper*), plateauing at ~92% accuracy.

**Solution:** A custom classification head was engineered to increase model capacity.
* **Backbone:** EfficientNetB0 (ImageNet Weights, Frozen).
* **Custom Head:**
    * `GlobalAveragePooling2D`
    * `Dense(256, activation='relu')` **(Feature Projection Layer)**
    * `Dropout(0.3)` **(Regularization)**
    * `Dense(6, activation='softmax')`

**Impact:** The addition of the 256-unit dense layer introduced necessary non-linearity, allowing the model to learn complex decision boundaries. This architectural change directly contributed to the final **97.8% accuracy**.

### 4.2. "Dual-Box" Inference Strategy
**Challenge:** During inference, "Open Circuits" were frequently misclassified as "Shorts" due to aspect ratio distortion when tight bounding boxes were resized to the model's input size (128x128).

**Solution:** A decoupled inference logic was implemented:
* **Visualization Box:** Tight crop (`padding=5px`) for precise UI rendering.
* **Inference Box:** Fixed-context crop (`padding=20px`) for the Neural Network.

**Impact:** By guaranteeing sufficient context (surrounding copper tracks), the model could reliably distinguish between a break in a track (Open) and a bridge between tracks (Short), achieving **0 misclassifications** between these critical categories.

---

## 5. Performance Evaluation

### 5.1. Metrics
The model was evaluated on a held-out validation set derived from the DeepPCB dataset.

* **Final Validation Accuracy:** **97.80%**
* **Training Accuracy:** 99.1%
* **Loss Function:** Categorical Cross-Entropy
* **Optimizer:** Adam (`lr=0.001`) with `ReduceLROnPlateau` scheduling.

### 5.2. Critical Class Performance
| Defect Type | Precision | Recall | Significance |
| :--- | :--- | :--- | :--- |
| **Open Circuit** | 98.5% | **100%** | Critical (Electrical Failure) |
| **Short** | 99.0% | **100%** | Critical (Electrical Failure) |
| **Mouse Bite** | 97.2% | 96.5% | Structural Weakness |

---

## 6. Technology Stack
* **Language:** Python 3.11.9
* **Computer Vision:** OpenCV 4.8
* **Deep Learning:** TensorFlow/Keras 2.14
* **Database:** SQLite3
* **Web Interface:** Streamlit (with Custom CSS)
* **Reporting:** FPDF (PDF Generation)

---

## 7. Conclusion
The project successfully delivers an automated inspection tool that meets the internship requirements for accuracy and usability. By extending the core AI capabilities with **Database Persistence**, **Financial Logic**, and **Batch Processing**, the system mimics a complete industrial Quality Assurance solution. The integration of the "Dual-Box" strategy and the "Heavy Head" architecture ensures reliability, achieving a final defect detection accuracy of **97.8%**.