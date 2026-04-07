from pathlib import Path
from services.chunker import Chunking
from services.data_process import ChunkResponse
from fastapi import APIRouter, UploadFile, File, HTTPException
from router import embedd_file


router = APIRouter(prefix="/data", tags=["Document Processing"])


@router.post("/chunker/fixed", response_model=ChunkResponse)
async def chunk_file_fixed(file: UploadFile = File(...), chunk_size: int = 500):
    """
    Upload a file and chunk it using fixed-size chunking.
    Supported formats: .txt, .pdf
    """
    try:
        file_path = Path(f"temp_{file.filename}")
        contents = await file.read()
        file_path.write_bytes(contents)
        
        chunker = Chunking(str(file_path))
        
        chunks = chunker.fixed_chunking(chunk_size)
        
        embedd_file.set_last_chunks(chunks)
        embedd_file.set_last_file_metadata(
            filename=file.filename,
            file_type=file.filename.split('.')[-1].lower(),
            chunk_method="fixed",
            chunk_size=chunk_size
        )
        
        file_path.unlink()
        
        return ChunkResponse(
            chunks=chunks,
            chunk_method="fixed",
            total_chunks=len(chunks)
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/chunker/semantic", response_model=ChunkResponse)
async def chunk_file_semantic(file: UploadFile = File(...)):
    """
    Upload a file and chunk it using semantic chunking.
    Supported formats: .txt, .pdf
    """
    try:
        file_path = Path(f"temp_{file.filename}")
        contents = await file.read()
        file_path.write_bytes(contents)
        
        chunker = Chunking(str(file_path))
        
        chunks = chunker.semantic_chunking()
        
        # Store chunks for embedding
        embedd_file.set_last_chunks(chunks)
        embedd_file.set_last_file_metadata(
            filename=file.filename,
            file_type=file.filename.split('.')[-1].lower(),
            chunk_method="semantic",
            chunk_size=len(chunks)
        )
        
        file_path.unlink()
        
        return ChunkResponse(
            chunks=chunks,
            chunk_method="semantic",
            total_chunks=len(chunks)
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
