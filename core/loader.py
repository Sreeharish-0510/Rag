import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader

def load_document(filename, content):
    _, ext = os.path.splitext(filename)

    file_path = os.path.join(tempfile.gettempdir(), "temp" + ext)

    with open(file_path, "wb") as f:
        f.write(content)

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    else:
        loader = Docx2txtLoader(file_path)

    return loader.load()