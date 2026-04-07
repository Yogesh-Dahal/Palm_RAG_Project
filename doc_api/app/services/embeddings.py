from typing import List
from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, model_name: str="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()
        
    def _load_model(self):
        try:
            print(f"Loading the embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            print(f"Successfully loaded the model {self.model_name}")
        except Exception as e:
            print(f"Error in loading the model {self.model_name}: {e}")
            raise
        
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not self.model:
            raise ValueError("Model is not loaded")
        
        print(f"Generating embeddings for {len(texts)} texts...")
        embeddings = self.model.encode(texts, convert_to_numpy=False)
        print(f"Generated embeddings with {len(embeddings)} vectors")
        
        return embeddings.tolist() if hasattr(embeddings, 'tolist') else embeddings