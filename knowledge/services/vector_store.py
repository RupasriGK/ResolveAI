
import chromadb
from pathlib import Path
from django.conf import settings


# Persistent ChromaDB storage
CHROMA_PATH = Path(settings.BASE_DIR) / "chroma_data"

chroma_client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

# Create or reuse the Knowledge Base collection
collection = chroma_client.get_or_create_collection(
    name="itresolve_knowledge",
    metadata={"hnsw:space": "cosine"}
)


def store_chunks(chunks, embeddings, document_id, document_title):
    """Store text chunks and their embeddings."""

    if not chunks:
        return 0

    if len(chunks) != len(embeddings):
        raise ValueError(
            "Number of chunks and embeddings must match."
        )

    ids = [
        f"{document_id}_chunk_{index}"
        for index in range(len(chunks))
    ]

    metadatas = [
        {
            "document_id": str(document_id),
            "document_title": document_title,
            "chunk_index": index
        }
        for index in range(len(chunks))
    ]

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(chunks)


def get_collection_count():
    """Return the total number of stored chunks."""
    return collection.count()


def delete_document_chunks(document_id, keep_count=None):
    """
    Delete all document chunks or only obsolete chunks.
    """

    if keep_count is None:
        collection.delete(
            where={"document_id": str(document_id)}
        )
        return

    collection.delete(
        where={
            "$and": [
                {"document_id": str(document_id)},
                {"chunk_index": {"$gte": keep_count}}
            ]
        }
    )
