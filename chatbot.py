
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import FastEmbedEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from langchain_community.chat_models import ChatOllama
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import os
from dotenv import load_dotenv

load_dotenv()


hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if hf_token is None:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN is not set in environment variables")
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token


# Load the PDF and split it into chunks
def load_and_process_pdf():
    loader = PyPDFLoader("ctse_lecture_notes.pdf")  # Ensure correct path
    pages = loader.load_and_split()
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)  # Reduce chunk size
    docs = splitter.split_documents(pages)
    return docs

# Create embeddings and setup Chroma DB
def create_vector_store(docs):
    persist_directory = "./chroma_langchain_db"
    embeddings = FastEmbedEmbeddings()

    if os.path.exists(persist_directory):
        vector_store = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    else:
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
def ask(query: str):
    docs = load_and_process_pdf()
    vector_store = create_vector_store(docs)
    retriever = setup_retriever(vector_store)
    qa_chain = setup_qa_chain(retriever)

    result = qa_chain.invoke({"query": query})
    answer = result["result"]
    return answer
