from pydantic import BaseModel, Field
class ChatRequest(BaseModel):
    sessionId: str = Field(..., description="Unique tracking identifier for conversation session")
    message: str = Field(..., description="The textual string prompt submitted by the end user")
class ChatResponse(BaseModel):
    reply: str
    tokensUsed: int
    retrievedChunks: int
class HealthResponse(BaseModel):
    status: str