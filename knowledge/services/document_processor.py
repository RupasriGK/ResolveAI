
from django.utils import timezone

from knowledge.models import KnowledgeDocument
from knowledge.services.document_extractor import extract_document_text
from knowledge.services.text_chunker import split_text_into_chunks
from knowledge.services.embedding_service import generate_embeddings
from knowledge.services.vector_store import (
    store_chunks,
    delete_document_chunks,
)


def process_knowledge_document(document_id):
    """
    Extract, chunk, embed and store a Knowledge Base document.
    """

    document = KnowledgeDocument.objects.get(id=document_id)

    try:
        # 1. Mark document as processing
        document.processing_status = (
            KnowledgeDocument.ProcessingStatus.PROCESSING
        )
        document.processing_error = ""

        document.save(
            update_fields=[
                "processing_status",
                "processing_error"
            ]
        )

        # 2. Extract document text
        extracted_text = extract_document_text(document)

        if not extracted_text or not extracted_text.strip():
            raise ValueError("The uploaded document contains no readable text.")

        # 3. Split text into chunks
        chunks = split_text_into_chunks(
            extracted_text,
            chunk_size=1000,
            chunk_overlap=200
        )

        if not chunks:
            raise ValueError("No text chunks were generated.")

        # 4. Generate embeddings in batches
        all_embeddings = []
        batch_size = 32

        for start in range(0, len(chunks), batch_size):

            batch = chunks[start:start + batch_size]

            embeddings = generate_embeddings(
                batch,
                input_type="document"
            )

            if len(embeddings) != len(batch):
                raise ValueError(
                    "Embedding count does not match chunk count."
                )

            all_embeddings.extend(embeddings)

        # 5. Store new vectors
        # ChromaDB upsert uses deterministic IDs, so existing
        # chunk IDs are updated and new chunk IDs are inserted.
        stored_count = store_chunks(
            chunks=chunks,
            embeddings=all_embeddings,
            document_id=document.id,
            document_title=document.title
        )

        # Remove obsolete chunks from an earlier version,
        # but only after the new chunks have been stored.
        delete_document_chunks(
            document.id,
            keep_count=stored_count
        )

        # 6. Mark document as completed
        document.processing_status = (
            KnowledgeDocument.ProcessingStatus.COMPLETED
        )
        document.processing_error = ""
        document.processed_at = timezone.now()

        document.save(
            update_fields=[
                "processing_status",
                "processing_error",
                "processed_at"
            ]
        )

        return {
            "success": True,
            "document_id": str(document.id),
            "document_title": document.title,
            "total_chunks": stored_count
        }

    except Exception as error:

        document.processing_status = (
            KnowledgeDocument.ProcessingStatus.FAILED
        )
        document.processing_error = str(error)

        document.save(
            update_fields=[
                "processing_status",
                "processing_error"
            ]
        )

        raise
