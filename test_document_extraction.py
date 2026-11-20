
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from knowledge.models import KnowledgeDocument
from knowledge.services.document_extractor import extract_document_text

documents = KnowledgeDocument.objects.all()

for document in documents:
    print("\n" + "=" * 60)
    print("DOCUMENT:", document.title)
    print("FILE:", document.file.name)

    try:
        extracted_text = extract_document_text(document)

        print("STATUS: SUCCESS")
        print("TOTAL CHARACTERS:", len(extracted_text))
        print("EXTRACTED CONTENT:")
        print(extracted_text[:500])

    except Exception as error:
        print("STATUS: FAILED")
        print("ERROR:", error)
