import re
from pathlib import Path
from enum import Enum
from typing import List
from pypdf import PdfReader


class Chunkmethod(str, Enum):
    FIXED = "fixed"
    SEMANTIC = "semantic"


class data_processing:
    def __init__(self, file: str):
        self.file_path = Path(file)
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"Please check the {file}, it isn't available")
        
        self.text = self.extract_file()
        
    def extract_file(self) -> str:
        file_type = self.file_path.suffix.lower()
        
        if file_type == ".txt":
            return self.extract_text()
        elif file_type == ".pdf":
            return self.extract_pdf()
        else:
            raise ValueError("File type isn't supported by my system")
        
    def extract_text(self) -> str:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return f.read()
        
    def extract_pdf(self) -> str:
        reader = PdfReader(self.file_path)
        extracted_text = []
        
        for i in reader.pages:
            text = i.extract_text()
            if text:
                extracted_text.append(text)

        return "\n".join(extracted_text)


class Chunking(data_processing):
    def fixed_chunking(self, chunk_size: int) -> List[str]:
        text = self.text
        chunks = []

        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i + chunk_size])

        return chunks
    
    def semantic_chunking(self, max_chunk_size: int = 500) -> list[str]:
        """
        Semantic chunking using paragraphs and sentences.
        """
        text = self.text.strip()
        chunks = []

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        for para in paragraphs:
            if len(para) <= max_chunk_size:
                chunks.append(para)
                continue

            sentences = re.split(r'(?<=[.!?])\s+', para)
            current_chunk = ""

            for sentence in sentences:
                if len(current_chunk) + len(sentence) <= max_chunk_size:
                    current_chunk += " " + sentence
                else:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence

            if current_chunk:
                chunks.append(current_chunk.strip())

        return chunks
