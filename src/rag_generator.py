from src.gemini_client import generate_content


def generate_answer(query, search_results):

    context_parts = []

    for i, result in enumerate(search_results, 1):

        context_parts.append(
            f"[SOURCE {i}]\n"
            f"Document: {result['document']}\n"
            f"Page: {result['page']}\n"
            f"Content: {result['text']}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are an AI research assistant.

Answer the user's question using ONLY the information
provided in the research sources below.

IMPORTANT RULES:

1. Do not invent information.
2. If the answer cannot be found in the sources, say:
   "I could not find this information in the provided documents."
3. After each important statement, include the source number
   in this format: [1], [2], etc.
4. Use the source numbers that correspond to the provided sources.
5. Keep the answer clear and concise.

Research Sources:

{context}

User Question:

{query}

Answer:
"""

    return generate_content(prompt)