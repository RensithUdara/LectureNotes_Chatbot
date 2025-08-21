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

# Professional CSS styling with custom CSS integration
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {{
        font-family: 'Inter', sans-serif;
        background: #f8f9fa;
        color: #2c3e50;
    }}
    
    /* General text styling */
    .stMarkdown, .stText, p, div, span {{
        color: #2c3e50 !important;
    }}
    
    /* Sidebar text styling */
    .css-1d391kg p, .css-1d391kg div {{
        color: rgba(255, 255, 255, 0.9) !important;
    }}
    
    .main .block-container {{
        padding-top: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin: 1rem;
    }}
    
    .css-1d391kg {{
        background: #2c3e50;
    }}
    
    .main-title {{
        color: #2c3e50;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
    }}
    
    .subtitle {{
        text-align: center;
        color: #34495e;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }}
    
    .chat-container {{
        max-height: 600px;
        overflow-y: auto;
        padding: 20px;
        background: rgba(248, 249, 250, 0.8);
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
    }}
    
    .user-message {{
        background: #3498db;
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0 10px 15%;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        animation: slideInRight 0.3s ease-out;
    }}
    
    .bot-message {{
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        color: #2c3e50;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 15% 10px 0;
        border-left: 4px solid #3498db;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        animation: slideInLeft 0.3s ease-out;
    }}
    
    .message-label {{
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 5px;
        opacity: 0.9;
    }}
    
    @keyframes slideInRight {{
        from {{ opacity: 0; transform: translateX(30px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    @keyframes slideInLeft {{
        from {{ opacity: 0; transform: translateX(-30px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    .stTextInput > div > div > input {{
        border-radius: 25px;
        border: 2px solid #e1e8ed;
        padding: 12px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
        color: #2c3e50 !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: #7f8c8d !important;
        opacity: 0.8;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
    }}
    
    .stButton > button {{
        background: #3498db;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
    }}
    
    .welcome-card {{
        background: rgba(248, 249, 250, 0.9);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(52, 152, 219, 0.2);
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }}
    
    .status-success {{
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
        margin: 5px 0;
    }}
    
    .status-warning {{
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
        margin: 5px 0;
    }}
    
    .progress-container {{
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        color: #2c3e50;
    }}
    
    /* Streamlit components text color */
    .stMetric {{
        color: #2c3e50 !important;
    }}
    
    .stMetric > div > div {{
        color: #2c3e50 !important;
    }}
    
    /* File uploader text */
    .stFileUploader > div > div {{
        color: #2c3e50 !important;
    }}
    
    /* Form labels and text */
    label {{
        color: #2c3e50 !important;
    }}
    
    /* Help text */
    .stTextInput > label > div {{
        color: #2c3e50 !important;
    }}
    
    #MainMenu {{visibility: hidden;}}
    .stDeployButton {{display:none;}}
    footer {{visibility: hidden;}}
    .stApp > header {{display:none;}}
    
    @media (max-width: 768px) {{
        .main-title {{ font-size: 2rem; }}
        .user-message, .bot-message {{ margin-left: 5%; margin-right: 5%; }}
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
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: white; font-weight: 600;'>📚 Document Hub</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem;'>Upload and manage your learning materials</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📄 Upload Document")
    
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
    <div style='text-align: center;'>
        <p>🎓 <strong>AI Lecture Assistant</strong> | Powered by 🦙 LLaMA3 + 🦜 LangChain + ⚡ Streamlit</p>
        <p><em>Transforming education through intelligent AI conversations</em></p>
    </div>
    """, 
    unsafe_allow_html=True
)
