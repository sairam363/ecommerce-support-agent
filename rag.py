import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

# -----------------------------
# Load Markdown Documents
# -----------------------------

documents = []

docs_folder = Path("sample_data/docs")

for file in docs_folder.glob("*.md"):
    text = file.read_text(encoding="utf-8")

    documents.append(
        Document(
            page_content=text,
            metadata={"source": file.name}
        )
    )

# -----------------------------
# Split Documents into Chunks
# -----------------------------

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)

# -----------------------------
# Create Embeddings
# -----------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# Create FAISS Vector Store
# -----------------------------

from pathlib import Path

INDEX_PATH = "faiss_index"

if Path(INDEX_PATH).exists():
    vector_store = FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
else:
    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )
    vector_store.save_local(INDEX_PATH)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

# -----------------------------
# Gemini Model
# -----------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

# -----------------------------
# RAG Function
# -----------------------------

def answer_policy(question: str):

    retrieved_docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in retrieved_docs]
    )

    prompt = f"""
You are an e-commerce customer support assistant.

Answer ONLY using the context below.

If the answer is not present in the context, reply:

"I couldn't find that information in the policy documents."

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    sources = list(
        set(
            doc.metadata["source"]
            for doc in retrieved_docs
        )
    )

    final_answer = response.content

    final_answer += "\n\n📚 Source(s): "

    final_answer += ", ".join(sources)

    return final_answer

def get_llm():
    return llm