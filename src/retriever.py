from src.embedding import model
from src.vector_store import collection


def search_documents(
    query,
    top_k=3,
    selected_documents=None
):

    query_embedding = model.encode([query])

    search_parameters = {
        "query_embeddings": query_embedding.tolist(),
        "n_results": top_k
    }

    if selected_documents:

        search_parameters["where"] = {
            "document": {
                "$in": selected_documents
            }
        }

    results = collection.query(
        **search_parameters
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    search_results = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        search_results.append({
            "text": document,
            "document": metadata["document"],
            "page": metadata["page"],
            "distance": distance
        })

    return search_results