from src.retriever import search_documents
from src.rag_generator import generate_answer
from src.summarizer import generate_summary
from src.document_comparator import compare_documents
from src.literature_synthesizer import synthesize_literature


def research_search(
    query,
    top_k=5,
    selected_documents=None
):

    return search_documents(
        query,
        top_k,
        selected_documents
    )


def research_answer(
    query,
    top_k=5,
    selected_documents=None
):

    results = search_documents(
        query,
        top_k,
        selected_documents
    )

    answer = generate_answer(
        query,
        results
    )

    return answer, results


def summarize_document(text):

    return generate_summary(text)


def compare_documents_for_research(
    document_1,
    document_2
):

    return compare_documents(
        document_1,
        document_2
    )


def synthesize_research(documents):

    return synthesize_literature(
        documents
    )