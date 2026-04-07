# Document Processing & Conversational RAG API

A production-ready backend system implementing document ingestion and a custom conversational RAG pipeline, built using **FastAPI**, **LangGraph**, **LLMs**, **Pinecone**, **Redis**, and **PostgreSQL**.

This project satisfies all requirements specified by Palm Mind Technology and follows clean, modular, and scalable backend architecture.

## Features

### 1. Document Ingestion API
- Upload `.pdf` and `.txt` files
- Text extraction and processing
- Two selectable chunking strategies:
  - **Fixed-size chunking** - Splits documents into fixed chunks
  - **Semantic chunking** - Intelligent content-based splitting
- Embedding generation using `all-MiniLM-L6-v2` model
- Vector storage in **Pinecone**
- Metadata persistence in **PostgreSQL**

### 2. Conversational RAG API
- **Custom RAG implementation** (no RetrievalQAChain)
- Manual retrieval + context injection
- Multi-turn conversation handling
- **Redis-based chat memory** with session support
- LLM-driven response generation with context awareness
- Intent-based routing via LangGraph

### 3. Interview Booking via LLM
- LLM detects booking intent from natural language
- Extracts structured data: **Name**, **Email**, **Date**, **Time**
- Stores booking information in **PostgreSQL**
- Seamlessly integrated into conversation flow

## Architecture

```
User Request
    ↓
FastAPI Endpoint
    ↓
LangGraph Workflow
    ├─→ Intent Node (Classify: QA or Booking)
    │
    ├─→ QA Path:
    │   ├─ Retrieve context from Pinecone
    │   ├─ Get chat history from Redis
    │   └─ Generate answer via LLM
    │
    └─→ Booking Path:
        ├─ Extract details from conversation
        ├─ Validate completeness
        └─ Save to PostgreSQL
    ↓
Return Response + Update Memory
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| API Framework | FastAPI |
| Language | Python 3.10+ |
| Workflow Orchestration | LangGraph |
| LLM Provider | Xiomi (via Openrouter) |
| Embeddings | Sentence-Transformers (all-MiniLM-L6-v2) |
| Vector Database | Pinecone |
| Chat Memory | Redis |
| SQL Database | PostgreSQL |
| File Parsing | PyPDF2 |
| Validation | Pydantic |

## Project Structure

```
doc_api/
├── app/
│   ├── main.py                    # FastAPI app entry point
│   ├── router/
│   │   ├── chat.py               # Chat & booking endpoint
│   │   ├── chunk_file.py         # Document chunking endpoints
│   │   └── embedd_file.py        # Embedding generation endpoint
│   ├── graph/
│   │   ├── graph.py              # LangGraph workflow definition
│   │   ├── nodes.py              # Intent, RAG, Booking nodes
│   │   └── state.py              # Graph state definition
│   ├── services/
│   │   ├── ai_services.py        # LLM client setup
│   │   ├── chunker.py            # Chunking strategies
│   │   ├── embeddings.py         # Embedding model wrapper
│   │   ├── pincone.py            # Pinecone vector retrieval
│   │   ├── redis.py              # Redis chat memory
│   │   └── data_process.py       # Data processing utilities
│   ├── schema/
│   │   ├── models.py             # SQLAlchemy ORM models
│   │   ├── chat_schema.py        # Pydantic request/response schemas
│   │   └── save_to_db.py         # Database persistence functions
│   ├── core/
│   │   └── database.py           # PostgreSQL configuration
│   ├── prompts/
│   │   └── prompts.py            # LLM prompt templates
│   └── data/
│       └── data.txt              # Sample data
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
└── README.md                      # Documentation
```

## Constraints Compliance

- No FAISS
- No Chroma
- No UI (Backend only)
- No RetrievalQAChain (custom implementation)
- Clean modular architecture
- Typed Python + Pydantic
- Industry-standard REST API structure

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/HimamshuBhattarai/Palm-Mind.git
cd doc_api
```

### 2. Create Virtual Environment
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```

Add the following to `.env`:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/doc_api

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Pinecone
PINECONE_API_KEY=your_api_key
PINECONE_INDEX_NAME=document-chunks

# OpenAI
OPENROUTER_API=sk-...
```

### 5. Run Server
```bash
cd app
uvicorn main:app --reload
```

Server will be available at: **http://127.0.0.1:8000**

## API Endpoints

### Document Chunking

#### Fixed-size Chunking
```bash
POST /data/chunker/fixed
Content-Type: multipart/form-data

Parameters:
- file: .txt or .pdf file
- chunk_size: integer (default: 500)
```

#### Semantic Chunking
```bash
POST /data/chunker/semantic
Content-Type: multipart/form-data

Parameters:
- file: .txt or .pdf file
```

### Embeddings

```bash
POST /embedd/embedder
# Generates and stores embeddings for the last chunked document
```

### Conversational Chat

```bash
POST /chat
Content-Type: application/json

Body:
{
  "session_id": "user123",
  "query": "What is in the document?"
}

Response (QA):
{
  "answer": "...",
  "status": "answered"
}

Response (Booking):
{
  "message": "Your interview has been booked successfully!",
  "status": "booked",
  "booking_id": 1,
  "booking_details": {
    "id": 1,
    "name": "John",
    "email": "john@example.com",
    "date": "2025-01-15",
    "time": "14:00",
    "created_at": "2025-01-05T10:30:00"
  }
}
```

## Testing

### Swagger UI
Visit: **http://127.0.0.1:8000/docs**

### Redis Inspection
```bash
redis-cli
KEYS chat:*
LRANGE chat:session_id 0 -1
```

### Vector Database
Check Pinecone dashboard for stored vectors and metadata

### Example Flow

**1. Upload Document**
```bash
POST /data/chunker/semantic
Upload: document.txt
```

**2. Generate Embeddings**
```bash
POST /embedd/embedder
```

**3. Chat with Memory**
```bash
POST /chat
{
  "session_id": "test123",
  "query": "What information do I need to provide for booking?"
}
```

**4. Book Interview**
```bash
POST /chat
{
  "session_id": "test123",
  "query": "I want to book for John Doe, john@email.com, January 20 at 2 PM"
}
```

## Custom RAG Flow

1. **User Query** → FastAPI endpoint receives request
2. **Classify Intent** → LangGraph intent node determines QA or Booking
3. **Retrieve Memory** → Load chat history from Redis
4. **Generate Embedding** → Convert query to vector using Sentence-Transformers
5. **Vector Search** → Find relevant chunks in Pinecone
6. **Build Context** → Concatenate retrieved chunks
7. **Generate Response** → LLM generates answer with context + history
8. **Save to Memory** → Store user query and response in Redis
9. **Return Response** → Send answer or booking confirmation

## Database Schema

### Metadata Table (Documents)
```sql
CREATE TABLE datas.metadata (
  id SERIAL PRIMARY KEY,
  document_name VARCHAR(255),
  document_type VARCHAR(100),
  chunk_method VARCHAR(50),
  chunk_size INTEGER,
  uploaded_at TIMESTAMP DEFAULT now()
);
```

### Booking Table
```sql
CREATE TABLE datas.booking (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255),
  date DATE,
  time VARCHAR(5),
  created_at TIMESTAMP DEFAULT now(),
  updated_at TIMESTAMP DEFAULT now()
);
```

## Multi-turn Conversation Example

**Turn 1:**
```json
POST /chat
{
  "session_id": "user123",
  "query": "What is machine learning?"
}
→ Response: "Machine learning is..."
```

**Turn 2 (same session):**
```json
POST /chat
{
  "session_id": "user123",
  "query": "Explain it more simply"
}
→ Response: Uses previous context + history
```

Redis stores all messages with session context.

## Future Enhancements

- Role-based access control (RBAC)
- Document versioning and history
- Streaming LLM responses
- Observability with structured logging
- Rate limiting and authentication
- Batch document processing

## Author

**Yogesh Dahal**
