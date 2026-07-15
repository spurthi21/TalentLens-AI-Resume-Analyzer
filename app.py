import streamlit as st
from pdf_reader import extract_text
from analyzer import analyze_resume

# 1. Page Configuration
st.set_page_config(
    page_title="TalentLens | AI Resume Analyzer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Themes-Compliant Custom Styling (Ensures High Contrast in both Light & Dark modes)
st.markdown("""
    <style>
    /* Main layout adjustments */
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    
    /* Metric Card Styling using CSS variables that adapt to light/dark themes automatically */
    .metric-card {
        background-color: var(--background-secondary-color, #F8FAFC);
        padding: 1.25rem;
        border-radius: 0.5rem;
        border: 1px solid var(--border-color, #E2E8F0);
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2563EB; /* Vibrant blue for high visibility */
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        color: var(--text-color, #64748B);
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Workspace
with st.sidebar:
    st.markdown("### **Workspace Control**")
    st.caption("Upload source documents and configure analysis parameters.")
    
    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf"],
        help="Supported formats: PDF. Maximum file size: 200MB."
    )
    
    st.divider()
    
    st.markdown("### **Analysis Settings**")
    model_mode = st.selectbox("Focus Area", ["Balanced", "Technical Depth", "Leadership & Impact"])
    strict_matching = st.toggle("Cross-reference Skills", value=True)
    
    st.divider()
    st.caption(" **Enterprise Security:** All processing happens locally on your machine.")

# 4. Main Application Canvas (Using native markdown headers for absolute contrast compliance)
st.title("💼 TalentLens AI")
st.markdown("##### Automated, locally-hosted resume intelligence engine.")
st.write("---")

if uploaded_file:
    # Read text immediately upon upload behind a clean status block
    with st.status("Extracting document vector text...", expanded=False) as status:
        resume = extract_text(uploaded_file)
        status.update(label="Document ingestion complete", state="complete")
    
    # Top-level dynamic metrics row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">PDF</div><div class="metric-label">Format Detected</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(resume.split())}</div><div class="metric-label">Word Count</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{model_mode}</div><div class="metric-label">Engine Profile</div></div>', unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Action Banner
    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        analyze_clicked = st.button("📊 Evaluate Candidate Profile", type="primary", use_container_width=True)
    with col_info:
        st.caption(" Click evaluate to initiate local LLM pattern matching and gap analysis.")

    st.divider()

    # Creative Tabbed Output Interface
    tab1, tab2, tab3 = st.tabs(["📋 Executive Report", "🛠️ Extracted Source Text", "⚙️ Metadata"])

    with tab1:
        if analyze_clicked:
            with st.spinner("Executing local LLM heuristics..."):
                result = analyze_resume(resume)
            
            st.toast("Profile evaluation matrix generated.", icon="🎯")
            
            # Display report using native markdown rendering for perfect text visibility
            st.markdown(result)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Export Executive Intelligence Brief (TXT)",
                data=result,
                file_name=f"TalentLens_Report_{uploaded_file.name.replace('.pdf', '')}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info("Initiate the evaluation engine via the button above to populate the executive brief.")

    with tab2:
        st.caption("Raw plaintext layer passed to the inference model:")
        # Display text inside a standard code block so it has a high-contrast background automatically
        st.code(resume, language="text", wrap_lines=True)

    with tab3:
        st.json({
            "Document Name": uploaded_file.name,
            "Mime Type": uploaded_file.type,
            "Byte Size": uploaded_file.size,
            "Target Engine Mode": model_mode,
            "Skill Isolation Layer": strict_matching
        })

else:
    st.info(" **Welcome to TalentLens.** To begin, drag and drop or upload a candidate resume in the left control panel.")