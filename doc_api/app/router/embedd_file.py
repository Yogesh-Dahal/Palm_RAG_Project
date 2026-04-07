from services.embeddings import Embedder
from services.data_process import EmbeddingResponse
from fastapi import APIRouter, HTTPException
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
from schema.save_to_db import save_to_db
from core.database import session_local
import pandas as pd

load_dotenv()

router = APIRouter(prefix="/embedd", tags=["Embeddings"])

last_chunks = []
embedder = None
pinecone_client = None
last_file_metadata = None


def set_last_chunks(chunks: list):
    global last_chunks
    last_chunks = chunks


def set_last_file_metadata(filename: str, file_type: str, chunk_method: str, chunk_size: int):
    global last_file_metadata
    last_file_metadata = {
        "document_name": filename,
        "document_type": file_type,
        "chunk_method": chunk_method,
        "chunk_size": chunk_size
    }


def init_pinecone():
    """Initialize Pinecone client"""
    global pinecone_client
    try:
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable not set")
        
        pinecone_client = Pinecone(api_key=api_key)
        print("Pinecone client initialized successfully")
    except Exception as e:
        print(f"Error initializing Pinecone: {e}")
        raise


def get_or_create_index(index_name: str = "document-chunks"):
    """Get or create a Pinecone index"""
    try:
        if pinecone_client is None:
            init_pinecone()
        
        indexes = pinecone_client.list_indexes()
        if index_name not in indexes.names():
            print(f"Creating index: {index_name}")
            pinecone_client.create_index(
                name=index_name,
                dimension=384,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
        
        return pinecone_client.Index(index_name)
    except Exception as e:
        print(f"Error getting/creating index: {e}")
        raise


@router.post("/embedder", response_model=EmbeddingResponse)
async def embed_chunks():
    """
    Generate embeddings for the most recent chunked file and store in PineconeDB.
    No parameters required - uses the last file that was chunked.
    """
    global embedder
    
    try:
        if not last_chunks:
            raise HTTPException(status_code=400, detail="No chunks available. Please chunk a file first.")
        
        # Validate chunks - filter out empty strings
        valid_chunks = [chunk for chunk in last_chunks if chunk and isinstance(chunk, str)]
        if not valid_chunks:
            raise HTTPException(status_code=400, detail="Chunks are empty or invalid.")
        
        print(f"Starting embedding process for {len(valid_chunks)} valid chunks out of {len(last_chunks)}")

        if embedder is None:
            embedder = Embedder()
        
        embeddings = embedder.generate_embeddings(valid_chunks)
        
        if not embeddings or len(embeddings) != len(valid_chunks):
            raise HTTPException(status_code=500, detail="Embedding generation failed or mismatch in count.")
        
        index = get_or_create_index()
        
        vectors_to_upsert = []
        for i, (chunk, embedding) in enumerate(zip(valid_chunks, embeddings)):
            # Ensure embedding is always a list
            embedding_list = embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)
            vectors_to_upsert.append({
                "id": f"chunk_{i}",
                "values": embedding_list,
                "metadata": {"text": chunk, "chunk_index": i}
            })
        
        print(f"Upserting {len(vectors_to_upsert)} vectors to Pinecone")
        index.upsert(vectors=vectors_to_upsert)
        print(f"Successfully stored {len(vectors_to_upsert)} embeddings in Pinecone")
        
        # Save metadata to database
        if last_file_metadata:
            db = session_local()
            try:
                df = pd.DataFrame([last_file_metadata])
                save_to_db(df, db)
                print(f"Successfully saved metadata for {last_file_metadata['document_name']} to database")
            except Exception as e:
                print(f"Error saving to database: {e}")
                raise HTTPException(status_code=500, detail=f"Error saving to database: {str(e)}")
            finally:
                db.close()
        
        return EmbeddingResponse(
            embeddings=embeddings,
            total_chunks=len(last_chunks),
            model_used="all-MiniLM-L6-v2"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating embeddings: {str(e)}")
