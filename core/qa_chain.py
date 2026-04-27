from langchain_openai import AzureChatOpenAI
from langchain.chains import LLMChain
from core.prompt import get_strict_prompt
import os

def build_qa_chain():
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        api_version="2024-05-01-preview",
        temperature=0
    )

    prompt = get_strict_prompt()

    return LLMChain(llm=llm, prompt=prompt)