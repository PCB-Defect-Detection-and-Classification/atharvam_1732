# 📘 Milestone 3: Frontend & Backend Integration

**Phase:** Milestone 3
**Focus:** Application Development & System Integration
**🎯 Objective:** Build a production-ready Web UI for real-time PCB defect inspection.
**🛠️ Tech Stack:** Streamlit, OpenCV, TensorFlow, FPDF

---

## 📖 Milestone Overview

This final milestone integrates the **Computer Vision Detection Pipeline (Milestone 1)** and the **Deep Learning Classifier (Milestone 2)** into a unified, user-friendly Web Application.

The system allows Quality Assurance (QA) engineers to upload PCB images, automatically detect and classify defects, and generate industry-standard inspection reports.

---

## 📂 Folder Structure

```text
Milestone 3/
│
├── app.py                    # Main Frontend Application (Streamlit)
│
├── src/                      # Backend Logic
│   ├── backend.py            # Image Alignment, Subtraction & Inference Pipeline
│   ├── config.py             # Global Configuration & Paths
│
├── models/                   # Trained AI Models
│   └── pcb_defect_model.keras  # The 97.8% Accuracy Model
│
├── requirements.txt          # Project Dependencies
└── README.md                 # Documentation
````

-----

## 💻 Module 5: Web UI (Frontend)

We built a responsive dashboard using **Streamlit** that serves as the control center for the inspection process.

### ✨ Key Features

  * **Interactive Sidebar:** Allows users to adjust the **Confidence Threshold** in real-time to filter weak predictions.
  * **Dual-Image Upload:** Accepts both a "Golden Template" and a "Test Board" for comparative analysis.
  * **"X-Ray" Vision Mode:** A custom component (`streamlit-image-comparison`) that allows users to slide between the reference and test images to manually verify defects.
  * **Automated Reporting:** Generates and downloads a **PDF Inspection Certificate** containing visual proofs and defect logs.

-----

## ⚙️ Module 6: Backend Pipeline

The backend (`src/backend.py`) orchestrates the complex logic required to go from raw pixels to a diagnosis.

### 🚀 The "Dual-Box" Inference Strategy

To resolve common misclassifications (e.g., *Short* vs. *Open Circuit*), we implemented a novel two-step processing strategy:

1.  **Visualization Box (Tight Crop):**

      * **Purpose:** User Interface.
      * **Logic:** Tightly hugs the defect (padding +5px) to show the user exactly where the error is.
      * **Result:** Clean, precise red bounding boxes on the screen.

2.  **Context Box (Fixed Context):**

      * **Purpose:** AI Prediction.
      * **Logic:** Extracts a fixed 64x64 region (or larger) around the defect.
      * **Result:** Provides the Neural Network with enough "surrounding visual context" to distinguish a broken track (*Open*) from a bridged track (*Short*).

### 🛠️ Pipeline Steps

1.  **Image Loading:** Reads uploaded files into NumPy arrays.
2.  **Smart Alignment:** Uses **ORB Feature Matching** (2000 features) to perfectly align the Test Board with the Template, correcting for rotation and shift.
3.  **Difference Extraction:** Applies Gaussian Blur (3x3) and Adaptive Thresholding to find anomalies.
4.  **ROI Extraction:** Crops suspected regions using the "Context Box" strategy.
5.  **Classification:** Passes crops to the **EfficientNetB0** model to predict the defect type.
6.  **Report Generation:** Compiles all data into a structured PDF.

-----

## 🖼️ Application Showcase

### 1\. The Dashboard

*A clean interface for uploading boards and configuring inspection parameters.*

### 2\. Defect Detection Map

*Red bounding boxes automatically highlight all detected errors.*

### 3\. "X-Ray" Comparison Tool

*An interactive slider reveals the differences between the Reference and Test boards.*

### 4\. PDF Inspection Report

*An auto-generated document listing Board Health Score, Defect Counts, and providing Visual Proofs.*

-----

## 🚀 How to Run the App

### 1️⃣ Prerequisites

Ensure you have the trained model from Milestone 2 placed in the `models/` directory.

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Launch the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`.

-----

## ✅ Final Project Status

| Milestone | Objective | Status | Result |
| :--- | :--- | :--- | :--- |
| **M1** | Defect Detection | ✅ Complete | **100% Recall** (0 Missed Defects) |
| **M2** | Defect Classification | ✅ Complete | **97.80% Accuracy** (EfficientNetB0) |
| **M3** | System Integration | ✅ Complete | **Fully Functional Web App** |

-----

