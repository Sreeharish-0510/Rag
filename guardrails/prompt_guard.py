from langchain.prompts import PromptTemplate

def get_strict_prompt():
    template = """
You are a strict document-based assistant.

Rules:
- Answer ONLY using the provided context.
- Do NOT use prior knowledge.
- If the answer is not in the context, say:
  "I don't know based on the provided document."
- Do NOT guess.

Context:
{context}

Question:
{question}

Answer:
"""
    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )