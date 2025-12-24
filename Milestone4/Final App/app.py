import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
from streamlit_image_comparison import image_comparison
from fpdf import FPDF
import datetime
import time
import zipfile
import io
from src import backend
from src import database # <--- NEW IMPORT

# --- PAGE CONFIG ---
st.set_page_config(page_title="PCB Defect Inspector", page_icon="🔬", layout="wide")

# --- INITIALIZE DATABASE ---
# This runs once to ensure the DB file exists
database.init_db()

# --- CONSTANTS ---
BOARD_VALUE = 50.00
BER_THRESHOLD = 0.75

# --- SESSION STATE (UI Logic only, Data moved to DB) ---
if 'single_results' not in st.session_state: st.session_state.single_results = None
if 'batch_results' not in st.session_state: st.session_state.batch_results = None
if 'batch_files' not in st.session_state: st.session_state.batch_files = []

# --- SHARED LOGIC ---
def get_repair_details(defect_type):
    details = {
        'Mouse Bite':      {'cost': 11.25, 'time': 15, 'action': 'Epoxy fill & bridge'},
        'Open Circuit':    {'cost': 7.50,  'time': 10, 'action': 'Solder jumper wire'},
        'Short':           {'cost': 1.50,  'time': 2,  'action': 'Scrape excess copper'},
        'Spur':            {'cost': 0.75,  'time': 1,  'action': 'Scrape excess copper'},
        'Spurious Copper': {'cost': 0.75,  'time': 1,  'action': 'Clean/Scrape'},
        'Missing Hole':    {'cost': 0.00,  'time': 0,  'action': 'SCRAP BOARD - DO NOT REPAIR'} 
    }
    return details.get(defect_type, {'cost': 0, 'time': 0, 'action': 'Inspect'})

def calculate_impact(defects):
    temp_cost = sum([get_repair_details(d['type'])['cost'] for d in defects])
    is_scrap = False
    scrap_reason = ""
    
    if any(d['type'] == 'Missing Hole' for d in defects):
        is_scrap, scrap_reason = True, "CRITICAL DEFECT (Missing Hole)"
    elif temp_cost > (BOARD_VALUE * BER_THRESHOLD):
        is_scrap, scrap_reason = True, f"ECONOMIC FAILURE (Repair ${temp_cost:.2f} > 75% Value)"
        
    total_repair_cost = BOARD_VALUE if is_scrap else temp_cost
    total_repair_time = 0 if is_scrap else sum([get_repair_details(d['type'])['time'] for d in defects])
    score = max(0, 100 - (len(defects) * 15))
    
    return score, total_repair_cost, total_repair_time, is_scrap, scrap_reason

# --- PDF GENERATOR ---
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'PCB Defect Inspection Report', 0, 1, 'C')
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_pdf(annotated_img, defects, health_score, total_cost, is_scrap):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Inspection Summary', 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(50, 10, f'Health Score: {health_score}/100', 1)
    pdf.cell(50, 10, f'Defects: {len(defects)}', 1)
    cost_text = "Action: SCRAP ($50.00)" if is_scrap else f'Est. Cost: ${total_cost:.2f}'
    pdf.cell(60, 10, cost_text, 1)
    pdf.ln(15)
    
    temp_img_path = "temp_report_img.jpg"
    Image.fromarray(annotated_img).save(temp_img_path)
    pdf.image(temp_img_path, x=10, w=190)
    pdf.ln(5)
    
    if pdf.get_y() > 220: pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Technician Work Order', 0, 1)
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(40, 10, 'Defect', 1, 0, 'C', 1)
    pdf.cell(80, 10, 'Action', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Time', 1, 0, 'C', 1)
    pdf.cell(40, 10, 'Cost ($)', 1, 1, 'C', 1)
    pdf.set_font('Arial', '', 10)
    for d in defects:
        info = get_repair_details(d['type'])
        cost = 50.00 if d['type'] == 'Missing Hole' else info['cost']
        pdf.cell(40, 10, str(d['type']), 1, 0, 'C')
        pdf.cell(80, 10, str(info['action']), 1, 0, 'C')
        pdf.cell(30, 10, f"{info['time']} min", 1, 0, 'C')
        pdf.cell(40, 10, f"${cost:.2f}", 1, 1, 'C')
    return pdf.output(dest='S').encode('latin-1')

# --- UI RENDERER ---
def render_dashboard(t_arr, annotated, defects, score, cost, time, is_scrap, reason, key_suffix=""):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Defects Found", len(defects), delta_color="inverse")
    color = "normal" if score > 80 else "off"
    c2.metric("Health Score", f"{score}/100", delta_color=color)
    
    if is_scrap:
        c3.metric("Action Required", "SCRAP BOARD", delta_color="off")
        c4.metric("Loss Amount", f"${BOARD_VALUE:.2f}", delta="-$$$")
        st.error(f"⚠️ {reason}")
    else:
        c3.metric("Est. Repair Time", f"{time} mins")
        c4.metric("Est. Repair Cost", f"${cost:.2f}", delta="-$$$")

    st.divider()

    tab1, tab2, tab3 = st.tabs(["🔍 Defect Map", "📋 Technician Work Order", "📄 Raw Data"])
    
    with tab1:
        st.image(annotated, caption="Defect Localization", width="stretch")
    
    with tab2:
        if defects:
            wo_df = pd.DataFrame(defects)[['type', 'confidence', 'action', 'time', 'cost']]
            st.dataframe(wo_df, width="stretch")
        else:
            st.success("✅ No repairs needed.")

    with tab3:
        st.json(defects)

    st.divider()
    st.subheader("👁️ X-Ray Verification")
    image_comparison(
        img1=t_arr, img2=annotated, label1="Golden Template", label2="Test Board",
        width=1200, make_responsive=True, in_memory=True
    )
    
    if defects:
        st.divider()
        st.subheader("📂 Export Data")
        pdf_bytes = generate_pdf(annotated, defects, score, cost, is_scrap)
        
        b1, b2, b3 = st.columns(3)
        b1.download_button(f"📥 Work Order (.csv) {key_suffix}", pd.DataFrame(defects).to_csv().encode('utf-8'), f"work_order{key_suffix}.csv", "text/csv")
        
        img_bgr = cv2.cvtColor(annotated, cv2.COLOR_RGB2BGR)
        _, buf = cv2.imencode(".jpg", img_bgr)
        b2.download_button(f"🖼️ Evidence Photo (.jpg) {key_suffix}", buf.tobytes(), f"evidence{key_suffix}.jpg", "image/jpeg")
        
        b3.download_button(f"📄 Official Report (.pdf) {key_suffix}", pdf_bytes, f"report{key_suffix}.pdf", "application/pdf")


# --- APP LAYOUT ---
st.markdown("""
    <style>
    .header-container { display: flex; align-items: center; gap: 20px; padding-bottom: 20px; }
    .header-icon { font-size: 4rem; }
    .header-text h1 { margin: 0; line-height: 1.2; }
    </style>
    <div class="header-container">
        <div class="header-icon">🔬</div>
        <div class="header-text">
            <h1>Intelligent PCB Defect Inspection System</h1>
            <p>Automated Quality Assurance • Production Analytics • Smart Costing</p>
        </div>
    </div>
    <hr style="margin-top: 0;">
""", unsafe_allow_html=True)

st.sidebar.header("⚙️ Configuration")
app_mode = st.sidebar.radio("Select Mode", ["Single Board Inspection", "Batch Processing (ZIP)", "View Historical Logs"])
confidence_thresh = st.sidebar.slider("Confidence Threshold", 0, 100, 81)

st.sidebar.divider()

# --- LIVE STATS (LOADED FROM DB) ---
st.sidebar.subheader("📈 Live Production Stats")
# FETCH FROM DB
db_total, db_avg, db_history = database.get_production_stats()

if db_total > 0:
    st.sidebar.metric("Boards Scanned", db_total)
    st.sidebar.metric("Avg Health Score", f"{db_avg:.1f}")
    st.sidebar.markdown("**Health Trend (Last 20)**")
    st.sidebar.line_chart(db_history)
else:
    st.sidebar.info("Start scanning to see production trends.")

st.sidebar.subheader("📂 Image Upload")
template_file = st.sidebar.file_uploader("1. Golden Template", type=['jpg', 'png', 'jpeg'])

# ==========================================
# MODE 1: SINGLE BOARD INSPECTION
# ==========================================
if app_mode == "Single Board Inspection":
    test_file = st.sidebar.file_uploader("2. Test Board", type=['jpg', 'png', 'jpeg'])
    
    if template_file and test_file and st.sidebar.button("🚀 Run Inspection", type="primary"):
        t_arr = np.array(Image.open(template_file).convert('RGB'))
        test_arr = np.array(Image.open(test_file).convert('RGB'))
        
        with st.spinner("Processing..."):
            model = backend.load_defect_model()
            _, annotated, defects = backend.run_inspection(t_arr, test_arr, model, confidence_thresh)
            
            score, cost, time_r, is_scrap, reason = calculate_impact(defects)
            for d in defects: d.update(get_repair_details(d['type']))
            
            # --- DATABASE LOGGING ---
            status = "SCRAP" if is_scrap else ("FAIL" if defects else "PASS")
            database.log_inspection(test_file.name, len(defects), score, status, cost, is_scrap)
            # ----------------------

            st.session_state.single_results = {
                't_arr': t_arr, 'annotated': annotated, 'defects': defects,
                'score': score, 'cost': cost, 'time': time_r, 
                'is_scrap': is_scrap, 'reason': reason
            }
            st.rerun() # Refresh to update sidebar stats immediately
            
    if st.session_state.single_results:
        res = st.session_state.single_results
        render_dashboard(res['t_arr'], res['annotated'], res['defects'], 
                         res['score'], res['cost'], res['time'], 
                         res['is_scrap'], res['reason'], key_suffix="_single")
    elif not test_file:
        st.info("👋 Upload images to begin.")

# ==========================================
# MODE 2: BATCH PROCESSING (ZIP)
# ==========================================
elif app_mode == "Batch Processing (ZIP)":
    zip_file = st.sidebar.file_uploader("2. Test Boards Archive (ZIP)", type="zip")
    
    if template_file and zip_file and st.sidebar.button("🚀 Run Batch Inspection", type="primary"):
        t_arr = np.array(Image.open(template_file).convert('RGB'))
        model = backend.load_defect_model()
        results_list = []
        
        with st.spinner("Processing Batch..."):
            with zipfile.ZipFile(zip_file, "r") as z:
                valid_files = [f for f in z.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                st.session_state.batch_files = valid_files
                
                prog = st.progress(0)
                for idx, filename in enumerate(valid_files):
                    prog.progress(int((idx+1)/len(valid_files)*100))
                    
                    test_arr = np.array(Image.open(io.BytesIO(z.read(filename))).convert('RGB'))
                    _, _, defects = backend.run_inspection(t_arr, test_arr, model, confidence_thresh)
                    score, cost, _, is_scrap, reason = calculate_impact(defects)
                    
                    # Breakdown
                    counts = {}
                    for d in defects: counts[d['type']] = counts.get(d['type'], 0) + 1
                    breakdown = ", ".join([f"{k}({v})" for k,v in counts.items()]) if defects else "-"
                    status = "SCRAP" if is_scrap else ("FAIL" if defects else "PASS")
                    
                    # --- DATABASE LOGGING ---
                    database.log_inspection(filename, len(defects), score, status, cost, is_scrap)
                    # ----------------------

                    results_list.append({
                        "Filename": filename,
                        "Status": status,
                        "Score": score,
                        "Est. Loss ($)": cost,
                        "Breakdown": breakdown
                    })
                    
        st.session_state.batch_results = pd.DataFrame(results_list)
        st.rerun() # Refresh to update sidebar stats immediately

    if st.session_state.batch_results is not None:
        df = st.session_state.batch_results
        
        st.divider()
        st.subheader("📊 Batch Summary Report")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Boards", len(df))
        passed = len(df[df['Status'] == 'PASS'])
        m2.metric("Yield Rate", f"{(passed / len(df)) * 100:.1f}%")
        m3.metric("Total Financial Impact", f"${df['Est. Loss ($)'].sum():.2f}", delta="-$$$")
        
        st.dataframe(df, width="stretch")
        st.download_button("📥 Download Master Report", df.to_csv(index=False).encode('utf-8'), "batch_master.csv", "text/csv")
        
        st.divider()
        st.subheader("🔍 Deep Dive Inspection")
        selected_file = st.selectbox("Select Board to Inspect:", st.session_state.batch_files)
        
        if selected_file and template_file and zip_file:
            with zipfile.ZipFile(zip_file, "r") as z:
                t_arr = np.array(Image.open(template_file).convert('RGB'))
                test_arr = np.array(Image.open(io.BytesIO(z.read(selected_file))).convert('RGB'))
                
                model = backend.load_defect_model()
                _, annotated, defects = backend.run_inspection(t_arr, test_arr, model, confidence_thresh)
                
                score, cost, time_r, is_scrap, reason = calculate_impact(defects)
                for d in defects: d.update(get_repair_details(d['type']))
                
                render_dashboard(t_arr, annotated, defects, score, cost, time_r, 
                                 is_scrap, reason, key_suffix="_batch_deep_dive")

# ==========================================
# MODE 3: HISTORICAL LOGS (Advanced)
# ==========================================
elif app_mode == "View Historical Logs":
    st.title("🏭 Production Analytics Dashboard")
    
    # 1. FETCH DATA
    full_df = database.get_full_history()
    
    if not full_df.empty:
        full_df['timestamp'] = pd.to_datetime(full_df['timestamp'])
        
        # --- NEW: SIDEBAR FILTERS ---
        st.sidebar.divider()
        st.sidebar.subheader("🔍 Filter Logs")
        
        # Filter by Status
        status_filter = st.sidebar.multiselect(
            "Filter by Status", 
            options=["PASS", "FAIL", "SCRAP"],
            default=["PASS", "FAIL", "SCRAP"]
        )
        
        # Filter by Date
        min_date = full_df['timestamp'].min().date()
        max_date = full_df['timestamp'].max().date()
        
        # Handle case where database has only 1 day of data
        if min_date == max_date:
            date_filter = (min_date, max_date)
            st.sidebar.info(f"Data available for: {min_date}")
        else:
            date_filter = st.sidebar.date_input(
                "Filter by Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
        
        # --- APPLY FILTERS ---
        # 1. Status Filter
        filtered_df = full_df[full_df['status'].isin(status_filter)]
        
        # 2. Date Filter
        if isinstance(date_filter, tuple) and len(date_filter) == 2:
            start_date, end_date = date_filter
            # Convert date objects to timestamp for comparison
            filtered_df = filtered_df[
                (filtered_df['timestamp'].dt.date >= start_date) & 
                (filtered_df['timestamp'].dt.date <= end_date)
            ]
        
        # --- DISPLAY KPIs (Based on FILTERED Data) ---
        st.divider()
        k1, k2, k3, k4 = st.columns(4)
        
        total_scans = len(filtered_df)
        total_scraps = len(filtered_df[filtered_df['status'] == 'SCRAP'])
        
        if total_scans > 0:
            yield_rate = ((total_scans - total_scraps) / total_scans) * 100
        else:
            yield_rate = 0.0
            
        total_loss = filtered_df['cost'].sum()
        
        k1.metric("Visible Records", total_scans)
        k2.metric("Yield Rate (Selection)", f"{yield_rate:.1f}%")
        k3.metric("Scrapped (Selection)", total_scraps, delta_color="inverse")
        k4.metric("Financial Loss", f"${total_loss:,.2f}", delta="-$$$")
        
        st.divider()
        
        # --- CHARTS ---
        if not filtered_df.empty:
            c1, c2 = st.columns([2, 1])
            with c1:
                st.subheader("📊 Timeline")
                timeline = filtered_df.set_index('timestamp').resample('H')['filename'].count()
                st.bar_chart(timeline)
            with c2:
                st.subheader("🍩 Defect Mix")
                status_counts = filtered_df['status'].value_counts()
                st.dataframe(status_counts, use_container_width=True)
        
        # --- DATA TABLE ---
        st.subheader("📋 Detailed Audit Log")
        st.dataframe(
            filtered_df,
            column_config={
                "timestamp": st.column_config.DatetimeColumn("Scan Time", format="D MMM YYYY, h:mm a"),
                "filename": "Board File",
                "defects_count": st.column_config.NumberColumn("Defects", format="%d 🔴"),
                "health_score": st.column_config.ProgressColumn("Health Score", format="%f", min_value=0, max_value=100),
                "status": st.column_config.TextColumn("QC Status"),
                "cost": st.column_config.NumberColumn("Repair Cost", format="$%.2f"),
                "is_scrap": st.column_config.CheckboxColumn("Scrapped?"),
                "id": None
            },
            hide_index=True,
            width="stretch"
        )
        
        # --- DATA MANAGEMENT ---
        st.divider()
        c_dl, c_del = st.columns([1, 4])
        
        with c_dl:
            st.download_button(
                "📥 Export Selection (.csv)", 
                filtered_df.to_csv(index=False).encode('utf-8'), 
                f"log_export.csv", "text/csv"
            )
            
        with c_del:
            # DANGER ZONE: Reset Database
            if st.button("🗑️ RESET DATABASE (Clear All History)", type="primary"):
                import os
                try:
                    # Close connection logic handled inside src/database.py usually, 
                    # but easiest way is to delete the file or truncate table.
                    # We will add a truncate function to database.py next.
                    database.clear_all_data() 
                    st.success("Database cleared! Please refresh the page.")
                    time.sleep(1)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error clearing DB: {e}")
        
    else:
        st.info("📭 Database is empty. Go run some inspections in Single or Batch mode!")