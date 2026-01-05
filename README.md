# 🔬 AI-Based PCB Defect Detection & Classification System

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.14-orange?logo=tensorflow)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![SQLite](https://img.shields.io/badge/Database-SQLite3-green?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Completed-success)

> **Internship Capstone Project** | **Final Accuracy:** 97.80% | **Recall:** 100% on Critical Defects 

## 📽️ Project Presentation
<div align="center">

[![View Presentation](https://img.shields.io/badge/View-Presentation-0969da?style=for-the-badge)](https://pcb-defect-detection-and-classification.github.io/atharvam_1732/)

</div>


---

## 📖 Executive Summary
This project is an **Industrial-Grade Automated Optical Inspection (AOI)** system designed to identify, classify, and analyze manufacturing defects in Printed Circuit Boards (PCBs).

Going beyond simple detection, the system serves as a complete **Quality Assurance Platform**. It integrates **Computer Vision** for precision alignment, **Deep Learning** for classification, and **Business Intelligence** logic to calculate repair costs, determine scrap status, and track production yield over time via a persistent database.

---

## 🛠️ Tech Stack & Architecture

| Component | Technology Used | Purpose |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Interactive Dashboard & Reporting UI |
| **Backend** | OpenCV, Python | Image Alignment (ORB) & Defect Extraction |
| **AI Model** | TensorFlow, Keras | Defect Classification (EfficientNetB0) |
| **Database** | SQLite3 | Persistent Audit Logs & Analytics |
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
* **Focus:** Industrial Features & User Experience.
* **Key Achievement:** Finalized the QA Platform with **Database Analytics**, **Batch Processing**, **Smart Costing**, and **Automated PDF Reporting**.
* **Result:** A fully functional, deployed application ready for factory use.

---

## ✨ Advanced Capabilities (Final System Features - Beyond Requirements)

While the initial requirements focused on simple detection, the final system (Milestone 4) implements a full industrial workflow:

### 1. 🧠 Smart Alignment & Preprocessing
   - **Auto-Registration:** Uses **ORB Feature Matching & Homography** to automatically align, rotate, and warp the Test Board to match the Golden Template perfectly.
   - **Noise Filtering:** Morphological operations remove dust and lighting glare to prevent false positives.

### 2. 💰 Business Intelligence & BER Logic
   - **Smart Costing:** Automatically calculates estimated repair costs (e.g., *Mouse Bite = $11.25*) and repair time.
   - **Scrap Decision Engine:** Flags boards as **"SCRAP"** if repair costs exceed 75% of value or if critical defects (e.g., Missing Hole) are found.

### 3. 🏭 Automated Batch Processing
   - **Bulk Inspection:** Supports **ZIP file uploads** to process dozens of boards simultaneously.
   - **Lazy Loading:** "Deep Dive" mode allows technicians to visually inspect specific files from a large batch without re-uploading.

### 4. 🗄️ Enterprise "Memory" (Analytics)
   - **Persistent Database:** An integrated **SQLite** database stores every inspection log forever.
   - **Health Trend Analysis:** A dynamic line chart tracks the **Average Health Score** over the last 20 boards, helping identify drifting production quality.
   - **Yield & Cost Metrics:** Visualizes **Pass/Fail Rates**, **Financial Loss**, and **Defect Pareto Charts** in real-time.
   - **Audit Tools:** Includes filtering by date/status and database management tools.

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
* [📖 User Guide](./Milestone4/Documentation/User_Guide.md) - Manual for Operators and Managers.
* [🛠️ Technical Report](./Milestone4/Documentation/Technical_Report.md) - Deep dive into algorithms, architecture, and business logic.

---

**Author:** Atharva Mundke | **Date:** December 2025
