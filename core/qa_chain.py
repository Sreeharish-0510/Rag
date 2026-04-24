from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from config import MODEL_NAME, TEMPERATURE
from guardrails.prompt_guard import get_strict_prompt

def build_qa_chain(retriever):
    llm = ChatOpenAI(
        model=MODEL_NAME,
        temperature=TEMPERATURE
    )

    prompt = get_strict_prompt()

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain