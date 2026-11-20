
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from knowledge.models import KnowledgeDocument
from knowledge.services.document_extractor import extract_document_text
from knowledge.services.text_chunker import split_text_into_chunks


documents = KnowledgeDocument.objects.all()

for document in documents:

    print("\n" + "=" * 60)
    print("DOCUMENT:", document.title)

    try:
        # Extract document text
        extracted_text = extract_document_text(document)

        # Split text into chunks
        chunks = split_text_into_chunks(
            extracted_text,
            chunk_size=1000,
            chunk_overlap=200
        )

        print("TOTAL CHARACTERS:", len(extracted_text))
        print("TOTAL CHUNKS:", len(chunks))

        for index, chunk in enumerate(chunks, start=1):
            print(f"\nCHUNK {index}")
            print("CHARACTERS:", len(chunk))
            print(chunk[:200])

    except Exception as error:
        print("ERROR:", error)
