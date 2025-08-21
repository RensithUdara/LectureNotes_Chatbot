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

# Simple and clean CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #f8fafc;
        color: #1e293b;
    }
    
    .main .block-container {
        padding: 2rem 1rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin: 1rem;
        border: 1px solid #e2e8f0;
        color: #1e293b;
    }
    
    /* Text color improvements */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5 {
        color: #1e293b !important;
    }
    
    .stText {
        color: #1e293b !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #1e293b !important;
    }
    
    .css-1d391kg .stMarkdown {
        color: #f1f5f9 !important;
    }
    
    .css-1d391kg .stMarkdown h1,
    .css-1d391kg .stMarkdown h2,
    .css-1d391kg .stMarkdown h3,
    .css-1d391kg .stMarkdown p {
        color: #f1f5f9 !important;
    }
    
    /* Chat messages */
    .user-message {
        background: #3b82f6;
        color: white;
        padding: 1rem 1.25rem;
        border-radius: 16px 16px 4px 16px;
        margin: 0.75rem 0 0.75rem 20%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        animation: slideInRight 0.3s ease-out;
    }
    
    .bot-message {
        background: white;
        color: #1e293b;
        padding: 1rem 1.25rem;
        border-radius: 16px 16px 16px 4px;
        margin: 0.75rem 20% 0.75rem 0;
        border-left: 3px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        animation: slideInLeft 0.3s ease-out;
    }
    
    .message-label {
        font-weight: 600;
        font-size: 0.8rem;
        margin-bottom: 0.5rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.5px;
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
    
    /* Button styling */
    .stButton > button {
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        background: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        color: #1e293b !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        color: #1e293b !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }
    
    /* Chat container */
    .chat-container {
        max-height: 500px;
        overflow-y: auto;
        padding: 1.5rem;
        background: white;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        color: #1e293b;
    }
    
    /* General text color fixes */
    .stExpander > div > div > p {
        color: #1e293b !important;
    }
    
    .stInfo > div > div > p {
        color: #0c4a6e !important;
    }
    
    .stSuccess > div > div > p {
        color: #064e3b !important;
    }
    
    /* Metric styling */
    .stMetric > div > div {
        color: #1e293b !important;
    }
    
    .stMetric label {
        color: #64748b !important;
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
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {display:none;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .user-message, .bot-message { 
            margin-left: 5%; 
            margin-right: 5%; 
        }
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("# 🎓 AI Lecture Assistant")
st.markdown("##### Transform your study experience with AI-powered insights from your lecture notes")

# Sidebar
with st.sidebar:
    st.markdown("## 📚 Document Hub")
    st.markdown("*Upload and manage your learning materials*")
    st.markdown("---")
    
    st.markdown("### 📄 Upload Document")
    
    uploaded_file = st.file_uploader(
        "Choose your lecture notes (PDF)", 
        type="pdf",
        help="Upload a PDF file containing your lecture notes"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"📋 **{uploaded_file.name}**")
            st.caption(f"Size: {uploaded_file.size/1024:.1f} KB")
        with col2:
            if st.button("🚀", help="Process PDF", type="primary"):
                with st.spinner("Processing..."):
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
    
    st.markdown("---")
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
    
    st.markdown("---")
    st.markdown("### 💡 Quick Guide")
    st.markdown("""
    **Getting Started:**
    
    📤 **Step 1:** Upload your PDF  
    🚀 **Step 2:** Process the document  
    💬 **Step 3:** Start asking questions  
    🎯 **Step 4:** Get instant answers  
    
    **Example Questions:**
    - "What are the main topics?"
    - "Explain the key concepts"
    - "Summarize chapter 1"
    """)

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
<div style='text-align: center; color: #64748b;'>
    <p>🎓 <strong>AI Lecture Assistant</strong> | Powered by 🦙 LLaMA3 + 🦜 LangChain + ⚡ Streamlit</p>
    <p><em>Transforming education through intelligent AI conversations</em></p>
</div>
""", unsafe_allow_html=True)