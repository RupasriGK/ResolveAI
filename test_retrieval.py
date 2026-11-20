
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from knowledge.services.retriever import retrieve_relevant_chunks


def test_query(question, history=None):

    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("=" * 70)

    results = retrieve_relevant_chunks(
        question=question,
        top_k=5,
        conversation_history=history
    )

    if not results:
        print("No results found.")
        return

    for index, chunk in enumerate(results, start=1):

        print(f"\nRESULT {index}")
        print("Document:", chunk["metadata"]["document_title"])
        print("Chunk:", chunk["metadata"]["chunk_index"])
        print("Distance:", round(chunk["distance"], 4))
        print("Content:", chunk["content"][:300])


# Test 1: AWS question
test_query("What is AWS EC2?")

# Test 2: Wi-Fi question
# test_query("I cannot connect to Wi-Fi. How can I troubleshoot it?")

# Test 3: Contextual follow-up
history = [
    {
        "role": "EMPLOYEE",
        "content": "What is AWS EC2?"
    },
    {
        "role": "AI",
        "content": "AWS EC2 is a virtual server service."
    }
]

# test_query(
#     "What is its main advantage?",
#     history
# )


# test_query(
#     "I cannot connect to Wi-Fi. How can I troubleshoot this problem?"
# )

# test_query(
#     "My laptop is connected to Wi-Fi but there is no internet access. What should I do?"
# )

# test_query(
#     "How can I fix a VPN connection failure?"
# )

test_query(
    "My laptop is connected to Wi-Fi but there is no internet access. What should I do?"
)