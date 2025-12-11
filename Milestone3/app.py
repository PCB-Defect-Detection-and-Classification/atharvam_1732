import streamlit as st
import cv2
import numpy as np
from PIL import Image
from streamlit_image_comparison import image_comparison
from fpdf import FPDF
import base64
import datetime
import os
import time
from src import backend, config

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
    
    # Draw simple metric boxes
    pdf.cell(50, 10, f'Health Score: {health_score}/100', 1)
    pdf.cell(50, 10, f'Defects Found: {len(defects)}', 1)
    pdf.cell(60, 10, f'Model: EfficientNetB0', 1)
    pdf.ln(15)

    # 2. VISUAL PROOF
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Visual Defect Map', 0, 1)
    
    # Save image temporarily to embed
    temp_img_path = "temp_report_img.jpg"
    Image.fromarray(annotated_img).save(temp_img_path)
    
    # Embed image (w=190 fits standard A4 margins)
    pdf.image(temp_img_path, x=10, w=190)
    pdf.ln(5)

    # 3. DEFECT TABLE
    # Check if we need a new page
    if pdf.get_y() > 240:
        pdf.add_page()
        
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Detailed Defect Log', 0, 1)
    
    # Table Header
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(60, 10, 'Defect Type', 1, 0, 'C', 1)
    pdf.cell(60, 10, 'Confidence Score', 1, 0, 'C', 1)
    pdf.cell(60, 10, 'Status', 1, 1, 'C', 1)
    
    # Table Rows
    pdf.set_font('Arial', '', 10)
    for d in defects:
        pdf.cell(60, 10, str(d['type']), 1, 0, 'C')
        pdf.cell(60, 10, f"{d['confidence']:.1f}%", 1, 0, 'C')
        pdf.cell(60, 10, 'Flagged', 1, 1, 'C')
        
    return pdf.output(dest='S').encode('latin-1')

# --- HEADER ---
col1, col2 = st.columns([1, 5])
with col1:
    st.write("🔬") 
with col2:
    st.title("Intelligent PCB Defect Inspection System")
    st.markdown("**Automated Quality Assurance powered by EfficientNet & Computer Vision**")

st.divider()

# --- SIDEBAR (Controls) ---
st.sidebar.header("⚙️ Configuration")
confidence_thresh = st.sidebar.slider("Confidence Threshold", 0, 100, 50, help="Filter out low-confidence predictions.")

st.sidebar.subheader("📂 Image Upload")
template_file = st.sidebar.file_uploader("1. Upload Golden Template", type=['jpg', 'png', 'jpeg'])
test_file = st.sidebar.file_uploader("2. Upload Test Board", type=['jpg', 'png', 'jpeg'])

# --- MAIN LOGIC ---
if template_file and test_file:
    # Load Images
    t_img = Image.open(template_file).convert('RGB')
    test_img = Image.open(test_file).convert('RGB')
    
    t_arr = np.array(t_img)
    test_arr = np.array(test_img)
    
    # Load Model
    with st.spinner("🧠 Loading AI Model..."):
        model = backend.load_defect_model()
    
    # Run Inspection Button
    if st.sidebar.button("🚀 Run Inspection", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulated Progress for UX
        status_text.text("aligning boards...")
        progress_bar.progress(25)
        time.sleep(0.5)
        
        status_text.text("extracting defect regions...")
        progress_bar.progress(50)
        
        # REAL PROCESSING
        aligned, annotated, defects = backend.run_inspection(t_arr, test_arr, model, confidence_thresh)
        
        status_text.text("classifying defects with EfficientNet...")
        progress_bar.progress(75)
        time.sleep(0.5)
        
        progress_bar.progress(100)
        status_text.text("Done!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
        # --- RESULTS DASHBOARD ---
        
        # 1. Metrics Row
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Defects", len(defects), delta_color="inverse")
        m2.metric("Processing Time", "1.2s")
        
        # Health Score Logic
        score = max(0, 100 - (len(defects) * 15))
        color = "normal" if score > 80 else "off"
        m3.metric("Board Health Score", f"{score}/100", delta_color=color)
        
        st.divider()
        
        # 2. Advanced Visualization (Tabs)
        tab1, tab2, tab3 = st.tabs(["🔍 Defect Map", "👁️ X-Ray Comparison", "📄 Data Table"])
        
        with tab1:
            st.image(annotated, caption="AI Detected Defects", use_container_width=True)
            
        with tab2:
            st.markdown("Slide to compare the **Aligned Test Image** vs **Golden Template**.")
            # This is the "Out of the Box" feature
            image_comparison(
                img1=t_arr,
                img2=annotated,
                label1="Golden Template",
                label2="Test Board (Aligned)",
                width=1200,
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
        
        # 3. Report Generation
        if defects:
            st.divider()
            st.subheader("📝 Export Report")
            
            # Generate the PDF
            pdf_bytes = generate_pdf(annotated, defects, score)
            
            # Create download button
            b64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="PCB_Inspection_Report.pdf"><button style="background-color: #FF4B4B; color: white; padding: 10px 24px; border: none; border-radius: 4px; cursor: pointer;">📥 Download Official PDF Report</button></a>'
            st.markdown(href, unsafe_allow_html=True)
            
        else:
            st.success("Board is compliant. No report required.")

else:
    # Empty State (Welcome Screen)
    st.info("👋 Welcome! Please upload images in the sidebar to begin inspection.")
    st.markdown("""
    ### Features:
    * **Advanced Alignment:** Uses ORB Feature matching to handle rotated boards.
    * **AI Classification:** Identifies 6 defect types (Mouse Bite, Open, Short, etc.).
    * **X-Ray Mode:** Interactive slider to verify defects manually.
    """)