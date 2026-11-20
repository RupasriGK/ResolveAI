
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from knowledge.models import KnowledgeDocument
from knowledge.services.document_processor import process_knowledge_document


documents = KnowledgeDocument.objects.all()

print("\nTOTAL DOCUMENTS:", documents.count())

for document in documents:

    print("\n" + "=" * 60)
    print("DOCUMENT:", document.title)
    print("DOCUMENT ID:", document.id)

    try:
        result = process_knowledge_document(document.id)

        print("STATUS: SUCCESS")
        print("DOCUMENT:", result["document_title"])
        print("TOTAL CHUNKS STORED:", result["total_chunks"])

    except Exception as error:
        print("STATUS: FAILED")
        print("ERROR:", error)


print("\n" + "=" * 60)
print("FINAL DOCUMENT STATUS")

for document in KnowledgeDocument.objects.all():
    document.refresh_from_db()

    print(
        document.title,
        "=>",
        document.processing_status
    )
