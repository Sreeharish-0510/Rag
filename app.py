import streamlit as st

from core.loader import load_document
from core.splitter import split_documents
from core.embeddings import get_embeddings
from core.vectorstore import create_vectorstore
from core.retriever import get_retriever
from core.qa_chain import build_qa_chain
from guardrails.validator import validate_answer
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Secure RAG", layout="wide")

st.title("🔐 Secure RAG Chatbot")

# session storage
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
    st.session_state.retriever = None

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
        qa_chain = build_qa_chain()

        st.session_state.qa_chain = qa_chain
        st.session_state.retriever = retriever

    st.success("Document processed successfully!")

# question input
question = st.text_input("Ask a question from the document")

# ask button
if st.button("Ask"):

    if not question:
        st.warning("Please enter a question")

    elif not st.session_state.qa_chain:
        st.warning("Please upload a document first")

    else:
        with st.spinner("Thinking..."):

            # 🔹 Improve short queries
            if len(question.split()) <= 4:
                question = f"Explain clearly: {question}"

            # 🔹 Retrieve relevant docs
            docs = st.session_state.retriever.get_relevant_documents(question)

            if not docs:
                st.error("I don't know based on the document.")
            else:
                # 🔹 Build context
                context = "\n\n".join([doc.page_content for doc in docs])

                # 🔹 Get answer
                response = st.session_state.qa_chain.run({
                    "context": context,
                    "question": question
                })

                # 🔹 Validate answer
                is_valid = validate_answer(response, docs)

                if not is_valid:
                    st.error("❌ Answer not found in document (Guardrail active)")
                else:
                    st.success(response)