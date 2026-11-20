import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from knowledge.services.vector_store import (
    collection,
    get_collection_count
)

print("STATUS: SUCCESS")
print("COLLECTION:", collection.name)
print("TOTAL STORED CHUNKS:", get_collection_count())