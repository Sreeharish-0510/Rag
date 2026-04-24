def validate_answer(answer, docs):
    context = " ".join([doc.page_content for doc in docs])

    if answer.lower() not in context.lower():
        return False
    return True