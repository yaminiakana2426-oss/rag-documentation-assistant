import os
from dotenv import load_dotenv  # <-- Add this line
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
load_dotenv()
from app.routes import chat
from app.models.schemas import HealthResponse
from app.vectorstore.database import vector_db

app = FastAPI(title="TRUEAILAB Production RAG Core Engines")

@app.on_event("startup")
def startup_event():
    docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../docs.json"))
    vector_db.initialize_store(docs_path)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"Unhandled Production Runtime Exception: {str(exc)}"}
    )

@app.get("/health", response_model=HealthResponse)
async def system_health_status():
    return HealthResponse(status="healthy")

app.include_router(chat.router, prefix="/api")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")