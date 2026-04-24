import streamlit as st

from core.loader import load_document
from core.splitter import split_documents
from core.embeddings import get_embeddings
from core.vectorstore import create_vectorstore
from core.retriever import get_retriever
from core.qa_chain import build_qa_chain
from guardrails.validator import validate_answer

st.set_page_config(page_title="Secure RAG", layout="wide")

st.title("🔐 Secure RAG Chatbot")

# session storage
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
    st.session_state.retriever = None
    st.session_state.docs = None

# upload
uploaded_file = st.file_uploader("Upload PDF or DOCX", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("Processing document..."):
        content = uploaded_file.read()

        docs = load_document(uploaded_file.name, content)
        chunks = split_documents(docs)

        embeddings = get_embeddings()
        vectorstore = create_vectorstore(chunks, embeddings)

        retriever = get_retriever(vectorstore)
        qa_chain = build_qa_chain(retriever)

        st.session_state.qa_chain = qa_chain
        st.session_state.retriever = retriever
        st.session_state.docs = docs

    st.success("Document processed successfully!")

# question input
question = st.text_input("Ask a question from the document")

if question and st.session_state.qa_chain:
    with st.spinner("Thinking..."):
        response = st.session_state.qa_chain.run(question)

        is_valid = validate_answer(response, st.session_state.docs)

        if not is_valid:
            st.error("❌ Answer not found in document (Guardrail active)")
        else:
            st.success(response)