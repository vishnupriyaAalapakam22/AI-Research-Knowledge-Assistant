from src.gemini_client import generate_content


def compare_documents(document_1, document_2):

    prompt = f"""
You are an AI research assistant.

Compare the following two research documents.

Compare them using these categories:

1. Main Topic
2. Objectives
3. Methodology
4. Dataset
5. Results / Findings
6. Limitations
7. Similarities
8. Differences
9. Overall Comparison

Use only the information provided.
Do not invent information.

If information is missing, say "Not mentioned".

DOCUMENT 1:
{document_1}

DOCUMENT 2:
{document_2}

Comparison:
"""

    return generate_content(prompt)