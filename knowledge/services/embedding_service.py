
import voyageai
from django.conf import settings


# Initialize Voyage AI client
client = voyageai.Client(
    api_key=settings.VOYAGE_API_KEY
)

EMBEDDING_MODEL = "voyage-4-lite"


def generate_embeddings(texts, input_type="document"):
    """
    Convert a list of text chunks into numerical vectors.

    Args:
        texts: List of text chunks.
        input_type: document or query.

    Returns:
        List of embedding vectors.
    """

    if not texts:
        return []

    if input_type not in ["document", "query"]:
        raise ValueError("input_type must be document or query")

    response = client.embed(
        texts=texts,
        model=EMBEDDING_MODEL,
        input_type=input_type
    )

    return response.embeddings
