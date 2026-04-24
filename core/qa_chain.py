from langchain_openai import ChatOpenAI
from config import MODEL_NAME, TEMPERATURE

def build_qa_chain(retriever):
    llm = ChatOpenAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )