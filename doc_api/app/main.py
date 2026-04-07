from fastapi import FastAPI
from router import chunk_file, embedd_file, chat
from core.database import init_db

app = FastAPI(title="Document Processing API")


init_db()

app.include_router(chunk_file.router)
app.include_router(embedd_file.router)
app.include_router(chat.router)


@app.get("/")
def read_root():
    return {"message": "Internship task for Palm-Mind Technology"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
