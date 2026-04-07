import os
from dotenv import load_dotenv
from pinecone import Pinecone
from services.embeddings import Embedder

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "document-chunks")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX_NAME)


def retrieve_context(query: str, top_k: int = 5) -> str:
    """
    Query Pinecone using user query and return concatenated chunk text.
    """
    try:
        embedder = Embedder()
        embedding = embedder.generate_embeddings([query])[0]
        query_vector = embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)

        result = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )

        chunks = []
        for match in result.get("matches", []):
            metadata = match.get("metadata", {})
            text = metadata.get("text")
            if text:
                chunks.append(text)

        context = "\n\n".join(chunks)
        if not context:
            print(f"WARNING: No context retrieved for query: {query}")
            print(f"Pinecone returned {len(result.get('matches', []))} matches")
            return ""
        
        print(f"Retrieved {len(chunks)} relevant chunks for context")
        return context
    except Exception as e:
        print(f"Error retrieving context from Pinecone: {e}")
        return ""
