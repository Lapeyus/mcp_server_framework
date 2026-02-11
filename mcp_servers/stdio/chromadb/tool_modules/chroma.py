import json
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

_embeddings = None
_vector_store = None


def _get_vector_store():
    global _embeddings, _vector_store
    if _vector_store is None:
        _embeddings = OllamaEmbeddings(
            model="nomic-embed-text:latest",
        )
        _vector_store = Chroma(
            collection_name="example_collection",
            embedding_function=_embeddings,  
            persist_directory="./chroma_langchain_db",
        )
    return _vector_store


def retrieve_documents(query: str, k: int = 4) -> str:
    """
    Retrieves documents from the global Chroma vector store based on a query.

    Args:
        query (str): The query string to search for.
        k (int): The number of similar documents to retrieve.

    Returns:
        str: A JSON string representing a list of retrieved documents.
             Each document is a dictionary with 'page_content', 'metadata', and 'id'.
    """
    store = _get_vector_store()

    try:
        retriever = store.as_retriever(search_kwargs={"k": k})
        retrieved_documents = retriever.invoke(query)

        json_compatible_docs = []
        for doc in retrieved_documents:
            json_compatible_docs.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata,
                "id": str(doc.id) if doc.id else None,
            })

        return json.dumps(json_compatible_docs, indent=2)
    except Exception as e:
        print(f"ERROR: Failed to retrieve documents for query '{query}'. Error: {e}")
        return json.dumps([])


if __name__ == "__main__":
    print(retrieve_documents("pip"))
