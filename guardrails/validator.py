def validate_answer(answer, docs):
    context = " ".join([doc.page_content for doc in docs])

    return answer.lower() in context.lower()