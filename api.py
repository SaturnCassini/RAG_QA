"""
This file exposes the API endpoints for the retrieval-augmented generation bot.
"""
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from interfaces import ChromaDB, RetrievalAugmentedGeneration, DocsQueryRequest, AskRequest


app = FastAPI()

# Define a list of allowed origins for CORS
# Use ["*"] to allow all origins
allowed_origins = [
    "http://localhost:3000",  # Adjust this to the domain(s) you want to allow
    "https://example.com",
]

# Add CORSMiddleware to the application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

limiter = Limiter(key_func=get_remote_address)

rag = RetrievalAugmentedGeneration(ChromaDB())

@app.post("/retrieve_docs")
@limiter.limit("20/hour")
async def retrieve_documents_endpoint(query_request: DocsQueryRequest, request: Request):
    try:
        user_ip = request.client.host
        documents = await rag.retrieve_docs(query_request.query, {'ip': user_ip})
        return JSONResponse(content={'documents': documents})
    except NotImplementedError as e:
        return JSONResponse(status_code=501, content={"message": str(e)})

@app.post("/ask")
@limiter.limit("20/hour")
async def ask_endpoint(ask_request: AskRequest, request: Request):
    print(ask_request.dict())
    try:
        response = await rag.ask(ask_request.question)
        print(response)
        return JSONResponse(content=response)
    except NotImplementedError as e:
        return JSONResponse(status_code=501, content={"message": str(e)})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"message": e.detail})

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
