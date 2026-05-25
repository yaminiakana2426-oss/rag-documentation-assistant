import os
from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.vectorstore.database import vector_db
from google import genai

router = APIRouter()

# Initialize the Gemini Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@router.post("/chat")
async def chat_endpoint(payload: ChatRequest):
    try:
        # 1. Search our local FAISS index for relevant documents
        context_docs = vector_db.search_similarity(payload.message, top_k=3)
        
        # 2. Extract and format the text fields cleanly
        if context_docs:
            context_text = "\n".join([f"- {doc['text']}" for doc in context_docs])
        else:
            context_text = "No direct documentation chunks matched this query inside the FAISS index database."

        # 3. Build the prompt
        system_prompt = f"""
        You are a highly capable technical support agent for TRUEAILAB. 
        Your task is to answer the user's question using the custom documentation context provided below.
        
        If the context directly or indirectly answers the question, summarize it beautifully and concisely.
        If the question is completely unrelated to the documentation (like general knowledge trivia), 
        just answer it politely using your general knowledge, but mention that it isn't in our local database.

        Custom Laboratory Context:
        {context_text}

        User's Question: {payload.message}
        """

        # 4. Generate the response using your active gemini-2.5-flash engine
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=system_prompt
        )
        
        # CHANGED HERE: We now use "reply" instead of "response" to match your app.js!
        return {"reply": response.text.strip()}

    except Exception as e:
        print(f"CRITICAL ERROR IN CHAT ROUTE: {str(e)}")
        # CHANGED HERE: Provide "error" as a fallback so the UI can display it if something fails
        return {"error": f"Internal Server Error: {str(e)}"}