from src.gemini_client import generate_content


def synthesize_literature(documents):

    combined_documents = "\n\n".join(
        f"DOCUMENT {i + 1}:\n{document}"
        for i, document in enumerate(documents)
    )

    prompt = f"""
You are an AI research assistant helping a researcher
understand existing literature.

Analyze the following research documents together.

Create a structured literature synthesis containing:

1. Research Focus
2. Common Approaches
3. Key Findings
4. Differences Between the Studies
5. Limitations
6. Research Gaps
7. Overall Synthesis

Use only the information provided.
Do not invent facts or conclusions.

{combined_documents}

Literature Synthesis:
"""



    return generate_content(prompt)