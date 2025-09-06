import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI

from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

# --- 1. Application Setup ---
app = FastAPI(
    title="Career Advisor API",
    description="API for the One-Stop Personalized Career & Education Advisor",
    version="0.1.0",
)

# --- CORS (Cross-Origin Resource Sharing) Setup ---
# This allows our frontend (running on http://localhost:3000) to communicate with this backend.
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. RAG Pipeline Setup ---

# Load documents from the 'data' directory
try:
    loader = DirectoryLoader('data/', glob="**/*.md", loader_cls=TextLoader, show_progress=True)
    documents = loader.load()
    if not documents:
        print("No documents found. Please check the 'data' directory.")
        documents = []
except Exception as e:
    print(f"Error loading documents: {e}")
    documents = []

# Chunk the documents into smaller pieces
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
texts = text_splitter.split_documents(documents)

# Create embeddings using a sentence transformer model
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Create a Chroma vector store
vectorstore = Chroma.from_documents(texts, embeddings)

# --- LLM Configuration ---
llm = None
if os.getenv("GOOGLE_API_KEY"):
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", convert_system_message_to_human=True)
    except Exception as e:
        print(f"Error initializing Google LLM: {e}")
else:
    print("GOOGLE_API_KEY not found in environment variables. Please create a .env file.")

# Create the Retrieval-Augmented Generation (RAG) chain
qa_chain = None
if llm and vectorstore:
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
        return_source_documents=True
    )
else:
    print("QA chain could not be created. Please check your LLM and vector store setup.")


# --- 3. API Endpoints ---

@app.get("/", tags=["Status"])
def root():
    """A simple endpoint to check if the API is running."""
    return {"status": "online", "message": "Career Advisor API is running."}

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    source_documents: list = []

@app.post("/query", response_model=QueryResponse, tags=["RAG"])
def query_rag(request: QueryRequest):
    """Receives a question, processes it through the RAG chain, and returns the answer."""
    if not qa_chain:
        return {"answer": "Error: QA chain is not initialized. Please check the server logs.", "source_documents": []}
    
    try:
        result = qa_chain({"query": request.question})
        return {
            "answer": result.get("result", "No answer found."),
            "source_documents": result.get("source_documents", [])
        }
    except Exception as e:
        # This will catch potential API errors, e.g., authentication issues
        return {"answer": f"An error occurred with the LLM provider: {e}", "source_documents": []}

# To run this application:
# 1. Make sure you have created the .env file with your GOOGLE_API_KEY.
# 2. In your terminal, navigate to the 'backend' directory.
# 3. Run the command: uvicorn main:app --reload