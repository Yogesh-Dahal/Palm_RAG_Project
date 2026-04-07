from pydantic import BaseModel
from typing import List


class ChunkRequest(BaseModel):
    chunk_method: str = "fixed"
    chunk_size: int = 500


class ChunkResponse(BaseModel):
    chunks: List[str]
    chunk_method: str
    total_chunks: int


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    total_chunks: int
    model_used: str       