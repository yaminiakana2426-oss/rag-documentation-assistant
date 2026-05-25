# TRUEAILAB Knowledge Base - RAG Assistant

A Retrieval-Augmented Generation (RAG) assistant designed to ingest local system documentation, build a local vector index using FAISS, and serve an interactive chat interface to answer user queries with high-accuracy contextual grounding.

---

## 🚀 Architecture Diagram & Component Overview

The application utilizes a clean, modular multi-tier architecture to decouple document preprocessing, vector search orchestration, and generative LLM integration.

+-------------------------------------------------------------+
|                        Frontend UI                          |
|                 (HTML5 / Vanilla CSS3 / JS)                  |
+------------------------------+------------------------------+
| (REST API / JSON Payload)
v
+-------------------------------------------------------------+
|                     FastAPI Backend Server                  |
|                 (app.main / app.routes.chat)                |
+------------------------------+------------------------------+
|
+----------------------+----------------------+
| (Vector Retrieval)                          | (LLM Context Augmentation)
v                                             v
+-----------------------+                    +-----------------------+
|  FAISS Vector Index   |                    |   Google Gemini API   |
| (IndexFlatIP Matrix)  |                    |   (gemini-2.5-flash)  |
+-----------------------+                    +-----------------------+


### Component Details
* **Frontend User Interface:** A minimalist dashboard built with semantic HTML5 and vanilla JavaScript. It manages application state, maintains an ongoing session tracking identifier (`sessionId`), handles real-time visual message bubble insertion, and executes non-blocking asynchronous REST requests (`fetch`).
* **FastAPI Backend Web Framework:** Serves as the centralized routing hub (`/api/chat`). It orchestrates data flow, maps incoming requests to JSON schemas using Pydantic validation, routes structural texts to the data processing layers, and serves static frontend assets.
* **Vector Database (FAISS Index):** Runs an in-memory `IndexFlatIP` (Inner Product) structural layout. It stores high-dimensional documentation coordinates natively, executing mathematical matrix lookups instantly without disk latency.
* **Google GenAI Client SDK:** Integrates remote cloud endpoints directly into local routes to generate vectors via `gemini-embedding-001` and run structural context completion prompts using the high-speed `gemini-2.5-flash` model.

---

## 🔄 RAG Workflow Explanation

The engine uses a sequential pipeline that balances proactive document ingestion at startup with real-time semantic retrieval at query execution.

[ Ingestion Pipeline (Application Startup) ]
docs.json ---> Chunks Matrix Extraction ---> Gemini Embedding Service ---> FAISS Index Add Matrix

[ Query Pipeline (Real-Time Generation) ]
User Query ---> Gemini Embed-001 Vector ---> FAISS Similarity Search ---> Filter Matches (>=0.10)
|
User Query + Matching Text Snippets <--- Gemini-2.5-Flash Synthesis <--- Context Injection Block


1. **Ingestion & Serialization Pipeline (Application Startup Event):** When FastAPI fires up, an asynchronous lifecycle handler loads the raw structural data (`docs.json`). The code unpacks the source dictionary items into a flat list of text chunks. Each structural snippet is packed into an atomic dictionary with its corresponding `title`.
2. **Query Preprocessing & Semantic Transition:** When a user types a message and clicks "Send", the raw string goes straight to the backend router. The string is fed to the remote embedding endpoint to output a numeric vector representing the message's core meaning.
3. **FAISS Database Lookups & Distance Computation:** The resulting vector is immediately evaluated against the pre-loaded FAISS index matrix using dot-product vector multiplication.
4. **Prompt Contextualization & Generative Synthesis:** The extracted data matches are compiled into a structural array and formatted as a custom Markdown block. This text block is combined with the original question and systemic role constraints into an augmented prompt, which is sent to `gemini-2.5-flash` for final answer generation.

---

## 🧠 Core System Design & Engineering Reasoning

### 1. Embedding Strategy
* **Model Selection:** Utilizes Google's production **`gemini-embedding-001`** model via the modern `google-genai` SDK.
* **Dimensional Footprint:** This engine maps textual items into a **3072-dimension** vector space. This high dimensionality captures complex technical contexts, ensuring semantic nuances are properly preserved.
* **Batching Performance:** The system maps multiple data rows during application boot via `batchEmbedContents` calls, significantly reducing startup network overhead.

### 2. Similarity Search Logic
* **Algorithm Matrix:** Uses **`faiss.IndexFlatIP`** (Inner Product / Cosine Similarity on normalized vectors). This is ideal for measuring directional alignment between search queries and documentation context.
* **Dynamic Threshold Filtering:** The similarity search threshold is configured to **`0.10`**. Because 3072-dimensional space spreads statistical vectors across broad ranges, this configuration ensures relevant information is captured without introducing noise or unrelated database blocks.
* **Boundary Enforcement:** If the vector lookup yields zero matches above the threshold metric, the search manager safely returns an empty list, allowing the system to fall back gracefully.

### 3. Prompt Design Reasoning
The system prompt explicitly casts the LLM into a specific, structured role:
* **Role Constraint:** Defines the model as a *"highly capable technical support agent for TRUEAILAB."*
* **Context Prioritization:** Instructs the model to heavily prioritize the *Custom Laboratory Context* section when formulating answers.
* **Adaptive Intelligence Rules:** Rather than blocking general queries with a rigid error message, it utilizes a dual-path design. If a question falls outside the local database (e.g., general knowledge), the model provides a helpful response using its pre-trained weights while transparently adding a disclosure note: *"This information is not found in our TRUEAILAB local database."*

---

## 🛠️ Step-by-Step Setup Instructions

Follow these instructions to configure and run the application locally.

### 📋 Prerequisites
Ensure you have **Python 3.12+** installed on your workstation.

### ⚙️ Installation & Configuration

1. Navigate to your project directory:
   ```bash
   cd "C:\Users\DELL\OneDrive\Desktop\rag assistant"
Install the necessary system dependencies:

Bash


pip install fastapi uvicorn google-genai faiss-cpu numpy pydantic
Set up your Gemini API Key as an environment variable in your terminal session:

PowerShell (VS Code Default):

PowerShell


$env:GEMINI_API_KEY="your_actual_api_key_here"
Command Prompt (CMD):

DOS


set GEMINI_API_KEY=your_actual_api_key_here
⚡ Launching the Application
Start the local Uvicorn development server on an open port (using port 8002 to avoid any background Windows socket conflicts):

Bash


python -m uvicorn app.main:app --port 8002
Once the terminal outputs INFO: Application startup complete., open your web browser and go to:

Plaintext


[http://127.0.0.1:8002](http://127.0.0.1:8002)