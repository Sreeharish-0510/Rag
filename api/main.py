from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import os, tempfile

from core.loader import load_document
from core.splitter import split_documents
from core.embeddings import get_embeddings
from core.vectorstore import create_vectorstore
from core.retriever import get_retriever
from core.qa_chain import build_qa_chain
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app = FastAPI()

vectorstore = None
retriever = None
qa_chain = None


class QueryRequest(BaseModel):
    question: str


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global vectorstore, retriever, qa_chain

    content = await file.read()

    if not content:
        return {"error": "Empty file received"}

    docs = load_document(file.filename, content)

    chunks = split_documents(docs)
    embeddings = get_embeddings()

    vectorstore = create_vectorstore(chunks, embeddings)
    retriever = get_retriever(vectorstore)
    qa_chain = build_qa_chain(retriever)

    return {"message": "Document processed successfully"}

@app.post("/query")
async def query_rag(req: QueryRequest):
    global qa_chain, retriever

    if not qa_chain:
        return {"answer": "Upload document first"}

    docs = retriever.get_relevant_documents(req.question)

    if not docs:
        return {"answer": "I don't know based on the provided document."}

    answer = qa_chain.run(req.question)

    return {"answer": answer}


@app.get("/")
def root():
    return {"status": "RAG API running"}