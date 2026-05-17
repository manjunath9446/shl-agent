

from fastapi import (
    FastAPI,
    HTTPException
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

import time

from app.models import (
    ChatRequest,
    ChatResponse
)

from app.agent import (
    run_agent
)

from app.retriever import (
    get_collection
)




# Main FastAPI application
# for SHL conversational agent

app = FastAPI(

    title="SHL Assessment Recommendation Agent",

    description=(
        "Conversational agent for "
        "SHL Individual Test Solutions"
    ),

    version="1.0.0"
)


# CORS


# Enables frontend-backend
# communication during deployment

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_methods=["*"],

    allow_headers=["*"]
)




# Loads ChromaDB assessment
# collection during API startup

@app.on_event("startup")
async def startup_event():

    global chroma_collection

    chroma_collection = get_collection()

    print(
        f"\nLoaded ChromaDB collection with "
        f"{chroma_collection.count()} assessments"
    )




# Verifies backend health
# and assessment availability

@app.get("/health")
async def health():

    return {

        "status": "ok",

        "assessments_loaded":
            chroma_collection.count()
    }


# CHAT ENDPOINT

# Main conversational endpoint
# for SHL recommendation workflow

@app.post(
    "/chat",
    response_model=ChatResponse
)

async def chat(
    request: ChatRequest
):

    start = time.time()

    try:

        # RUN AGENT

        # Executes consultation pipeline:
        # clarification → retrieval →
        # recommendation/refinement

        response = run_agent(
            request
        )

    except Exception as e:

        print("\n=== API ERROR ===")
        print(str(e))

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )

    elapsed = time.time() - start

    # REQUEST LOGGING

    # Logs response latency and
    # recommendation count

    print(
        f"\nRequest handled in "
        f"{elapsed:.2f}s | "
        f"Recs: "
        f"{len(response.recommendations)}"
    )

    return response