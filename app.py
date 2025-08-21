# app.py
import streamlit as st
import os
from chatbot import ask, process_uploaded_pdf

# Set up page
st.set_page_config(
    page_title="AI Lecture Assistant", 
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    """Load CSS from assets/custom.css if it exists"""
    css_file = "assets/custom.css"
    if os.path.exists(css_file):
        with open(css_file, 'r') as f:
            return f.read()
    return ""

custom_css = load_css()

# Professional CSS styling with minimal colors and 3D shadows
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for consistent theming */
    :root {{
        --primary-bg: #ffffff;
        --secondary-bg: #f8fafc;
        --sidebar-bg: #1e293b;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-light: #94a3b8;
        --accent-blue: #3b82f6;
        --accent-blue-hover: #2563eb;
        --border-color: #e2e8f0;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }}
    
    /* Main app container */
    .stApp {{
        font-family: 'Inter', sans-serif;
        background: var(--secondary-bg);
        color: var(--text-primary);
    }}
    
    /* Main content area */
    .main .block-container {{
        padding: 2rem 1rem;
        background: var(--primary-bg);
        border-radius: 12px;
        box-shadow: var(--shadow-lg);
        margin: 1rem;
        border: 1px solid var(--border-color);
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background: var(--sidebar-bg) !important;
        border-right: 1px solid #334155;
    }}
    
    .css-1d391kg .stMarkdown {{
        color: #f1f5f9 !important;
    }}
    
    .css-1d391kg .stMarkdown h1,
    .css-1d391kg .stMarkdown h2,
    .css-1d391kg .stMarkdown h3,
    .css-1d391kg .stMarkdown p {{
        color: #f1f5f9 !important;
    }}
    
    /* Title styling */
    .main-title {{
        color: var(--text-primary);
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: var(--shadow-sm);
    }}
    
    .subtitle {{
        text-align: center;
        color: var(--text-secondary);
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }}
    
    /* Chat container with 3D effect */
    .chat-container {{
        max-height: 500px;
        overflow-y: auto;
        padding: 1.5rem;
        background: var(--primary-bg);
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
    }}
    
    /* User message styling */
    .user-message {{
        background: var(--accent-blue);
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 16px 16px 4px 16px;
        margin: 0.75rem 0 0.75rem 20%;
        box-shadow: var(--shadow-md);
        animation: slideInRight 0.3s ease-out;
        border: 1px solid rgba(59, 130, 246, 0.1);
    }}
    
    /* Bot message styling */
    .bot-message {{
        background: var(--primary-bg);
        color: var(--text-primary);
        padding: 1rem 1.25rem;
        border-radius: 16px 16px 16px 4px;
        margin: 0.75rem 20% 0.75rem 0;
        border-left: 3px solid var(--accent-blue);
        box-shadow: var(--shadow-md);
        animation: slideInLeft 0.3s ease-out;
        border: 1px solid var(--border-color);
    }}
    
    .message-label {{
        font-weight: 600;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    /* Animation keyframes */
    @keyframes slideInRight {{
        from {{ opacity: 0; transform: translateX(20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    @keyframes slideInLeft {{
        from {{ opacity: 0; transform: translateX(-20px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    /* Input styling */
    .stTextInput > div > div > input {{
        border-radius: 12px;
        border: 2px solid var(--border-color);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: var(--primary-bg);
        color: var(--text-primary);
        box-shadow: var(--shadow-sm);
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: var(--accent-blue);
        box-shadow: var(--shadow-md), 0 0 0 3px rgba(59, 130, 246, 0.1);
        outline: none;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: var(--text-light);
        opacity: 0.8;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: var(--accent-blue);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-md);
        border: 1px solid rgba(59, 130, 246, 0.1);
    }}
    
    .stButton > button:hover {{
        background: var(--accent-blue-hover);
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
        box-shadow: var(--shadow-md);
    }}
    
    /* Welcome card styling */
    .welcome-card {{
        background: var(--primary-bg);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: var(--shadow-lg);
        position: relative;
    }}
    
    .welcome-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--accent-blue), #8b5cf6);
        border-radius: 16px 16px 0 0;
    }}
    
    /* Status indicators */
    .status-success {{
        background: #10b981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.25rem 0;
        box-shadow: var(--shadow-sm);
    }}
    
    .status-warning {{
        background: #f59e0b;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        font-size: 0.85rem;
        display: inline-block;
        margin: 0.25rem 0;
        box-shadow: var(--shadow-sm);
    }}
    
    /* Progress container */
    .progress-container {{
        background: var(--primary-bg);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        text-align: center;
        color: var(--text-primary);
    }}
    
    /* Metrics styling */
    .stMetric {{
        background: var(--primary-bg);
        padding: 1rem;
        border-radius: 8px;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
    }}
    
    .stMetric > div {{
        color: var(--text-primary) !important;
    }}
    
    .stMetric > div > div {{
        color: var(--text-primary) !important;
    }}
    
    /* File uploader styling */
    .stFileUploader {{
        background: var(--primary-bg);
        border-radius: 8px;
        padding: 0.5rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
    }}
    
    .stFileUploader > div {{
        color: var(--text-primary) !important;
    }}
    
    /* Sidebar file uploader */
    .css-1d391kg .stFileUploader {{
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }}
    
    .css-1d391kg .stFileUploader > div {{
        color: #f1f5f9 !important;
    }}
    
    /* Process step cards */
    .process-step {{
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        transition: transform 0.2s ease;
    }}
    
    .process-step:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }}
    
    /* Hide Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    footer {{visibility: hidden;}}
    .stApp > header {{display:none;}}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .main-title {{ font-size: 2rem; }}
        .user-message, .bot-message {{ 
            margin-left: 5%; 
            margin-right: 5%; 
        }}
        .main .block-container {{
            margin: 0.5rem;
            padding: 1rem;
        }}
    }}
    
    /* Custom scrollbar */
    .chat-container::-webkit-scrollbar {{
        width: 6px;
    }}
    
    .chat-container::-webkit-scrollbar-track {{
        background: var(--border-color);
        border-radius: 3px;
    }}
    
    .chat-container::-webkit-scrollbar-thumb {{
        background: var(--text-light);
        border-radius: 3px;
    }}
    
    .chat-container::-webkit-scrollbar-thumb:hover {{
        background: var(--text-secondary);
    }}
    
    /* Custom CSS from assets/custom.css */
    {custom_css}
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown('<h1 class="main-title">🎓 AI Lecture Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your study experience with AI-powered insights from your lecture notes</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 1.5rem;'>
        <h2 style='color: #f1f5f9; font-weight: 600; margin-bottom: 0.5rem; font-size: 1.5rem;'>📚 Document Hub</h2>
        <p style='color: #cbd5e1; font-size: 0.85rem; margin: 0; opacity: 0.9;'>Upload and manage your learning materials</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='margin-bottom: 1rem;'>
        <h3 style='color: #f1f5f9; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;'>📄 Upload Document</h3>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your lecture notes (PDF)", 
        type="pdf",
        help="Upload a PDF file containing your lecture notes"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📋 {uploaded_file.name}**")
            st.markdown(f"*Size: {uploaded_file.size/1024:.1f} KB*")
        with col2:
            if st.button("🚀", help="Process PDF", type="primary"):
                # Show loading animation using custom CSS
                progress_placeholder = st.empty()
                with progress_placeholder:
                    st.markdown("""
                    <div class="progress-container">
                        <div class="loading-dots">
                            <div></div><div></div><div></div><div></div>
                        </div>
                        <p>Processing your document...</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                try:
                    success, message = process_uploaded_pdf(uploaded_file)
                    progress_placeholder.empty()
                    
                    if success:
                        st.success("🎉 Ready!")
                        st.balloons()
                        st.session_state.pdf_processed = True
                        st.session_state.pdf_name = uploaded_file.name
                        st.session_state.current_pdf_info = {
                            'name': uploaded_file.name,
                            'processed': True
                        }
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                except Exception as e:
                    progress_placeholder.empty()
                    st.error(f"❌ Error processing PDF: {str(e)}")
    
    st.markdown("### 📊 Status")
    
    if hasattr(st.session_state, 'pdf_processed') and st.session_state.pdf_processed:
        st.markdown(f"""
        <div class="status-success">
            ✅ Document Ready<br>
            <small>{getattr(st.session_state, 'pdf_name', 'Document loaded')}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        if os.path.exists("ctse_lecture_notes.pdf"):
            st.markdown("""
            <div class="status-success">
                📋 Default Document<br>
                <small>ctse_lecture_notes.pdf</small>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.pdf_processed = True
        else:
            st.markdown("""
            <div class="status-warning">
                ⚠️ No Document<br>
                <small>Please upload a PDF file</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### 💡 Quick Guide")
    st.markdown("""
    **Step 1:** 📤 Upload your PDF  
    **Step 2:** 🚀 Process the document  
    **Step 3:** 💬 Start asking questions  
    **Step 4:** 🎯 Get instant answers  
    
    ---
    
    **💬 Try asking:**
    - "What are the main topics?"
    - "Explain the key concepts"
    - "Summarize chapter 1"
    """)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

# Main chat interface
st.markdown("### 💭 Interactive Learning Chat")

if not st.session_state.pdf_processed:
    st.markdown("""
    <div class="welcome-card">
        <h3>🚀 Welcome to AI Lecture Assistant!</h3>
        <p>Transform your learning experience with intelligent conversations about your study materials.</p>
        <p><strong>👈 Start by uploading your lecture notes in the sidebar</strong></p>
        <br>
        <div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.8); padding: 15px; border-radius: 10px; margin: 5px;">
                <strong>📤 Upload</strong><br>
                <small>Add your PDF documents</small>
            </div>
            <div style="background: rgba(255,255,255,0.8); padding: 15px; border-radius: 10px; margin: 5px;">
                <strong>🔄 Process</strong><br>
                <small>AI analyzes your content</small>
            </div>
            <div style="background: rgba(255,255,255,0.8); padding: 15px; border-radius: 10px; margin: 5px;">
                <strong>💬 Chat</strong><br>
                <small>Ask questions & learn</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Chat input form
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        user_query = st.text_input(
            "💬 Ask anything about your lecture notes...", 
            key="user_input",
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
        st.markdown(f"**💭** {suggestion}")

# Clear chat history
if clear_history:
    st.session_state.chat_history = []
    st.rerun()

# Process query
if submit and user_query:
    if st.session_state.pdf_processed:
        try:
            # Show thinking animation
            thinking_placeholder = st.empty()
            with thinking_placeholder:
                st.markdown("""
                <div class="progress-container">
                    <div class="loading-dots">
                        <div></div><div></div><div></div><div></div>
                    </div>
                    <p>🤖 AI is thinking...</p>
                </div>
                """, unsafe_allow_html=True)
            
            answer = ask(user_query)
            thinking_placeholder.empty()
            
            st.session_state.chat_history.append(("You", user_query))
            st.session_state.chat_history.append(("Bot", answer))
            st.rerun()
        except Exception as e:
            thinking_placeholder.empty()
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
    st.markdown("""
    <div class="welcome-card">
        <h3>🎯 Ready to Learn!</h3>
        <p>Your AI assistant is ready to help you understand your lecture notes better.</p>
        <br>
        <div style="text-align: left; max-width: 600px; margin: 0 auto;">
            <h4>📝 What you can ask:</h4>
            <ul style="list-style: none; padding: 0;">
                <li>🔍 <strong>Summarize:</strong> "Give me a summary of chapter 3"</li>
                <li>💡 <strong>Explain:</strong> "What does this concept mean?"</li>
                <li>🎯 <strong>Focus:</strong> "What are the key points to remember?"</li>
                <li>❓ <strong>Quiz:</strong> "Ask me questions about this topic"</li>
                <li>🔗 <strong>Connect:</strong> "How does this relate to previous topics?"</li>
            </ul>
        </div>
        <br>
        <p><em>💬 Type your question above or click "Tips" for more ideas!</em></p>
    </div>
    """)

# Footer with stats
if st.session_state.chat_history:
    total_questions = len([msg for role, msg in st.session_state.chat_history if role == "You"])
    total_responses = len([msg for role, msg in st.session_state.chat_history if role == "Bot"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Questions", total_questions)
    with col2:
        st.metric("Responses", total_responses)
    with col3:
        if hasattr(st.session_state, 'pdf_name'):
            st.metric("Document", f"{st.session_state.pdf_name[:10]}...")
    with col4:
        st.metric("Status", "Ready")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #34495e;'>
        <p>🎓 <strong>AI Lecture Assistant</strong> | Powered by 🦙 LLaMA3 + 🦜 LangChain + ⚡ Streamlit</p>
        <p><em>Transforming education through intelligent AI conversations</em></p>
    </div>
    """, 
    unsafe_allow_html=True
)
