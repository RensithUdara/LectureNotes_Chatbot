# 📘 Lecture Notes Chatbot

An intelligent chatbot powered by LLaMA3 and LangChain that allows you to upload PDF lecture notes and ask questions about the content.

## 🚀 Features

- **PDF Upload**: Upload any PDF lecture notes through the web interface
- **AI-Powered Q&A**: Ask questions and get intelligent answers from your documents
- **Modern UI**: Clean, responsive Streamlit interface with chat bubbles
- **Local Processing**: All processing happens locally with Ollama
- **Persistent Storage**: Vector embeddings are stored for efficient retrieval

## 📋 Prerequisites

Before running the project, make sure you have:

1. **Python 3.8+** installed
2. **Ollama** installed on your system
3. **Git** (for cloning the repository)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd LectureNotes_Chatbot-LLM-main
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Ollama
**Windows:**
```bash
winget install Ollama.Ollama
```

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 4. Download the AI Model
```bash
ollama pull tinyllama
```

### 5. Set Up Environment Variables (Optional)
Create a `.env` file in the project root:
```env
# Hugging Face API Token (optional)
HF_API_TOKEN=your_hugging_face_token_here

# Ollama Configuration (optional)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=tinyllama
```

## 🖥️ Running the Application

1. **Start the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and go to: `http://localhost:8501`

3. **Upload a PDF:**
   - Use the sidebar to upload your lecture notes PDF
   - Click "Process PDF" to analyze the document
   - Wait for the "PDF Ready" confirmation

4. **Start Chatting:**
   - Ask questions about your lecture notes
   - Get AI-powered answers instantly
   - View your chat history in the main area

## 📁 Project Structure

```
LectureNotes_Chatbot/
├── app.py                 # Main Streamlit application
├── chatbot.py            # Core chatbot logic and PDF processing
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create this)
├── flan-t5/             # Jupyter notebooks (FLAN-T5 model)
├── LLama3/              # Jupyter notebooks (LLaMA3 model)
└── chroma_db_*/         # Vector database storage (auto-created)
```

## 💡 Usage Tips

- **PDF Quality**: Ensure your PDF has readable text (not just images)
- **Question Format**: Ask specific questions about the content
- **Multiple PDFs**: Upload different PDFs to switch between documents
- **Chat History**: Use "Clear History" to start fresh conversations

## 🔧 Troubleshooting

### Common Issues:

1. **Ollama Connection Error:**
   ```bash
   ollama serve  # Start Ollama service manually
   ```

2. **PDF Processing Error:**
   - Ensure PDF is text-based (not scanned images)
   - Check file size (very large files may take time)

3. **Import Errors:**
   ```bash
   pip install --upgrade langchain langchain-community
   ```

4. **Memory Issues:**
   - Use smaller PDF files
   - Restart the application

## 🔮 Features Coming Soon

- [ ] Support for multiple document formats (DOCX, TXT)
- [ ] Conversation memory across sessions
- [ ] Export chat history
- [ ] Advanced search filters
- [ ] Multiple AI model options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **LangChain** for the RAG framework
- **Ollama** for local AI model hosting
- **Streamlit** for the web interface
- **LLaMA3** for the language model

---

**Happy Learning! 🎓**
