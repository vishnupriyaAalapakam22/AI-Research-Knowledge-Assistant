from src.document_processor import extract_text_from_pdf
from src.text_chunker import chunk_pages
from src.embedding import create_embeddings
from src.vector_store import store_chunks


def ingest_document(pdf_path, document_name):

    pages = extract_text_from_pdf(pdf_path)

    chunks = chunk_pages(pages)

    embeddings = create_embeddings(chunks)

    store_chunks(
        chunks,
        embeddings,
        document_name
    )

    return len(chunks)