from src.gemini_client import generate_content


def generate_summary(text):

    prompt = f"""
You are an AI research assistant.

Summarize the following research document in a clear,
structured format.

Include:

1. Main Topic
2. Key Objectives
3. Methodology
4. Important Findings
5. Limitations
6. Conclusion

Use only the information provided in the document.
Do not invent information.

Document:
{text}

Summary:
"""

    

    return generate_content(prompt)