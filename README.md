# 🔬 AI-Based PCB Defect Detection & Classification System

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.14-orange?logo=tensorflow)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Status](https://img.shields.io/badge/Status-Completed-success)

> **Internship Capstone Project** | **Final Accuracy:** 97.80% | **Recall:** 100% on Critical Defects

---

## 📖 Executive Summary
This project is an automated optical inspection (AOI) system designed to identify and classify manufacturing defects in Printed Circuit Boards (PCBs). By integrating **Computer Vision (OpenCV)** for precise defect localization and **Deep Learning (EfficientNetB0)** for accurate classification, the system eliminates manual inspection errors.

The final product is a production-ready **Web Application** that allows Quality Assurance engineers to upload PCB images, visualize defects in real-time, and generate industry-standard PDF inspection reports.

---

## 🛠️ Tech Stack & Architecture

| Component | Technology Used | Purpose |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Interactive Dashboard & Reporting UI |
| **Backend** | OpenCV, Python | Image Alignment (ORB) & Defect Extraction |
| **AI Model** | TensorFlow, Keras | Defect Classification (EfficientNetB0) |
| **Reporting** | FPDF, Pandas | Auto-generating PDF Certificates & CSV Logs |

---

## 📂 Project Roadmap (Milestones)

This repository is organized into 4 distinct developmental phases:

### 🟢 **[Milestone 1: Defect Detection Logic](./Milestone1)**
* **Focus:** Computer Vision & Image Processing.
* **Key Achievement:** Built the "Image Subtraction Pipeline" using ORB Feature Matching to align template and test boards.
* **Result:** Successfully extracted defect regions (ROIs) from raw images.

### 🟡 **[Milestone 2: Model Training & Tuning](./Milestone2)**
* **Focus:** Deep Learning & Classification.
* **Key Achievement:** Trained a custom **EfficientNetB0** model.
* **Innovation:** Implemented a **"Heavy Head"** architecture (Dense 256 + ReLU) to solve non-linear defect boundaries.
* **Result:** Achieved **97.8% Validation Accuracy**.

### 🟠 **[Milestone 3: System Integration](./Milestone3)**
* **Focus:** Backend & Frontend Unification.
* **Key Achievement:** Solved the "Scale Distortion" issue using a **"Dual-Box" Inference Strategy** (Tight crop for UI vs. Context crop for AI).
* **Result:** Eliminated false positives between "Shorts" and "Open Circuits."

### 🔴 **[Milestone 4: Final Product & Deployment](./Milestone4)**
* **Focus:** User Experience & Documentation.
* **Key Achievement:** Finalized the Web App with **"X-Ray" Comparison**, **PDF Reporting**, and **CSV Export** features.
* **Result:** A fully functional, deployed application.

---

## 📊 Key Performance Metrics

The system detects **6 Defect Types** with high precision:

| Defect Type | Recall (Sensitivity) | Significance |
| :--- | :--- | :--- |
| **Open Circuit** | **100%** | 🔴 Critical (Electrical Failure) |
| **Short** | **100%** | 🔴 Critical (Electrical Failure) |
| **Mouse Bite** | 96.5% | 🟡 Structural Weakness |
| **Spur** | 98.2% | 🟢 Minor Defect |
| **Missing Hole** | 100% | 🔴 Critical (Assembly Failure) |
| **Spurious Copper** | 95.8% | 🟢 Minor Defect |

---

## 🚀 How to Run the Final App

To run the complete system (Milestone 4 version):

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/your-username/PCB-Defect-Detection.git](https://github.com/your-username/PCB-Defect-Detection.git)
    cd PCB-Defect-Detection
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r Milestone4/Final_App/requirements.txt
    ```

3.  **Launch the Dashboard**
    ```bash
    cd Milestone4/Final_App
    streamlit run app.py
    ```

---

## 📚 Documentation
For detailed technical breakdowns, please refer to the specific documentation in Milestone 4:
* [📖 User Guide](./Milestone4/Documentation/User_Guide.md) - How to use the software.
* [🛠️ Technical Report](./Milestone4/Documentation/Technical_Report.md) - Deep dive into algorithms and architecture.

---

**Author:** Atharva Mundke |
**Date:** December 2025