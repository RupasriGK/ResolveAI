
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from knowledge.services.embedding_service import generate_embeddings

texts = [
    "How can I create an EC2 instance in AWS?",
    "How do I reset my Windows password?"
]

try:
    embeddings = generate_embeddings(texts)

    print("STATUS: SUCCESS")
    print("TOTAL EMBEDDINGS:", len(embeddings))
    print("VECTOR DIMENSIONS:", len(embeddings[0]))
    print("FIRST 5 VALUES:", embeddings[0][:5])

except Exception as error:
    print("STATUS: FAILED")
    print("ERROR:", error)
