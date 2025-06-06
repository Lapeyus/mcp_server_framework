from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
import json

embeddings = OllamaEmbeddings(
        model="nomic-embed-text:latest",
)

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,  
    persist_directory="./chroma_langchain_db",
)

def retrieve_documents(query: str, k: int) -> str: #, filter: dict         filter (dict): A dictionary to filter documents by metadata.
    """
    Retrieves documents from the global Chroma vector store based on a query.

    Args:
        query (str): The query string to search for.
        k (int): The number of similar documents to retrieve.

    Returns:
        str: A JSON string representing a list of retrieved documents.
             Each document is a dictionary with 'page_content', 'metadata', and 'id'.
    """
    global vector_store
    if vector_store is None:
        raise RuntimeError("Vector store not initialized. Call initialize_chroma_db first.")
    
    try:
        retriever = vector_store.as_retriever(search_kwargs={"k": k}) #, "filter": {}
        retrieved_documents = retriever.invoke(query)
        
        # Convert Document objects to a list of dictionaries
        json_compatible_docs = []
        for doc in retrieved_documents:
            json_compatible_docs.append({
                "page_content": doc.page_content,
                "metadata": doc.metadata,
                "id": str(doc.id) if doc.id else None # Ensure ID is string or None
            })
        
        return json.dumps(json_compatible_docs, indent=2) # Return as JSON string
    except Exception as e:
        print(f"ERROR: Failed to retrieve documents for query '{query}'. Error: {e}")
        return json.dumps([]) # Return empty JSON list on error


if __name__ == "__main__":
    # text_splitter = SemanticChunker(
    #     embeddings,
    #     breakpoint_threshold_type="gradient"
    # )
    
    # urls = [
    #     "https://google.github.io/adk-docs/get-started/installation/",
    #     "https://google.github.io/adk-docs/",
    #     "https://google.github.io/adk-docs/get-started/",
    #     "https://google.github.io/adk-docs/get-started/quickstart/",
    #     "https://google.github.io/adk-docs/get-started/streaming/",
    #     "https://google.github.io/adk-docs/get-started/streaming/quickstart-streaming/",
    #     "https://google.github.io/adk-docs/get-started/testing/",
    #     "https://google.github.io/adk-docs/get-started/about/",
    #     "https://google.github.io/adk-docs/tutorials/",
    #     "https://google.github.io/adk-docs/tutorials/agent-team/",
    #     "https://google.github.io/adk-docs/agents/",
    #     "https://google.github.io/adk-docs/agents/llm-agents/",
    #     "https://google.github.io/adk-docs/agents/workflow-agents/",
    #     "https://google.github.io/adk-docs/agents/workflow-agents/sequential-agents/",
    #     "https://google.github.io/adk-docs/agents/workflow-agents/loop-agents/",
    #     "https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/",
    #     "https://google.github.io/adk-docs/agents/custom-agents/",
    #     "https://google.github.io/adk-docs/agents/multi-agents/",
    #     "https://google.github.io/adk-docs/agents/models/",
    #     "https://google.github.io/adk-docs/tools/",
    #     "https://google.github.io/adk-docs/tools/function-tools/",
    #     "https://google.github.io/adk-docs/tools/built-in-tools/",
    #     "https://google.github.io/adk-docs/tools/third-party-tools/",
    #     "https://google.github.io/adk-docs/tools/google-cloud-tools/",
    #     "https://google.github.io/adk-docs/tools/mcp-tools/",
    #     "https://google.github.io/adk-docs/tools/openapi-tools/",
    #     "https://google.github.io/adk-docs/tools/authentication/",
    #     "https://google.github.io/adk-docs/runtime/",
    #     "https://google.github.io/adk-docs/runtime/runconfig/",
    #     "https://google.github.io/adk-docs/deploy/",
    #     "https://google.github.io/adk-docs/deploy/agent-engine/",
    #     "https://google.github.io/adk-docs/deploy/cloud-run/",
    #     "https://google.github.io/adk-docs/deploy/gke/",
    #     "https://google.github.io/adk-docs/sessions/",
    #     "https://google.github.io/adk-docs/sessions/session/",
    #     "https://google.github.io/adk-docs/sessions/state/",
    #     "https://google.github.io/adk-docs/sessions/memory/",
    #     "https://google.github.io/adk-docs/callbacks/",
    #     "https://google.github.io/adk-docs/callbacks/types-of-callbacks/",
    #     "https://google.github.io/adk-docs/callbacks/design-patterns-and-best-practices/",
    #     "https://google.github.io/adk-docs/artifacts/",
    #     "https://google.github.io/adk-docs/events/",
    #     "https://google.github.io/adk-docs/context/",
    #     "https://google.github.io/adk-docs/evaluate/",
    #     "https://google.github.io/adk-docs/mcp/",
    #     "https://google.github.io/adk-docs/streaming/",
    #     "https://google.github.io/adk-docs/streaming/streaming-tools/",
    #     "https://google.github.io/adk-docs/streaming/custom-streaming/",
    #     "https://google.github.io/adk-docs/streaming/custom-streaming-ws/",
    #     "https://google.github.io/adk-docs/streaming/configuration/",
    #     "https://google.github.io/adk-docs/safety/",
    #     "https://google.github.io/adk-docs/community/",
    #     "https://google.github.io/adk-docs/contributing-guide/",
    #     "https://google.github.io/adk-docs/api-reference/",
    #     "https://google.github.io/adk-docs/api-reference/python/" 
    # ]
    # loader = UnstructuredURLLoader(urls=urls)
    # docs = loader.load_and_split(text_splitter) #.load()
    # print(len(docs))




    
    # vector_store.add_documents(documents=docs)
    print(retrieve_documents('pip'))