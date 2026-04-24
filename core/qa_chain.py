from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

def build_qa_chain(retriever):
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever
    )