# PCB Defect Detection & Classification System

**Internship Project:** AI-Based PCB Defect Detection  
**Phase:** Milestone 1 - Image Processing & Dataset Preparation  
**Status:** ✅ Completed

---

## 📖 Project Overview

The objective of this project is to develop an automated system capable of identifying and classifying defects on Printed Circuit Boards (PCBs). In the electronics manufacturing industry, manual inspection is slow and prone to error. This solution leverages **Computer Vision** (for localization) and **Deep Learning** (for classification) to automate quality assurance.

This repository contains the deliverables for **Milestone 1**, which focuses on building the foundational image processing pipeline and preparing the data for the neural network.

---

## 🎯 Milestone 1 Objectives

The goal of this phase was to implement **Modules 1 & 2** from the project roadmap:

1. **Module 1 (Defect Localization):**  
   Implement a reference-based subtraction algorithm to detect anomalies between a "Golden Template" and a "Test Image."

2. **Module 2 (ROI Extraction):**  
   Prepare a clean, labeled dataset by extracting Ground Truth Regions of Interest (ROIs) from the DeepPCB dataset to train the CNN in Milestone 2.

---

## ⚙️ Methodology & Technical Approach

### 1. The Detection Pipeline (Module 1)

**File:** `src/processing.py`  

This module implements the core logic that identifies defects using **image subtraction**.  

**Algorithm Steps:**

1. **Image Alignment:** Resize the test image to match the template.  
2. **Image Subtraction:** Calculate pixel-wise absolute difference:  
   ```math
   Diff(x,y) = | Template(x,y) - Test(x,y) |
    ````

3. **Grayscale Conversion:** Simplifies processing.
4. **Otsu's Thresholding:** Automatically finds the optimal threshold to separate defects from noise.
5. **Morphological Filtering:**

   * **Opening:** Removes small white noise.
   * **Dilation:** Solidifies defect regions.
6. **Contour Extraction:** Draw bounding boxes around detected defects.

**Outcome:** Demonstrates that computer vision alone can localize defects like "Missing Holes" or "Spurs" without human intervention.

---

### 2. The Training Data Generator (Module 2)

**File:** `src/extraction.py`

This module generates **labeled ROIs** for training a CNN.

**Process:**

1. Parse XML annotation files from the DeepPCB dataset.
2. Extract verified bounding box coordinates (`xmin, ymin, xmax, ymax`).
3. Crop the corresponding regions from the raw images.
4. Automatically sort crops into class-specific folders (e.g., `Mouse_bite`, `Open_circuit`, `Short`).

**Outcome:** A dataset of **2,953 high-quality images** ready for CNN training.

---

## 📂 Repository Structure

```
PCB_Defect_Project/
├── dataset/                   # (Not tracked by Git) Contains DeepPCB dataset
├── output/                    # (Not tracked by Git) Generated Deliverables
│   ├── Visual_Report_Assets/  # "Before vs After" images proving Module 1 works
│   └── Labeled_Training_Data/ # Cropped defect images for Milestone 2 Training
├── src/                       # Source Code
│   ├── config.py              # Path configurations
│   ├── processing.py    # Subtraction & Thresholding Logic
│   └── extraction.py      # XML Parsing & Dataset Creation
├── main.py                    # Master execution script
├── requirements.txt           # Python dependencies
└── README.md                  # Project Documentation
```

---

## 💻 Setup & Usage

**Prerequisites:**

* Python 3.10 or higher
* DeepPCB Dataset (must include `images`, `PCB_USED`, and `Annotations`)

**Installation:**

```bash
git clone https://github.com/PCB-Defect-Detection-and-Classification/atharvam_1732/tree/main/Milestone1
cd Milestone1
python -m venv venv
source venv/bin/activate    # On Mac/Linux      
venv\Scripts\activate   # On Windows
pip install -r requirements.txt
```

**Execution:**

```bash
python main.py
```

---

## 📊 Results

### Output 1: Visual Verification (Module 1)

* The system identifies defects in testing.
* Generates **Difference Maps** and **Binary Masks** highlighting defects.
* See `output/Visual_Report_Assets/` for examples.

### Output 2: Labeled Dataset (Module 2)

* Processed **693 image pairs** from DeepPCB.
* Generated a balanced dataset:

| Defect Class    | Samples Extracted |
| --------------- | ----------------- |
| Missing Hole    | ~497              |
| Mouse Bite      | ~492              |
| Open Circuit    | ~482              |
| Short           | ~491              |
| Spur            | ~488              |
| Spurious Copper | ~503              |
| **Total**       | **~2,953**        |

---

## 🔜 Next Steps (Milestone 2)

* **Data Augmentation:** Increase dataset size via rotations and flips.
* **Model Architecture:** Implement a Convolutional Neural Network (CNN - ResNet).
* **Training:** Train the model to classify ROIs.
* **Evaluation:** Achieve target accuracy >95%.
