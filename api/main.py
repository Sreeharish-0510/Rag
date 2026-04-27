from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from core.loader import load_document
from core.splitter import split_documents
from core.embeddings import get_embeddings
from core.vectorstore import create_vectorstore
from core.retriever import get_retriever
from core.qa_chain import build_qa_chain

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vectorstore = None
retriever = None
qa_chain = None


class QueryRequest(BaseModel):
    question: str


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global vectorstore, retriever, qa_chain

    content = await file.read()

    docs = load_document(file.filename, content)
    chunks = split_documents(docs)

    embeddings = get_embeddings()
    vectorstore = create_vectorstore(chunks, embeddings)

    retriever = get_retriever(vectorstore)
    qa_chain = build_qa_chain()   

    return {"message": "Document processed successfully"}


@app.post("/query")
async def query_rag(req: QueryRequest):
    global qa_chain, retriever

    if not qa_chain:
        return {"answer": "Upload document first"}

    # 🔹 Step 1: Improve query (important for short questions)
    question = req.question
    if len(question.split()) <= 4:
        question = f"Explain clearly: {question}"

    # 🔹 Step 2: Retrieve docs
    docs = retriever.get_relevant_documents(question)

    if not docs:
        return {"answer": "I don't know based on the document."}

    # 🔹 DEBUG (remove later)
    print("\n--- RETRIEVED DOCS ---")
    for i, d in enumerate(docs):
        print(f"\nDOC {i}:\n{d.page_content[:300]}")

    # 🔹 Step 3: Combine context manually
    context = "\n\n".join([d.page_content for d in docs])

    # 🔹 Step 4: Ask LLM with SAME context
    answer = qa_chain.run({
        "query": question,
        "context": context
    })

    return {"answer": answer}

@app.get("/")
def root():
    return {"status": "running"}