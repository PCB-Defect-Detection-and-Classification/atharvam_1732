import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from streamlit_image_comparison import image_comparison
from fpdf import FPDF
import datetime
import time
from src import backend

# --- PAGE CONFIG ---
st.set_page_config(page_title="PCB Defect Inspector", page_icon="🔬", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
    }
    .header-container {
        display: flex;
        align-items: center;
        justify-content: left; 
        gap: 20px;
        padding-bottom: 20px;
    }
    .header-icon {
        font-size: 4rem; 
    }
    .header-text h1 {
        margin: 0;
        padding: 0;
        line-height: 1.2;
    }
    .header-text p {
        margin: 0;
        color: #666;
        font-style: italic;
    }
    </style>
""", unsafe_allow_html=True)

# --- PDF GENERATION LOGIC ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'PCB Defect Inspection Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(annotated_img, defects, health_score):
    pdf = PDFReport()
    pdf.add_page()
    
    # 1. SUMMARY METRICS
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Inspection Summary', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    pdf.cell(50, 10, f'Health Score: {health_score}/100', 1)
    pdf.cell(50, 10, f'Defects Found: {len(defects)}', 1)
    pdf.cell(60, 10, f'Model: EfficientNetB0', 1)
    pdf.ln(15)

    # 2. VISUAL PROOF
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Visual Defect Map', 0, 1)
    
    # Save temp image for PDF embedding
    temp_img_path = "temp_report_img.jpg"
    Image.fromarray(annotated_img).save(temp_img_path)
    pdf.image(temp_img_path, x=10, w=190)
    pdf.ln(5)

    # 3. DEFECT TABLE
    if pdf.get_y() > 240: pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Detailed Defect Log', 0, 1)
    
    # Headers
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(60, 10, 'Defect Type', 1, 0, 'C', 1)
    pdf.cell(60, 10, 'Confidence Score', 1, 0, 'C', 1)
    pdf.cell(60, 10, 'Status', 1, 1, 'C', 1)
    
    # Rows
    pdf.set_font('Arial', '', 10)
    for d in defects:
        pdf.cell(60, 10, str(d['type']), 1, 0, 'C')
        pdf.cell(60, 10, f"{d['confidence']:.1f}%", 1, 0, 'C')
        pdf.cell(60, 10, 'Flagged', 1, 1, 'C')
        
    return pdf.output(dest='S').encode('latin-1')

# --- HEADER ---
st.markdown("""
    <div class="header-container">
        <div class="header-icon">🔬</div>
        <div class="header-text">
            <h1>Intelligent PCB Defect Inspection System</h1>
            <p>Automated Quality Assurance powered by EfficientNet & Computer Vision</p>
        </div>
    </div>
    <hr style="margin-top: 0;">
""", unsafe_allow_html=True)

# --- SIDEBAR ---
st.sidebar.header("⚙️ Configuration")
confidence_thresh = st.sidebar.slider("Confidence Threshold", 0, 100, 50, help="Filter out low-confidence predictions.")

st.sidebar.subheader("📂 Image Upload")
template_file = st.sidebar.file_uploader("1. Upload Golden Template", type=['jpg', 'png', 'jpeg'])
test_file = st.sidebar.file_uploader("2. Upload Test Board", type=['jpg', 'png', 'jpeg'])

# --- MAIN LOGIC ---
if template_file and test_file:
    t_img = Image.open(template_file).convert('RGB')
    test_img = Image.open(test_file).convert('RGB')
    
    t_arr = np.array(t_img)
    test_arr = np.array(test_img)
    
    with st.spinner("🧠 Loading AI Model..."):
        model = backend.load_defect_model()
    
    if st.sidebar.button("🚀 Run Inspection", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # --- PROCESSING ---
        status_text.text("aligning boards...")
        progress_bar.progress(25)
        
        status_text.text("extracting defect regions...")
        progress_bar.progress(50)
        
        start_time = time.time()
        aligned, annotated, defects = backend.run_inspection(t_arr, test_arr, model, confidence_thresh)
        end_time = time.time()
        
        status_text.text("classifying defects...")
        progress_bar.progress(75)
        time.sleep(0.5)
        
        progress_bar.progress(100)
        status_text.text("Done!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
        # --- DASHBOARD ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Defects", len(defects), delta_color="inverse")
        m2.metric("Processing Time", f"{(end_time - start_time):.2f}s")
        
        score = max(0, 100 - (len(defects) * 15))
        m3.metric("Board Health Score", f"{score}/100", delta_color="normal" if score > 80 else "off")
        
        st.divider()
        
        # --- TABS ---
        tab1, tab2, tab3 = st.tabs(["🔍 Defect Map", "👁️ X-Ray Comparison", "📄 Data Table"])
        
        with tab1:
            st.image(annotated, caption="AI Detected Defects", use_container_width=True)
            
        with tab2:
            st.markdown("Slide to compare the **Aligned Test Image** vs **Golden Template**.")
            image_comparison(
                img1=t_arr,
                img2=annotated,
                label1="Golden Template",
                label2="Test Board",
                starting_position=50,
                show_labels=True,
                make_responsive=True, 
                in_memory=True
            )
            
        with tab3:
            if defects:
                st.dataframe(defects, use_container_width=True)
            else:
                st.info("No defects found! Board is clean.")
        
        # --- EXPORT SECTION ---
        if defects:
            st.divider()
            st.subheader("📂 Export Results")
            
            pdf_bytes = generate_pdf(annotated, defects, score)
            col1, col2, col3 = st.columns(3)
            
            # 1. CSV
            df = pd.DataFrame(defects)
            col1.download_button("📥 Download Log (.csv)", df.to_csv(index=False).encode('utf-8'), "defect_log.csv", "text/csv")
            
            # 2. JPG
            img_bgr = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)
            _, img_buffer = cv2.imencode(".jpg", img_bgr)
            col2.download_button("🖼️ Download Image (.jpg)", img_buffer.tobytes(), "labeled_pcb.jpg", "image/jpeg")
            
            # 3. PDF
            col3.download_button("📄 Download Report (.pdf)", pdf_bytes, "PCB_Inspection_Report.pdf", "application/pdf")

        else:
            st.success("Board is compliant. No export required.")

else:
    st.info("👋 Please upload images in the sidebar to begin inspection.")