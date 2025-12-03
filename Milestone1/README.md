
# PCB Defect Detection & Classification System (Milestone 1)

This repository contains the implementation for **Milestone 1** of the PCB Defect Detection internship project.  
It focuses on defect localization using **Computer Vision (OpenCV)** and data preparation for **Deep Learning**.

---

## Project Structure

```

src/          : Contains the modular logic for image processing and XML parsing.
dataset/      : (Ignored by Git) Place your PCB_DATASET folder here.
output/       : Generated deliverables (Visual proofs and Labeled ROIs).

````

---

## Modules Implemented

1. **Module 1 (Image Subtraction)**  
   Identifying defects by comparing Test images against Golden Templates.

2. **Module 2 (ROI Extraction)**  
   Parsing XML ground-truth data to crop and label defects for Model Training.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd PCB_Defect_Detection
````

### 2. Create Virtual Environment

It is recommended to use a virtual environment to keep dependencies isolated.

**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Dataset Placement

Download the DeepPCB dataset and place it in the root directory so the structure looks like this:

```
PCB_Defect_Detection/
└── dataset/
    └── PCB_DATASET/
        ├── images/
        ├── Annotations/
        └── PCB_USED/
```

### 5. Run the Pipeline

```bash
python main.py
```

---

## Outputs

After running the script, check the `output/` folder:

```
Visual_Report_Assets/    : Contains "Before/After" images for your PDF report.
Labeled_Training_Data/   : Contains cropped defect images sorted by category (Ready for Milestone 2).
```

---

