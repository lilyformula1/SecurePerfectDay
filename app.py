import streamlit as st
import sys
import os
import tempfile
import re

sys.path.append(os.path.dirname(__file__))
from cyberguard import analyze

st.set_page_config(page_title="Perfect Day - Secure Scan", page_icon="🛡️")

st.markdown("""
<style>
    .stApp { background-color: #070B12; }
    h1, h2, h3, h4, h5, h6 { color: #00E5FF !important; font-family: 'Segoe UI', sans-serif; }
    p, label, div { color: #E8F1F7 !important; }
    section[data-testid="stSidebar"] { background-color: #0A121F; border-right: 1px solid #1E3445; }
    .stButton > button { background-color: #101C2B; color: #00E5FF; font-weight: bold; border: 1px solid #1E3445; border-radius: 6px; transition: all 0.3s ease; }
    .stButton > button:hover { background-color: #00E5FF; color: #070B12; border: 1px solid #00E5FF; }
    .stButton > button[kind="primary"] { background-color: #00E5FF; color: #070B12; border: 1px solid #00E5FF; }
    .stButton > button[kind="primary"]:hover { background-color: #00FF9C; border: 1px solid #00FF9C; color: #070B12; }
    .stFileUploader { background-color: #101C2B; border: 1px solid #1E3445; border-radius: 8px; padding: 10px; }
    textarea { background-color: #0E1724 !important; color: #E8F1F7 !important; border: 1px solid #1E3445 !important; font-family: 'Courier New', monospace; font-size: 14px; }
    .stDownloadButton > button { background-color: #142433; color: #00FF9C; border: 1px solid #00FF9C; font-weight: bold; border-radius: 6px; padding: 10px; transition: all 0.3s ease; }
    .stDownloadButton > button:hover { background-color: #00FF9C; color: #070B12; }
    [data-testid="stMetricValue"] { color: #00E5FF !important; font-family: 'Segoe UI', sans-serif; }
    [data-testid="stMetricLabel"] { color: #7F98A8 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Your Perfect Day Starts Here")
st.caption("A perfect day is a day where you don't get hacked. Use CyberBoom to scan your files and keep your day safe!")
st.write("Upload any suspicious file to make sure your system stays secure.")

uploaded_file = st.file_uploader("Upload a Windows executable for analysis", type=['exe', 'dll', 'sys'])

if uploaded_file is not None:
    st.success(f"Sample Loaded: {uploaded_file.name} ({(uploaded_file.size / 1024):.2f} KB)")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        temp_path = tmp_file.name

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
                full_output = analyze(temp_path, "full")
                
                if requested_mode == "full":
                    output = full_output
                else:
                    output = ""
                    capture = False
                    
                    # Run through the output line by line
                    for line in full_output.splitlines():
                        # Check if line starts with a Header
                        if "HASH ANALYSIS" in line or "STRING ANALYSIS" in line or "PE ANALYSIS" in line or "API DETECTION" in line or "ENTROPY ANALYSIS" in line or "RISK ASSESSMENT" in line:
                            # Start capturing if this is the requested section
                            if ("HASH ANALYSIS" in line and requested_mode == "hash") or \
                               ("STRING ANALYSIS" in line and requested_mode == "strings") or \
                               ("PE ANALYSIS" in line and requested_mode == "pe") or \
                               ("API DETECTION" in line and requested_mode == "api") or \
                               ("ENTROPY ANALYSIS" in line and requested_mode == "entropy") or \
                               ("RISK ASSESSMENT" in line and requested_mode == "risk"):
                                capture = True
                            else:
                                # If it's a different header, stop capturing
                                capture = False
                        
                        # Add the line if we are capturing
                        if capture:
                            output += line + "\n"

                if not output.strip():
                    output = full_output

                risk_match = re.search(r"Risk Score\s*:\s*(\d+)", full_output)
                level_match = re.search(r"Risk Level\s*:\s*(HIGH|MEDIUM|LOW)", full_output)
                
                score = int(risk_match.group(1)) if risk_match else 0
                level = level_match.group(1) if level_match else "N/A"
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Risk Score", f"{score}/100")
                col2.metric("Risk Level", level)
                col3.metric("File Size", f"{(uploaded_file.size / 1024):.2f} KB")
                
                st.success("Analysis Complete!")
                st.text_area("Analysis Output", output, height=400)
                
                st.download_button(
                    label="📥 Save Report (.txt)",
                    data=output,
                    file_name=f"CyberBoom_Report_{uploaded_file.name}.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.write(f"Debug Info: {e}")
                
else:
    st.info("📁 Please upload a file to begin analysis.")