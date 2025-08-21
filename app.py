# app.py
import streamlit as st
import os
from chatbot import ask, process_uploaded_pdf  # Importing functions from chatbot.py

# Set up page
st.set_page_config(
    page_title="AI Lecture Assistant", 
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.        with col2:
            if st.button("🚀", help="Process PDF", type="primary"):
                # Enhanced processing with better UX
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    status_text.text("🔄 Analyzing document structure...")
                    progress_bar.progress(25)
                    
                    success, message = process_uploaded_pdf(uploaded_file)
                    
                    if success:
                        status_text.text("✅ Processing completed!")
                        progress_bar.progress(100)
                        
                        # Success notification
                        st.success("🎉 Document ready for questions!")
                        st.balloons()
                        
                        st.session_state.pdf_processed = True
                        st.session_state.pdf_name = uploaded_file.name
                        # Store the current PDF info for reference
                        st.session_state.current_pdf_info = {
                            'name': uploaded_file.name,
                            'processed': True
                        }
                        
                        # Clear progress indicators
                        progress_bar.empty()
                        status_text.empty()
                        st.rerun()
                    else:
                        status_text.text("❌ Processing failed")
                        progress_bar.progress(0)
                        st.error(f"❌ {message}")
                        
                except Exception as e:
                    status_text.text("❌ An error occurred")
                    progress_bar.progress(0)
                    st.error(f"❌ Error: {str(e)}")yle>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #2c3e50;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        margin: 1rem;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
        border-radius: 0 20px 20px 0;
    }
    
    .css-1d391kg .stMarkdown {
        color: white;
    }
    
    /* Title styling */
    .main-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Chat container styling */
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 20px;
        background: rgba(248, 249, 250, 0.8);
        border-radius: 15px;
        border: 1px solid rgba(222, 226, 230, 0.6);
        margin: 20px 0;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Message bubbles */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0 10px 15%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        animation: slideInRight 0.3s ease-out;
        position: relative;
    }
    
    .user-message::before {
        content: "👤";
        position: absolute;
        left: -35px;
        top: 50%;
        transform: translateY(-50%);
        background: white;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    .bot-message {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        color: #2c3e50;
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 15% 10px 0;
        border-left: 4px solid #3498db;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        animation: slideInLeft 0.3s ease-out;
        position: relative;
    }
    
    .bot-message::before {
        content: "🤖";
        position: absolute;
        right: -35px;
        top: 50%;
        transform: translateY(-50%);
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        border-radius: 50%;
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    .message-label {
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 5px;
        opacity: 0.9;
    }
    
    /* Animations */
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Form styling */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 2px solid #e1e8ed;
        padding: 12px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: white;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 12px 30px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar enhancements */
    .sidebar-content {
        padding: 20px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.1);
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
    
    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 20px;
        background: rgba(102, 126, 234, 0.05);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #764ba2;
        background: rgba(118, 75, 162, 0.1);
    }
    
    /* Welcome card */
    .welcome-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(102, 126, 234, 0.2);
        margin: 20px 0;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* Status indicators */
    .status-success {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
        margin: 5px 0;
    }
    
    .status-warning {
        background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 20px;
        font-weight: 500;
        display: inline-block;
        margin: 5px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-top: 40px;
        border-top: 1px solid rgba(127, 140, 141, 0.2);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stApp > header {display:none;}
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .user-message, .bot-message {
            margin-left: 5%;
            margin-right: 5%;
        }
        
        .user-message::before, .bot-message::before {
            display: none;
        }
    }
</style>
""", unsafe_allow_html=True)

# Title and description with professional styling
st.markdown('<h1 class="main-title">🎓 AI Lecture Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Transform your study experience with AI-powered insights from your lecture notes</p>', unsafe_allow_html=True)

# Sidebar for PDF upload
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h2 style='color: white; font-weight: 600; margin-bottom: 0;'>📚 Document Hub</h2>
        <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem;'>Upload and manage your learning materials</p>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### 📄 Upload Document")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose your lecture notes (PDF)", 
        type="pdf",
        help="Upload a PDF file containing your lecture notes",
        label_visibility="collapsed"
    )
    
    # Process uploaded file
    if uploaded_file is not None:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**📋 {uploaded_file.name}**")
            st.markdown(f"*Size: {uploaded_file.size/1024:.1f} KB*")
        with col2:
            if st.button("�", help="Process PDF", type="primary"):
                with st.spinner("🔄 Processing..."):
                    success, message = process_uploaded_pdf(uploaded_file)
                    if success:
                        st.success("✅ Ready!")
                        st.session_state.pdf_processed = True
                        st.session_state.pdf_name = uploaded_file.name
                        # Store the current PDF info for reference
                        st.session_state.current_pdf_info = {
                            'name': uploaded_file.name,
                            'processed': True
                        }
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Status section
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.markdown("### 📊 Status")
    
    # Display current PDF status
    if hasattr(st.session_state, 'pdf_processed') and st.session_state.pdf_processed:
        st.markdown(f"""
        <div class="status-success">
            ✅ Document Ready<br>
            <small>{getattr(st.session_state, 'pdf_name', 'Document loaded')}</small>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Check if default PDF exists
        if os.path.exists("ctse_lecture_notes.pdf"):
            st.markdown(f"""
            <div class="status-success">
                📋 Default Document<br>
                <small>ctse_lecture_notes.pdf</small>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.pdf_processed = True
        else:
            st.markdown(f"""
            <div class="status-warning">
                ⚠️ No Document<br>
                <small>Please upload a PDF file</small>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick guide
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

# Main chat interface
st.markdown("### � Interactive Learning Chat")

# Check if PDF is ready
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
    
    # Additional controls
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        clear_history = st.form_submit_button("🗑️ Clear Chat", use_container_width=True)
    with col2:
        if st.form_submit_button("💡 Get Suggestions", use_container_width=True):
            suggestions = [
                "What are the main topics covered?",
                "Can you summarize the key points?",
                "Explain the most important concepts",
                "What should I focus on for the exam?",
                "Give me practice questions on this topic"
            ]
            st.session_state.show_suggestions = True

# Suggestion buttons
if hasattr(st.session_state, 'show_suggestions') and st.session_state.show_suggestions:
    st.markdown("#### 💡 Suggested Questions:")
    suggestions = [
        "What are the main topics covered?",
        "Can you summarize the key points?", 
        "Explain the most important concepts",
        "What should I focus on for the exam?",
        "Give me practice questions"
    ]
    
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(f"💭 {suggestion[:20]}...", key=f"sug_{i}", help=suggestion):
                # Simulate user input
                st.session_state.suggested_query = suggestion
                st.session_state.show_suggestions = False
                st.rerun()

# Clear chat history
if clear_history:
    st.session_state.chat_history = []
    st.session_state.show_suggestions = False
    st.rerun()

# Handle suggested query
if hasattr(st.session_state, 'suggested_query'):
    user_query = st.session_state.suggested_query
    submit = True
    delattr(st.session_state, 'suggested_query')

# Process the user query
if submit and user_query:
    if st.session_state.pdf_processed:
        try:
            with st.spinner("🤖 Thinking..."):
                # Don't pass pdf_path since the chatbot now manages it internally
                answer = ask(user_query)
            
            # Save Q&A to history
            st.session_state.chat_history.append(("You", user_query))
            st.session_state.chat_history.append(("Bot", answer))
        except Exception as e:
            st.session_state.chat_history.append(("Bot", f"⚠️ Error: {str(e)}"))
    else:
        st.error("Please upload and process a PDF file first.")

# Display chat history with enhanced styling
if st.session_state.chat_history:
    st.markdown("### 📜 Conversation History")
    
    # Chat container with custom styling
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display messages in reverse order (newest first)
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
    # Enhanced welcome message when no chat history
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
        <p><em>💬 Type your question above or click "Get Suggestions" for ideas!</em></p>
    </div>
    """)

# Enhanced footer with stats and info
st.markdown('<div class="footer">', unsafe_allow_html=True)

# Stats row
if st.session_state.chat_history:
    total_questions = len([msg for role, msg in st.session_state.chat_history if role == "You"])
    total_responses = len([msg for role, msg in st.session_state.chat_history if role == "Bot"])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"**📊 Questions Asked:** {total_questions}")
    with col2:
        st.markdown(f"**🤖 AI Responses:** {total_responses}")
    with col3:
        if hasattr(st.session_state, 'pdf_name'):
            st.markdown(f"**📄 Current Doc:** {st.session_state.pdf_name}")
    with col4:
        st.markdown("**🚀 Status:** Ready")

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
st.markdown('</div>', unsafe_allow_html=True)

# Display chat history with improved styling

# Display chat history with improved styling
if st.session_state.chat_history:
    st.markdown("### 📝 Chat History")
    
    # Custom CSS for chat bubbles
    st.markdown("""
        <style>
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
            background-color: #fafafa;
            border: 1px solid #ddd;
            border-radius: 10px;
            margin: 10px 0;
        }
        .user-message {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            margin: 8px 0 8px 20%;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .bot-message {
            background: #ffffff;
            color: #333;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            margin: 8px 20% 8px 0;
            border-left: 4px solid #4CAF50;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .message-label {
            font-weight: bold;
            font-size: 0.8em;
            margin-bottom: 4px;
        }
        </style>
        <div class="chat-container">
    """, unsafe_allow_html=True)
    
    # Display messages in reverse order (newest first)
    for i in range(len(st.session_state.chat_history)-1, -1, -1):
        role, msg = st.session_state.chat_history[i]
        if role == "You":
            st.markdown(
                f"""
                <div class="user-message">
                    <div class="message-label">🧑 You</div>
                    {msg}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="bot-message">
                    <div class="message-label">🤖 Assistant</div>
                    {msg}
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown("</div>", unsafe_allow_html=True)

else:
    # Welcome message when no chat history
    st.info("""
    👋 **Welcome to the Lecture Notes Chatbot!**
    
    🔹 Upload your lecture notes PDF using the sidebar
    🔹 Ask any questions about the content  
    🔹 Get instant AI-powered answers
    
    Ready to start learning? Upload your PDF and ask your first question!
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Powered by 🦙 LLaMA3 + � LangChain + ⚡ Streamlit"
    "</div>", 
    unsafe_allow_html=True
)

