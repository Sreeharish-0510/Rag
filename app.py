import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("🔐 Secure RAG Chatbot")

# -------------------
# Upload
# -------------------
uploaded_file = st.file_uploader("Upload PDF", type=["pdf", "docx"])

if uploaded_file:
    file_bytes = uploaded_file.read()

    files = {
        "file": (uploaded_file.name, file_bytes)
    }

    upload_res = requests.post(f"{API_URL}/upload", files=files)

    st.write("Status:", upload_res.status_code)
    st.write("Response:", upload_res.text)

    if upload_res.status_code == 200:
        st.success("✅ Document uploaded")

# -------------------
# Query
# -------------------
query = st.text_input("Ask a question:")

if query:
    query_res = requests.post(
        f"{API_URL}/query",
        json={"question": query}
    )

    if query_res.status_code == 200:
        st.write("### Answer")
        st.write(query_res.json()["answer"])   # ✅ correct here