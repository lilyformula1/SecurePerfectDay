import streamlit as st
import sys
import os
import tempfile
import re
import html
from datetime import datetime

sys.path.append(os.path.dirname(__file__))
from cyberguard import analyze

st.set_page_config(page_title="CyberBoom - Perfect Day Report", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# ============================================================
# CYBER SECURITY DARK THEME
# ============================================================
st.markdown("""
<style>
    .stApp { background-color: #070B12; }
    h1, h2, h3, h4, h5, h6 { color: #00E5FF !important; font-family: 'Segoe UI', sans-serif; }
    p, label, div, span { color: #E8F1F7 !important; }
    section[data-testid="stSidebar"] { background-color: #0A121F; border-right: 1px solid #1E3445; }
    .stButton > button { background-color: #101C2B; color: #00E5FF; font-weight: bold; border: 1px solid #1E3445; border-radius: 6px; transition: all 0.3s ease; }
    .stButton > button:hover { background-color: #00E5FF; color: #070B12; border: 1px solid #00E5FF; }
    .stButton > button[kind="primary"] { background-color: #00E5FF; color: #070B12; border: 1px solid #00E5FF; }
    .stButton > button[kind="primary"]:hover { background-color: #00FF9C; border: 1px solid #00FF9C; color: #070B12; }
    .stFileUploader { background-color: #101C2B; border: 1px solid #1E3445; border-radius: 8px; padding: 10px; }
    .stTextArea textarea { background-color: #0E1724 !important; color: #E8F1F7 !important; border: 1px solid #1E3445 !important; font-family: 'Courier New', monospace; font-size: 14px; }
    .stDownloadButton > button { background-color: #142433; color: #00FF9C; border: 1px solid #00FF9C; font-weight: bold; border-radius: 6px; padding: 10px; transition: all 0.3s ease; }
    .stDownloadButton > button:hover { background-color: #00FF9C; color: #070B12; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 🛡️ CYBERBOOM")
    st.caption("Perfect Day Security Suite")
    st.markdown("---")
    st.markdown("""
    **Why is this your Perfect Day?**
    
    Because you just made sure your system is safe from hackers! 
    
    Upload a file, scan it, and get your Security Clearance Report.
    """)
    st.markdown("---")
    st.caption(f"Session: {datetime.now().strftime('%Y-%m-%d')}")

# ============================================================
# MAIN CONTENT
# ============================================================
st.title("🛡️ Your Perfect Day Starts Here")
st.caption("Get your personal Security Clearance Report. Upload a file and let CyberBoom keep your day safe!")

uploaded_file = st.file_uploader("Upload a Windows executable for analysis", type=['exe', 'dll', 'sys'])

if uploaded_file is not None:
    st.success(f"Sample Loaded: {uploaded_file.name} ({(uploaded_file.size / 1024):.2f} KB)")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        temp_path = tmp_file.name

    # Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        run_pe = st.button("🧬 PE Analysis", use_container_width=True)
    with col2:
        run_api = st.button("⚠ API Detection", use_container_width=True)
    with col3:
        run_strings = st.button("🔤 String Scanner", use_container_width=True)
        
    col4, col5, col6 = st.columns(3)
    with col4:
        run_entropy = st.button("📊 Entropy", use_container_width=True)
    with col5:
        run_hash = st.button("🔐 Hash Analysis", use_container_width=True)
    with col6:
        run_risk = st.button("⚡ Risk Engine", use_container_width=True)
        
    run_full = st.button("⚡ RUN FULL ANALYSIS", type="primary", use_container_width=True)

    requested_mode = None
    if run_pe:
        requested_mode = "pe"
    elif run_api:
        requested_mode = "api"
    elif run_strings:
        requested_mode = "strings"
    elif run_entropy:
        requested_mode = "entropy"
    elif run_hash:
        requested_mode = "hash"
    elif run_risk:
        requested_mode = "risk"
    elif run_full:
        requested_mode = "full"
        
    if requested_mode:
        with st.spinner('Analyzing sample...'):
            try:
                # Core Analysis
                full_output = analyze(temp_path, "full")
                
                # Section Extraction Logic
                if requested_mode == "full":
                    output = full_output
                else:
                    output = ""
                    capture = False
                    for line in full_output.splitlines():
                        if "HASH ANALYSIS" in line or "STRING ANALYSIS" in line or "PE ANALYSIS" in line or "API DETECTION" in line or "ENTROPY ANALYSIS" in line or "RISK ASSESSMENT" in line:
                            if ("HASH ANALYSIS" in line and requested_mode == "hash") or \
                               ("STRING ANALYSIS" in line and requested_mode == "strings") or \
                               ("PE ANALYSIS" in line and requested_mode == "pe") or \
                               ("API DETECTION" in line and requested_mode == "api") or \
                               ("ENTROPY ANALYSIS" in line and requested_mode == "entropy") or \
                               ("RISK ASSESSMENT" in line and requested_mode == "risk"):
                                capture = True
                            else:
                                capture = False
                        if capture:
                            output += line + "\n"

                if not output.strip():
                    output = full_output

                # Risk Metrics
                risk_match = re.search(r"Risk Score\s*:\s*(\d+)", full_output)
                level_match = re.search(r"Risk Level\s*:\s*(HIGH|MEDIUM|LOW)", full_output)
                
                score = int(risk_match.group(1)) if risk_match else 0
                level = level_match.group(1) if level_match else "N/A"

                # Dynamic Risk Status
                if level == "HIGH":
                    status_color = "#FF3B6B"
                    status_text = "⚠️ HIGH RISK DETECTED"
                elif level == "MEDIUM":
                    status_color = "#FFD166"
                    status_text = "⚠️ MEDIUM RISK DETECTED"
                else:
                    status_color = "#00FF9C"
                    status_text = "✅ LOW RISK - PERFECT DAY!"

                # Interactive Dashboard
                st.markdown(f"""
                <div style="background-color: #101C2B; border: 1px solid {status_color}; border-radius: 10px; padding: 20px; margin-bottom: 20px;">
                    <h3 style="color: {status_color}; margin-bottom: 10px;">{status_text}</h3>
                    <p><strong>Risk Score:</strong> {score}/100</p>
                    <p><strong>Risk Level:</strong> {level}</p>
                    <p><strong>File Size:</strong> {(uploaded_file.size / 1024):.2f} KB</p>
                </div>
                """, unsafe_allow_html=True)

                st.success("Analysis Complete!")
                
                # Interactive Text Area
                st.text_area("CyberBoom Analysis Report", output, height=350)

                # ============================================================
                # PROFESSIONAL REPORT TEMPLATE (HTML DOWNLOAD)
                # ============================================================
                report_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>CyberBoom Security Report</title>
                    <style>
                        body {{ font-family: 'Segoe UI', sans-serif; background-color: #070B12; color: #E8F1F7; padding: 40px; }}
                        h1 {{ color: #00E5FF; }}
                        h2 {{ color: #00FF9C; border-bottom: 2px solid #00FF9C; padding-bottom: 10px; }}
                        .risk-high {{ color: #FF3B6B; font-weight: bold; }}
                        .risk-med {{ color: #FFD166; font-weight: bold; }}
                        .risk-low {{ color: #00FF9C; font-weight: bold; }}
                        pre {{ background-color: #0E1724; border: 1px solid #1E3445; padding: 20px; border-radius: 8px; white-space: pre-wrap; word-wrap: break-word; }}
                    </style>
                </head>
                <body>
                    <h1>🛡️ CYBERBOOM - SECURITY CLEARANCE REPORT</h1>
                    <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Sample Analyzed:</strong> {uploaded_file.name}</p>
                    <p><strong>Risk Score:</strong> {score}/100</p>
                    <p><strong>Risk Level:</strong> <span class="risk-{'high' if level == 'HIGH' else ('med' if level == 'MEDIUM' else 'low')}">{level}</span></p>
                    <hr>
                    <h2>Analysis Output</h2>
                    <pre>{html.escape(output)}</pre>
                    <hr>
                    <p><em>Generated by CyberBoom - Your Perfect Day Security Suite</em></p>
                </body>
                </html>
                """

                # Professional Download Button
                st.download_button(
                    label="📥 Download Security Report (HTML)",
                    data=report_html,
                    file_name=f"CyberBoom_Security_Report_{uploaded_file.name}.html",
                    mime="text/html"
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.write(f"Debug Info: {e}")
                
else:
    st.info("📁 Please upload a file to begin analysis.")
