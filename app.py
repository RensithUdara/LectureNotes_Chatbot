# app.py
import streamlit as st
import os
from chatbot import ask, process_uploaded_pdf  # Importing functions from chatbot.py

# Set up page
st.set_page_config(
    page_title="Lecture Notes Chatbot", 
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📘 Lecture Notes Chatbot")
st.markdown("*Powered by LLaMA3 + LangChain*")

# Sidebar for PDF upload
with st.sidebar:
    st.header("📄 PDF Management")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your lecture notes (PDF)", 
        type="pdf",
        help="Upload a PDF file containing your lecture notes"
    )
    
    # Process uploaded file
    if uploaded_file is not None:
        if st.button("📤 Process PDF", type="primary"):
            with st.spinner("Processing PDF... This may take a few moments."):
                success, message = process_uploaded_pdf(uploaded_file)
                if success:
                    st.success(message)
                    st.session_state.pdf_processed = True
                    st.session_state.pdf_name = uploaded_file.name
                else:
                    st.error(message)
    
    # Display current PDF status
    if hasattr(st.session_state, 'pdf_processed') and st.session_state.pdf_processed:
        st.success(f"✅ PDF Ready: {getattr(st.session_state, 'pdf_name', 'Unknown')}")
    else:
        # Check if default PDF exists
        if os.path.exists("ctse_lecture_notes.pdf"):
            st.info("📋 Using default: ctse_lecture_notes.pdf")
            st.session_state.pdf_processed = True
        else:
            st.warning("⚠️ No PDF loaded. Please upload a PDF file to start chatting.")
    
    # Instructions
    st.markdown("---")
    st.markdown("""
    **Instructions:**
    1. Upload your lecture notes PDF
    2. Click "Process PDF" 
    3. Ask questions about the content
    4. Get AI-powered answers!
    """)

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

# Main chat interface
st.markdown("### 💬 Chat with your Lecture Notes")

# Check if PDF is ready
if not st.session_state.pdf_processed:
    st.warning("🚨 Please upload and process a PDF file first to start chatting.")
    st.stop()

# Chat input
with st.form("chat_form", clear_on_submit=True):
    user_query = st.text_input(
        "Ask a question about your lecture notes:", 
        key="user_input",
        placeholder="e.g., What are the main concepts in Chapter 1?"
    )
    col1, col2 = st.columns([1, 6])
    with col1:
        submit = st.form_submit_button("🚀 Ask", type="primary")
    with col2:
        clear_history = st.form_submit_button("🗑️ Clear History")

# Clear chat history
if clear_history:
    st.session_state.chat_history = []
    st.rerun()

# Process the user query
if submit and user_query:
    if st.session_state.pdf_processed:
        try:
            with st.spinner("🤖 Thinking..."):
                # Determine PDF path
                pdf_path = None
                if hasattr(st.session_state, 'pdf_name'):
                    pdf_path = getattr(st.session_state, 'current_pdf_path', None)
                
                answer = ask(user_query, pdf_path)
            
            # Save Q&A to history
            st.session_state.chat_history.append(("You", user_query))
            st.session_state.chat_history.append(("Bot", answer))
        except Exception as e:
            st.session_state.chat_history.append(("Bot", f"⚠️ Error: {str(e)}"))
    else:
        st.error("Please upload and process a PDF file first.")

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

