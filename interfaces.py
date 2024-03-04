from pydantic import BaseModel, Field
from typing import List, Dict
from abc import ABC, abstractmethod
import httpx
import json
from fastapi import HTTPException

class User(BaseModel):
    username: str
    access_level: str

class Query(BaseModel):
    query_text: str
    user: User

class Document(BaseModel):
    title: str
    content: str

# Abstract base class for retrieval system
class RetrievalSystemInterface(ABC):
    @abstractmethod
    def retrieve_documents(self, query: Query) -> List[Document]:
        pass

# Example implementation of the RetrievalSystemInterface using Pydantic models
class SimpleRetrievalSystem(RetrievalSystemInterface):
    def retrieve_documents(self, query: Query) -> List[Document]:
        # Simplified example implementation
        return [Document(title="Doc1", content="Content1"), Document(title="Doc2", content="Content2")]

class ScraperRetrievalSystem(RetrievalSystemInterface):
    def retrieve_documents(self, query: Query) -> List[Document]:
        # Placeholder for a more complex retrieval technique like web scraping
        return [Document(title="Doc3", content="Content3"), Document(title="Doc4", content="Content4")]

class DocsQueryRequest(BaseModel):
    """
    Pydantic model for the query request. For example, a user might send a query like:
    {
        "query": "What are the documents around artifficial intellicence?"
    }
    """
    query: str = Field(..., min_length=1, max_length=2000)

class AskRequest(BaseModel):
    """
    Pydantic model for the ask request. For example, a user might send a question like:
    {
        "question": "What is the capital of France?"
    }
    """
    question: str = Field(..., min_length=1, max_length=2000)

# Abstract base class for vector store interface
class VectorStoreInterface(ABC):
    @abstractmethod
    def retrieve_documents(self, query_text: str, metadata: Dict) -> List[Document]:
        pass

class ChromaDB(VectorStoreInterface):
    def retrieve_documents(self, query_text: str, metadata: Dict) -> List[Document]:
        raise NotImplementedError("ChromaDB interaction not implemented")

class RetrievalAugmentedGeneration:
    def __init__(self, vector_store: VectorStoreInterface):
        self.vector_store = vector_store

    async def retrieve_docs(self, query_text: str, user_metadata: Dict) -> List[Document]:
        documents = await self.vector_store.retrieve_documents(query_text, user_metadata)
        return documents

    async def ask(self, query_text: str, n: int = 500) -> Dict[str, str]:
        async with httpx.AsyncClient() as client:
            # Ensure correct model name and other parameters are included in the JSON payload
            data = {
                "model": "mistral",  # Adjusted model name as per your example
                "messages":[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Hello!"}
                ],
                "stream": False,
                "max_tokens": n
            }
            headers = {"Content-Type": "application/json"}

            # Making the POST request
            response = await client.post(
                "http://localhost:11434/v1/chat/completions",  # Aphrodite server address
                json=data,  # `json=` automatically sets Content-Type to application/json
                headers=headers  # This line is technically redundant here as `json=` does the job
            )
            
            if response.status_code == 200:
                try:
                    response_data = response.json()  # Parse the JSON response
                    # Extract the text from the first choice
                    response_text = response_data["choices"][0]["message"]["content"]
                    return {"response": response_text}
                except ValueError as e:
                    print(f"JSON parsing error: {e}. Response text: '{response.text}'")
                    raise HTTPException(status_code=500, detail="Invalid JSON response from external API.")
            else:
                print(f"Failed external API call. Status: {response.status_code}, Body: {response.text}")
                raise HTTPException(status_code=response.status_code, detail="External API call failed.")