# app.py
import streamlit as st
import os
from chatbot import ask, process_uploaded_pdf

# Set up page - Clean configuration
st.set_page_config(
    page_title="AI Lecture Assistant", 
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Complete Professional UI Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Reset and Base Styling */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Main App Background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #1e293b;
        min-height: 100vh;
    }
    
    /* Main Content Area */
    .main .block-container {
        padding: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
        margin: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        color: #1e293b;
    }
    
    /* Sidebar Complete Redesign */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%) !important;
        border-right: 3px solid #3b82f6 !important;
    }
    
    /* Sidebar Text Colors - Complete Fix for Dark Background */
    .css-1d391kg .stMarkdown {
        color: #f8fafc !important;
    }
    
    .css-1d391kg .stMarkdown h1,
    .css-1d391kg .stMarkdown h2,
    .css-1d391kg .stMarkdown h3,
    .css-1d391kg .stMarkdown h4,
    .css-1d391kg .stMarkdown p,
    .css-1d391kg .stMarkdown strong,
    .css-1d391kg .stMarkdown span,
    .css-1d391kg .stMarkdown div {
        color: #f8fafc !important;
    }
    
    .css-1d391kg .stMarkdown em {
        color: #cbd5e1 !important;
    }
    
    .css-1d391kg .stMarkdown small {
        color: #cbd5e1 !important;
    }
    
    /* File Uploader in Sidebar */
    .css-1d391kg .stFileUploader {
        background: rgba(59, 130, 246, 0.1) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: 2px dashed #3b82f6 !important;
    }
    
    .css-1d391kg .stFileUploader label {
        color: #f8fafc !important;
    }
    
    .css-1d391kg .stFileUploader > div > div > div {
        color: #f8fafc !important;
    }
    
    .css-1d391kg .stFileUploader button {
        color: #f8fafc !important;
        background: rgba(59, 130, 246, 0.2) !important;
        border: 1px solid #3b82f6 !important;
    }
    
    /* All text elements in sidebar */
    .css-1d391kg * {
        color: #f8fafc !important;
    }
    
    /* Override any dark text */
    .css-1d391kg .stText,
    .css-1d391kg .stCaption,
    .css-1d391kg .stWrite {
        color: #f8fafc !important;
    }
    
    /* Sidebar Buttons */
    .css-1d391kg .stButton > button {
        background: #3b82f6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .css-1d391kg .stButton > button:hover {
        background: #2563eb !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Sidebar File Uploader Text Fix */
    .css-1d391kg .stFileUploader .st-emotion-cache-1vt4y43 {
        color: #f8fafc !important;
    }
    
    .css-1d391kg .stFileUploader .st-emotion-cache-1vt4y43 p {
        color: #f8fafc !important;
    }
    
    .css-1d391kg .stFileUploader div[data-testid="stFileUploaderDropzone"] {
        color: #f8fafc !important;
    }
    
    .css-1d391kg .stFileUploader div[data-testid="stFileUploaderDropzone"] * {
        color: #f8fafc !important;
    }
    
    /* Force all sidebar text to be white */
    section[data-testid="stSidebar"] {
        color: #f8fafc !important;
    }
    
    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown * {
        color: #f8fafc !important;
    }
    
    section[data-testid="stSidebar"] .stWrite * {
        color: #f8fafc !important;
    }
    
    section[data-testid="stSidebar"] .stCaption * {
        color: #cbd5e1 !important;
    }
    
    /* Main Content Text Colors */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {
        color: #1e293b !important;
    }
    
    .stText {
        color: #1e293b !important;
    }
    
    /* Chat Messages - Enhanced Design */
    .user-message {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 1.25rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0 1rem 25%;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        animation: slideInRight 0.4s ease-out;
        position: relative;
    }
    
    .user-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, transparent 50%);
        border-radius: 20px 20px 5px 20px;
        pointer-events: none;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        color: #1e293b;
        padding: 1.25rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 25% 1rem 0;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        animation: slideInLeft 0.4s ease-out;
        position: relative;
    }
    
    .bot-message::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, transparent 50%);
        border-radius: 20px 20px 20px 5px;
        pointer-events: none;
    }
    
    .message-label {
        font-weight: 700;
        font-size: 0.75rem;
        margin-bottom: 0.75rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    /* Enhanced Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.75rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(59, 130, 246, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 6px 15px rgba(59, 130, 246, 0.3);
    }
    
    /* Enhanced Input Styling */
    .stTextInput > div > div > input {
        border-radius: 15px;
        border: 2px solid #cbd5e1;
        padding: 1rem 1.25rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        color: #1e293b !important;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
        color: #1e293b !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
        font-style: italic;
    }
    
    /* Enhanced Chat container */
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(15px);
        color: #1e293b;
    }
    
    /* Status Badges - Enhanced */
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.75rem 1.25rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
        text-align: center;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.75rem 1.25rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);
        text-align: center;
    }
    
    /* Welcome Cards - Premium Design */
    .welcome-card {
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
        color: #1e293b;
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .welcome-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
    }
    
    .welcome-card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .welcome-card strong {
        color: #1e293b;
        font-weight: 700;
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.5rem;
    }
    
    .welcome-card small {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Enhanced Component Styling */
    .stExpander > div > div > p {
        color: #1e293b !important;
    }
    
    /* Clean up any unwanted UI elements */
    .stApp .css-1rs6os,
    .stApp .css-17eq0hr,
    .stApp .css-1kyxreq {
        display: none !important;
    }
    
    /* Hide any text nodes that might contain arrow text */
    .stApp span:empty,
    .stApp div:empty {
        display: none !important;
    }
    
    /* Specific fix for keyboard arrow text */
    .stApp *[class*="keyboard"],
    .stApp *[class*="arrow"] {
        display: none !important;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(59, 130, 246, 0.05) 100%) !important;
        border-left: 4px solid #3b82f6 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .stInfo > div > div > p {
        color: #1e40af !important;
        font-weight: 500 !important;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%) !important;
        border-left: 4px solid #10b981 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .stSuccess > div > div > p {
        color: #065f46 !important;
        font-weight: 500 !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    .stError > div > div > p {
        color: #991b1b !important;
        font-weight: 500 !important;
    }
    
    /* Enhanced Metric styling */
    .stMetric {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        text-align: center;
    }
    
    .stMetric > div > div {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 1.5rem !important;
    }
    
    .stMetric label {
        color: #64748b !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Enhanced Expander */
    .stExpander {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.7) 0%, rgba(248, 250, 252, 0.7) 100%);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin: 0.5rem 0;
    }
    
    .stSpinner > div {
        border-top-color: #3b82f6 !important;
    }
    
    /* Footer styling */
    .footer-content {
        text-align: center;
        color: #64748b;
        background: rgba(255, 255, 255, 0.8);
        padding: 2rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        margin-top: 2rem;
    }
    
    .footer-content p {
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    .footer-content strong {
        color: #1e293b;
    }
    
    /* Status badges */
    .status-success {
        background: #10b981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.25rem 0;
    }
    
    .status-warning {
        background: #f59e0b;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.25rem 0;
    }
    
    /* Welcome cards */
    .welcome-card {
        text-align: center;
        padding: 1rem;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        transition: transform 0.3s ease;
        color: #1e293b;
    }
    
    .welcome-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    .welcome-card-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .welcome-card strong {
        color: #1e293b;
        font-weight: 600;
    }
    
    .welcome-card small {
        color: #64748b;
    }
    
    /* Hide Streamlit elements and fix unwanted text */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {display:none;}
    
    /* Hide sidebar toggle button text */
    .css-1rs6os .css-17eq0hr {
        display: none !important;
    }
    
    /* Hide any unwanted arrow text */
    .stButton .css-1rs6os {
        display: none !important;
    }
    
    /* Hide keyboard arrow text elements */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    /* Hide expand/collapse text */
    .css-1kyxreq {
        display: none !important;
    }
    
    /* Hide any text containing arrow keywords */
    *[title*="arrow"], 
    *[aria-label*="arrow"],
    *:contains("keyboard_double_arrow_right"),
    *:contains("arrow_right") {
        display: none !important;
    }
    
    /* Fix sidebar toggle area */
    .css-1d391kg .css-1rs6os {
        display: none !important;
    }
    
    /* Hide streamlit navigation elements */
    .stSelectbox > div[data-baseweb="select"] > div:first-child {
        display: none !important;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .user-message, .bot-message { 
            margin-left: 5%; 
            margin-right: 5%; 
        }
    }
    
    /* Additional cleanup */
    .stApp [data-testid="stSidebarNav"] {
        display: none !important;
    }
    
    .stApp button[kind="header"] {
        display: none !important;
    }
</style>

<script>
// Clean up any unwanted text elements
setTimeout(function() {
    // Remove any elements containing arrow text
    const unwantedElements = document.querySelectorAll('*');
    unwantedElements.forEach(element => {
        if (element.textContent && (
            element.textContent.includes('keyboard_double_arrow_right') ||
            element.textContent.includes('arrow_right') ||
            element.textContent.includes('keyboard_arrow_right')
        )) {
            element.style.display = 'none';
        }
    });
    
    // Hide sidebar toggle if it exists
    const sidebarToggle = document.querySelector('[data-testid="collapsedControl"]');
    if (sidebarToggle) {
        sidebarToggle.style.display = 'none';
    }
}, 1000);
</script>
""", unsafe_allow_html=True)

# Title
st.markdown("# 🎓 AI Lecture Assistant")
st.markdown("##### Transform your study experience with AI-powered insights from your lecture notes")

# Sidebar - Complete Professional Redesign
with st.sidebar:
    # Sidebar Header with Icon
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0 2rem 0;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">📚</div>
        <h2 style="color: #f8fafc; margin: 0; font-weight: 700; font-size: 1.4rem;">Document Hub</h2>
        <p style="color: #cbd5e1; margin: 0.5rem 0 0 0; font-style: italic; font-size: 0.9rem;">Your Learning Command Center</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Elegant Separator
    st.markdown("""
    <div style="height: 2px; background: linear-gradient(90deg, transparent 0%, #3b82f6 50%, transparent 100%); margin: 1rem 0 2rem 0; border-radius: 1px;"></div>
    """, unsafe_allow_html=True)
    
    # Document Upload Section
    st.markdown("""
    <div style="background: rgba(59, 130, 246, 0.1); padding: 1.5rem; border-radius: 15px; border: 1px solid rgba(59, 130, 246, 0.3); margin-bottom: 1.5rem;">
        <h3 style="color: #f8fafc; margin: 0 0 1rem 0; font-size: 1.1rem; display: flex; align-items: center;">
            <span style="font-size: 1.3rem; margin-right: 0.5rem;">📄</span>
            Upload Document
        </h3>
        <p style="color: #cbd5e1; margin: 0 0 1rem 0; font-size: 0.85rem; line-height: 1.4;">
            Transform your PDF lectures into interactive learning experiences
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your lecture notes (PDF)", 
        type="pdf",
        help="Upload a PDF file containing your lecture notes",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); padding: 1rem; border-radius: 12px; border-left: 4px solid #10b981; margin: 1rem 0;">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div style="color: #f8fafc;">
                <strong style="font-size: 0.9rem;">📋 {uploaded_file.name}</strong><br>
                <small style="color: #cbd5e1; font-size: 0.75rem;">Size: {uploaded_file.size/1024:.1f} KB</small>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("🚀", help="Process PDF", type="primary", key="process_pdf"):
                with st.spinner("🤖 Processing..."):
                    try:
                        success, message = process_uploaded_pdf(uploaded_file)
                        if success:
                            st.success("🎉 Ready!")
                            st.balloons()
                            st.session_state.pdf_processed = True
                            st.session_state.pdf_name = uploaded_file.name
                            st.rerun()
                        else:
                            st.error(f"❌ {message}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Status Dashboard
    st.markdown("""
    <div style="margin: 2rem 0 1.5rem 0;">
        <h3 style="color: #f8fafc; margin: 0 0 1rem 0; font-size: 1.1rem; display: flex; align-items: center;">
            <span style="font-size: 1.3rem; margin-right: 0.5rem;">📊</span>
            System Status
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    if hasattr(st.session_state, 'pdf_processed') and st.session_state.pdf_processed:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1rem 1.25rem; border-radius: 15px; margin: 1rem 0; text-align: center; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">✅</div>
            <strong style="color: white; font-size: 0.9rem; display: block;">Document Ready</strong>
            <small style="color: #d1fae5; font-size: 0.75rem;">{getattr(st.session_state, 'pdf_name', 'Document loaded')}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        if os.path.exists("ctse_lecture_notes.pdf"):
            st.markdown("""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 1rem 1.25rem; border-radius: 15px; margin: 1rem 0; text-align: center; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">📋</div>
                <strong style="color: white; font-size: 0.9rem; display: block;">Default Document</strong>
                <small style="color: #d1fae5; font-size: 0.75rem;">ctse_lecture_notes.pdf</small>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.pdf_processed = True
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 1rem 1.25rem; border-radius: 15px; margin: 1rem 0; text-align: center; box-shadow: 0 4px 15px rgba(245, 158, 11, 0.3);">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">⚠️</div>
                <strong style="color: white; font-size: 0.9rem; display: block;">No Document</strong>
                <small style="color: #fef3c7; font-size: 0.75rem;">Please upload a PDF file</small>
            </div>
            """, unsafe_allow_html=True)
    
    # AI Model Status
    st.markdown("""
    <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 12px; border: 1px solid rgba(59, 130, 246, 0.3); margin: 1rem 0; text-align: center;">
        <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">🦙</div>
        <strong style="color: #f8fafc; font-size: 0.85rem; display: block;">AI Model</strong>
        <small style="color: #cbd5e1; font-size: 0.75rem;">LLaMA3 Ready</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Elegant Separator
    st.markdown("""
    <div style="height: 2px; background: linear-gradient(90deg, transparent 0%, #3b82f6 50%, transparent 100%); margin: 2rem 0; border-radius: 1px;"></div>
    """, unsafe_allow_html=True)
    
    # Interactive Learning Guide
    st.markdown("""
    <div style="margin-bottom: 1.5rem;">
        <h3 style="color: #f8fafc; margin: 0 0 1rem 0; font-size: 1.1rem; display: flex; align-items: center;">
            <span style="font-size: 1.3rem; margin-right: 0.5rem;">💡</span>
            Learning Guide
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Learning Steps with Enhanced Design
    steps = [
        {"icon": "📤", "title": "Upload", "desc": "Add your PDF documents", "color": "#3b82f6"},
        {"icon": "🚀", "title": "Process", "desc": "AI analyzes your content", "color": "#10b981"},
        {"icon": "💬", "title": "Chat", "desc": "Ask questions & learn", "color": "#f59e0b"},
        {"icon": "🎯", "title": "Master", "desc": "Get instant insights", "color": "#8b5cf6"}
    ]
    
    for i, step in enumerate(steps, 1):
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 12px; margin: 0.75rem 0; border-left: 3px solid {step['color']}; transition: all 0.3s ease;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.2rem; margin-right: 0.75rem;">{step['icon']}</span>
                <div>
                    <strong style="color: #f8fafc; font-size: 0.9rem; display: block;">Step {i}: {step['title']}</strong>
                    <small style="color: #cbd5e1; font-size: 0.75rem; line-height: 1.3;">{step['desc']}</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Examples Section
    st.markdown("""
    <div style="margin-top: 2rem;">
        <h4 style="color: #f8fafc; margin: 0 0 1rem 0; font-size: 1rem; display: flex; align-items: center;">
            <span style="font-size: 1.1rem; margin-right: 0.5rem;">❓</span>
            Example Questions
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    examples = [
        "What are the main topics?",
        "Explain key concepts",
        "Summarize chapter 1",
        "Create practice questions"
    ]
    
    for example in examples:
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.03); padding: 0.75rem; border-radius: 8px; margin: 0.5rem 0; border: 1px solid rgba(255, 255, 255, 0.1);">
            <span style="color: #cbd5e1; font-size: 0.8rem;">💭 "{example}"</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer Credits in Sidebar
    st.markdown("""
    <div style="margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255, 255, 255, 0.1); text-align: center;">
        <small style="color: #64748b; font-size: 0.7rem; line-height: 1.4;">
            Powered by<br>
            🦙 LLaMA3 • 🦜 LangChain<br>
            ⚡ Streamlit • 🎓 AI
        </small>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

# Main content
st.markdown("## 💭 Interactive Learning Chat")

if not st.session_state.pdf_processed:
    # Welcome message
    st.info("**🚀 Welcome to AI Lecture Assistant!**")
    st.markdown("""
    Transform your learning experience with intelligent conversations about your study materials.
    
    **👈 Start by uploading your lecture notes in the sidebar**
    """)
    
    # Process steps using columns with proper HTML
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-card-icon">📤</div>
            <strong>Upload</strong><br>
            <small>Add your PDF documents</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-card-icon">🔄</div>
            <strong>Process</strong><br>
            <small>AI analyzes your content</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="welcome-card">
            <div class="welcome-card-icon">💬</div>
            <strong>Chat</strong><br>
            <small>Ask questions & learn</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.stop()

# Chat interface
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        user_query = st.text_input(
            "Ask anything about your lecture notes...", 
            placeholder="e.g., What are the main concepts in this chapter?",
            label_visibility="collapsed"
        )
    with col2:
        submit = st.form_submit_button("🚀 Ask", type="primary", use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        clear_history = st.form_submit_button("🗑️ Clear", use_container_width=True)
    with col2:
        suggestions_btn = st.form_submit_button("💡 Tips", use_container_width=True)

# Show suggestions
if suggestions_btn:
    st.markdown("#### 💡 Suggested Questions:")
    suggestions = [
        "What are the main topics covered?",
        "Can you summarize the key points?", 
        "Explain the most important concepts",
        "What should I focus on for the exam?",
        "Give me practice questions"
    ]
    
    for suggestion in suggestions:
        st.markdown(f"💭 {suggestion}")

# Clear chat history
if clear_history:
    st.session_state.chat_history = []
    st.rerun()

# Process query
if submit and user_query:
    if st.session_state.pdf_processed:
        try:
            with st.spinner("🤖 AI is thinking..."):
                answer = ask(user_query)
            
            st.session_state.chat_history.append(("You", user_query))
            st.session_state.chat_history.append(("Bot", answer))
            st.rerun()
        except Exception as e:
            st.session_state.chat_history.append(("Bot", f"⚠️ Error: {str(e)}"))
            st.rerun()
    else:
        st.error("Please upload and process a PDF file first.")

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 📜 Conversation History")
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for i in range(len(st.session_state.chat_history)-1, -1, -1):
        role, msg = st.session_state.chat_history[i]
        if role == "You":
            st.markdown(
                f"""
                <div class="user-message">
                    <div class="message-label">You asked:</div>
                    {msg}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="bot-message">
                    <div class="message-label">AI Assistant:</div>
                    {msg}
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Ready to learn message using Streamlit components
    st.success("**🎯 Ready to Learn!**")
    st.markdown("Your AI assistant is ready to help you understand your lecture notes better.")
    
    st.markdown("#### 📝 What you can ask:")
    
    # Example questions in expandable sections
    with st.expander("🔍 Summarization Questions"):
        st.write("• Give me a summary of chapter 3")
        st.write("• What are the key takeaways?")
        st.write("• Summarize the main points")
    
    with st.expander("💡 Explanation Questions"):
        st.write("• What does this concept mean?")
        st.write("• How does this work?")
        st.write("• Explain this in simple terms")
    
    with st.expander("🎯 Focus Questions"):
        st.write("• What are the key points to remember?")
        st.write("• What's most important for the exam?")
        st.write("• Which topics should I prioritize?")
    
    with st.expander("❓ Practice Questions"):
        st.write("• Ask me questions about this topic")
        st.write("• Give me some practice problems")
        st.write("• Test my understanding")
    
    st.info("💬 Type your question above or click 'Tips' for more ideas!")

# Footer with stats
if st.session_state.chat_history:
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    total_questions = len([msg for role, msg in st.session_state.chat_history if role == "You"])
    total_responses = len([msg for role, msg in st.session_state.chat_history if role == "Bot"])
    
    with col1:
        st.metric("Questions", total_questions)
    with col2:
        st.metric("Responses", total_responses)
    with col3:
        if hasattr(st.session_state, 'pdf_name'):
            st.metric("Document", f"{st.session_state.pdf_name[:10]}...")
    with col4:
        st.metric("Status", "Ready")

# Footer
st.markdown("---")
st.markdown("""
<div class='footer-content'>
    <p>🎓 <strong>AI Lecture Assistant</strong> | Powered by 🦙 LLaMA3 + 🦜 LangChain + ⚡ Streamlit</p>
    <p><em>Transforming education through intelligent AI conversations</em></p>
</div>
""", unsafe_allow_html=True)