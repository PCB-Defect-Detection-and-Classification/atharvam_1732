# 📖 PCB Defect Inspection System — User Guide

## 1. Getting Started

This application allows Quality Assurance (QA) teams to automatically inspect **Printed Circuit Boards (PCBs)** for **six types of defects** using AI-based image analysis.

### Prerequisites

Before starting, make sure you have:

- 🟢 **Golden Template Image**  
  A defect-free reference image of the PCB.

- 🔍 **Test Board Image**  
  The PCB image you want to inspect.

---

## 2. Using the Dashboard

### Step 1: Upload Images

1. Locate the **📂 Image Upload** section in the left sidebar.
2. Upload:
   - **Template Image**
   - **Test Image**
3. Supported formats:
   - `.jpg`
   - `.png`

---

### Step 2: Configure Settings

- Adjust the **Confidence Threshold** slider to control defect detection sensitivity.

**Recommended Settings:**
- **50%** — General-purpose inspection  
- **80%** — Only highlight very obvious defects

Higher values reduce false positives but may miss subtle defects.

---

### Step 3: Run Inspection

1. Click the red **🚀 Run Inspection** button.
2. The system will:
   - Align the template and test images
   - Detect defects
   - Classify defects using the AI model

---

## 3. Interpreting Results

### 🩺 Health Score

- **100 / 100** — Perfect board (no defects)
- **Below 80 / 100** — Significant defects detected

---

### 📊 Visualization Tabs

#### 🔍 Defect Map
- Displays the **Test Board image**
- Red bounding boxes indicate detected defects

#### 👁️ X-Ray Comparison
- Drag the slider to peel back the Test Image
- Reveals the Golden Template underneath
- Useful for verifying whether a detection is due to misalignment

#### 📄 Data Table
- Lists all detected defects
- Includes:
  - Coordinates
  - Defect type
  - Confidence score

---

## 4. Exporting Data

After inspection is complete, scroll to the **📂 Export Results** section.

Available downloads:

- 📥 **Download Log (.csv)**  
  Raw detection data for Excel or database integration

- 🖼️ **Download Image (.jpg)**  
  Annotated image with bounding boxes for documentation

- 📄 **Download Report (.pdf)**  
  Official inspection certificate suitable for audits and records

---

✅ *End of User Guide*
