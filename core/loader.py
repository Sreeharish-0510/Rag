import tempfile
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

def load_document(filename, content):
    with tempfile.NamedTemporaryFile(delete=False, suffix=filename) as tmp:
        tmp.write(content)
        tmp.flush()
        path = tmp.name

    if filename.endswith(".pdf"):
        loader = PyPDFLoader(path)
    else:
        loader = Docx2txtLoader(path)

    return loader.load()