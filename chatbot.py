
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama
import os
import tempfile
from dotenv import load_dotenv

load_dotenv()

# Set environment variables to suppress warnings
os.environ.setdefault('TF_ENABLE_ONEDNN_OPTS', '0')
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '2')
os.environ.setdefault('PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION', 'python')

# Make HF token optional
hf_token = os.getenv("HF_API_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
if hf_token and hf_token != "your_hugging_face_token_here":
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token

# Global variable to store the current vector store
_vector_store = None
_current_pdf_path = None

# Load the PDF and split it into chunks
def load_and_process_pdf(pdf_path=None):
    if pdf_path is None:
        # Default PDF path
        pdf_path = "ctse_lecture_notes.pdf"
    
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    docs = splitter.split_documents(pages)
    return docs

# Create embeddings and setup Chroma DB
def create_vector_store(docs, pdf_path=None):
    # Create a unique persist directory based on PDF path
    if pdf_path:
        pdf_name = os.path.basename(pdf_path).replace('.pdf', '').replace(' ', '_')
        persist_directory = f"./chroma_db_{pdf_name}"
    else:
        persist_directory = "./chroma_langchain_db"
    
    embeddings = FastEmbedEmbeddings()

    # Always create a fresh vector store for new documents
    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    # Note: Chroma 0.4.x+ automatically persists, no need to call persist()
    return vector_store

# Set up the retriever
def setup_retriever(vector_store):
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 3,
            "score_threshold": 0.5,
        }
    )
    return retriever

# Initialize LLaMA and build the QA chain
def setup_qa_chain(retriever):
    llm = ChatOllama(model="tinyllama")  # Try using a smaller model if available
    qa_chain = RetrievalQA.from_llm(llm=llm, retriever=retriever)
    return qa_chain

# Ask function
def ask(query: str, pdf_path=None):
    global _vector_store, _current_pdf_path
    
    # If no PDF path provided but we have a current vector store, use it
    if pdf_path is None and _vector_store is not None:
        # Use existing vector store
        pass
    # If we need to reload the PDF or no vector store exists
    elif pdf_path != _current_pdf_path or _vector_store is None:
        if pdf_path is None:
            # Try default PDF first
            pdf_path = "ctse_lecture_notes.pdf"
            if not os.path.exists(pdf_path):
                return "Error: No PDF loaded. Please upload a PDF file first."
        
        try:
            docs = load_and_process_pdf(pdf_path)
            _vector_store = create_vector_store(docs, pdf_path)
            _current_pdf_path = pdf_path
        except FileNotFoundError as e:
            return f"Error: {str(e)}. Please upload a PDF file first."
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
    
    # Check if we have a vector store
    if _vector_store is None:
        return "Error: No PDF loaded. Please upload a PDF file first."
    
    retriever = setup_retriever(_vector_store)
    qa_chain = setup_qa_chain(retriever)

    try:
        result = qa_chain.invoke({"query": query})
        answer = result["result"]
        return answer
    except Exception as e:
        return f"Error generating answer: {str(e)}"

# Function to process uploaded PDF from Streamlit
def process_uploaded_pdf(uploaded_file):
    """Process an uploaded PDF file from Streamlit file uploader"""
    try:
        # Create a persistent temporary file to save the uploaded PDF
        import tempfile
        temp_dir = tempfile.gettempdir()
        tmp_path = os.path.join(temp_dir, f"uploaded_pdf_{uploaded_file.name}")
        
        # Save the uploaded file
        with open(tmp_path, "wb") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
        
        # Load and process the PDF
        docs = load_and_process_pdf(tmp_path)
        vector_store = create_vector_store(docs, tmp_path)
        
        # Update global variables
        global _vector_store, _current_pdf_path
        _vector_store = vector_store
        _current_pdf_path = tmp_path
        
        return True, f"PDF '{uploaded_file.name}' processed successfully!"
    
    except Exception as e:
        return False, f"Error processing PDF: {str(e)}"
