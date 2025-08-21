
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
    vector_store.persist()
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
    
    # Check if we need to reload the PDF
    if pdf_path != _current_pdf_path or _vector_store is None:
        try:
            docs = load_and_process_pdf(pdf_path)
            _vector_store = create_vector_store(docs, pdf_path)
            _current_pdf_path = pdf_path
        except FileNotFoundError as e:
            return f"Error: {str(e)}. Please upload a PDF file first."
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
    
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
        # Create a temporary file to save the uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name
        
        # Load and process the PDF
        docs = load_and_process_pdf(tmp_path)
        vector_store = create_vector_store(docs, tmp_path)
        
        # Update global variables
        global _vector_store, _current_pdf_path
        _vector_store = vector_store
        _current_pdf_path = tmp_path
        
        return True, "PDF processed successfully!"
    
    except Exception as e:
        return False, f"Error processing PDF: {str(e)}"
    
    finally:
        # Clean up temporary file
        try:
            if 'tmp_path' in locals():
                os.unlink(tmp_path)
        except:
            pass
