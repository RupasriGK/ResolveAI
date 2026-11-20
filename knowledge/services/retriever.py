
from knowledge.services.embedding_service import generate_embeddings
from knowledge.services.vector_store import collection


# Initial threshold based on retrieval testing.
MAX_DISTANCE = 0.60


def build_contextual_query(question, conversation_history=None):
    """
    Build a meaningful retrieval query using the current
    question and previous employee questions.
    """

    previous_questions = []

    if conversation_history:
        for message in conversation_history:

            if message.get("role") in ["EMPLOYEE", "user"]:

                content = message.get("content", "").strip()

                if content:
                    previous_questions.append(content)

    previous_questions = previous_questions[-3:]

    if previous_questions:
        context = "\n".join(previous_questions)

        return (
            f"Previous employee questions:\n{context}\n\n"
            f"Current employee question:\n{question}"
        )

    return question


def retrieve_relevant_chunks(
    question,
    top_k=5,
    conversation_history=None
):
    """
    Retrieve relevant Knowledge Base chunks using
    contextual embeddings and a distance threshold.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    total_chunks = collection.count()

    if total_chunks == 0:
        return []

    # 1. Build contextual query.
    retrieval_query = build_contextual_query(
        question,
        conversation_history
    )

    # 2. Generate query embedding.
    question_embedding = generate_embeddings(
        [retrieval_query],
        input_type="query"
    )[0]

    # 3. Search ChromaDB.
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, total_chunks),
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    # 4. Filter irrelevant results.
    retrieved_chunks = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for index, content in enumerate(documents):

        distance = distances[index]

        if distance > MAX_DISTANCE:
            continue

        retrieved_chunks.append({
            "content": content,
            "metadata": metadatas[index],
            "distance": distance
        })

    return retrieved_chunks
