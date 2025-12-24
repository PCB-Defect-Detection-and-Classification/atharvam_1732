# 📖 PCB Defect Inspection System — User Guide

## 1. Getting Started

This application is an **Industrial-Grade Quality Assurance (QA) Platform**. It uses AI to inspect Printed Circuit Boards (PCBs), calculate repair costs, and manage production data over time.

### Prerequisites

Before starting, ensure you have:

- 🟢 **Golden Template Image** A defect-free reference image of the PCB.

- 🔍 **Test Board Image(s)** The PCB image(s) you want to inspect. Supports `.jpg`, `.png`, `.jpeg`.

- 📦 **ZIP Archive (Optional)** For batch processing, you can zip multiple board images into a single `.zip` file.

---

## 2. Select Your Mode

The application supports three distinct workflows via the **Sidebar Menu**:

1.  **Single Board Inspection**: Detailed analysis of one board.
2.  **Batch Processing (ZIP)**: Automated bulk inspection of multiple boards.
3.  **View Historical Logs**: Database analytics and audit trails.

---

## 3. Mode A: Single Board Inspection

### Step 1: Upload Images
1.  Go to **Sidebar > 📂 Image Upload**.
2.  Upload **1. Golden Template**.
3.  Upload **2. Test Board**.

### Step 2: Run & Analyze
1.  Adjust **Confidence Threshold** (Default: 50%).
2.  Click **🚀 Run Inspection**.
3.  The system will automatically **Align** the board (fix rotation/shifting) and detect defects.

### Step 3: Interpret Results
* **Health Score**: 0-100 Quality rating.
* **Financial Impact**:
    * **Est. Repair Cost**: Dollar amount to fix the board (e.g., $11.25).
    * **Action Required**:
        * **PASS**: No defects.
        * **REPAIR**: Defects found, cost is reasonable.
        * **SCRAP**: Cost is >75% of board value OR critical defect found.
* **Technician Work Order**: A tab listing specific repair actions (e.g., *"Epoxy fill & bridge"* for Mouse Bites).

---

## 4. Mode B: Batch Processing (ZIP)

Ideal for high-volume testing without manual uploads.

### Step 1: Prepare & Upload
1.  Select **"Batch Processing (ZIP)"** in the sidebar.
2.  Upload your **Golden Template**.
3.  Upload a **.zip file** containing multiple PCB images.

### Step 2: Automated Analysis
1.  Click **🚀 Run Batch Inspection**.
2.  The system processes all files in memory.
3.  **Batch Summary Report**: A master table appears showing:
    * Filename
    * Status (PASS/FAIL/SCRAP)
    * Yield Rate (%)
    * Total Financial Loss ($)

### Step 3: Deep Dive
Use the **"Select Board to Inspect"** dropdown at the bottom to view the visual defect map for any specific file in the batch without re-uploading it.

---

## 5. Mode C: Historical Logs & Analytics

A persistent database stores every inspection you perform.

### 📊 The Dashboard
* **KPI Cards**: View Total Boards Scanned, Yield Rate, and Total Financial Loss.
* **Timeline Chart**: See inspection activity over time.
* **Defect Mix**: A breakdown of the most common defect types.

### 🔍 Filters & Management
* **Filter by Status**: Use the sidebar to show only "FAIL" or "SCRAP" records.
* **Filter by Date**: Select a specific date range to audit.
* **Export Database**: Download the entire audit log as a `.csv` file.
* **Reset Database**: Use the **"🗑️ RESET DATABASE"** button to wipe all history and start fresh (Caution: Irreversible).

---

## 6. Exporting Reports

For any inspection (Single or Batch), you can download professional documentation from the **📂 Export Data** section:

- 📥 **Work Order (.csv)** Raw data including defect coordinates and repair costs.

- 🖼️ **Evidence Photo (.jpg)** High-resolution image with bounding boxes burnt in.

- 📄 **Official Report (.pdf)** A formal certificate including the Health Score, Cost Breakdown, and Technician Instructions.

---

✅ *End of User Guide*