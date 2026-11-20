
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from knowledge.services.retriever import retrieve_relevant_chunks
from knowledge.services.answer_generator import generate_answer


questions = [
    "How can I create an EC2 instance in AWS?",
    "What is a VPC and why is it used?",
    "How does a RAG chatbot retrieve information?"
]


for question in questions:

    print("\n" + "=" * 70)
    print("EMPLOYEE QUESTION:")
    print(question)

    try:
        # Step 1: Retrieve relevant knowledge
        retrieved_chunks = retrieve_relevant_chunks(
            question,
            top_k=3
        )

        print("\nRETRIEVED CHUNKS:", len(retrieved_chunks))

        # Step 2: Generate AI answer
        answer = generate_answer(
            question,
            retrieved_chunks
        )

        print("\nITResolve AI RESPONSE:")
        print(answer)

    except Exception as error:
        print("\nERROR:", error)
