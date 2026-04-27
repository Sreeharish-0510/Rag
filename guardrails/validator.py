def validate_answer(answer: str, docs: list) -> bool:
    """
    Validates whether the answer is grounded in retrieved documents.

    Rules:
    - Allow "I don't know" responses
    - Check if answer has overlap with context
    - Prevent hallucinated responses
    """

    if not answer:
        return False

    answer_lower = answer.lower()

    # ✅ Allow safe fallback
    if "i don't know" in answer_lower:
        return True

    # ❌ No docs → invalid
    if not docs:
        return False

    # Combine all retrieved context
    context = " ".join([doc.page_content.lower() for doc in docs])

    # Extract meaningful words (ignore short/common words)
    words = [w for w in answer_lower.split() if len(w) > 4]

    if not words:
        return False

    # Count overlap
    match_count = sum(1 for w in words if w in context)

    # ✅ Accept if enough overlap
    return match_count >= 2