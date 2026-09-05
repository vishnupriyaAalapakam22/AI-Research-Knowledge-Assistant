import chromadb


client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="research_documents"
)


def store_chunks(chunks, embeddings, document_name):

    # Remove previous version of the same document
    try:

        collection.delete(
            where={
                "document": document_name
            }
        )

    except Exception:
        pass

    for i, (chunk, embedding) in enumerate(
        zip(chunks, embeddings)
    ):

        chunk_id = f"{document_name}_{i}"

        collection.add(
            ids=[chunk_id],
            documents=[chunk["text"]],
            embeddings=[embedding.tolist()],
            metadatas=[
                {
                    "document": document_name,
                    "page": chunk["page"]
                }
            ]
        )


def get_document_names():

    results = collection.get(
        include=["metadatas"]
    )

    documents = set()

    for metadata in results["metadatas"]:

        documents.add(
            metadata["document"]
        )

    return sorted(documents)