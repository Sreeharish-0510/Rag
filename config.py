MODEL_NAME = "gpt-4.1-nano"   # since you're on Azure nano
TEMPERATURE = 0

CHUNK_SIZE = 500              # 🔽 smaller chunks = better retrieval
CHUNK_OVERLAP = 100

TOP_K = 4                     # 4–5 is ideal
FETCH_K = 12                  # 🔼 larger pool for better recall
LAMBDA_MULT = 0.6             # more diversity