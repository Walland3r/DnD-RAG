"""
D&D Knowledge Base - Main Module

This module configures and initializes the D&D knowledge agent using pydantic-ai and Qdrant.
It provides the core functionality for retrieving D&D information from a vector database.
"""

import os
from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

# Configuration Constants
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/v1")
MODEL_NAME = "qwen3:1.7b"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
COLLECTION_NAME = "handbook"

# System Prompts
MAIN_SYSTEM_PROMPT = """
You are a helpful and knowledgeable assistant that answers questions 
strictly about Dungeons & Dragons 5th Edition rules and lore. You must use the retrieve
tool to obtain all necessary information. Do not rely on your internal knowledge of
D&D; instead, always call retrieve with the user's question and base your answer only
on the retrieved documents.
"""

INTENT_SYSTEM_PROMPT = """
You are a classifier that determines whether a user question is
appropriate and at least loosely related to Dungeons & Dragons.
Don't explain, just answer with tool call.
"""


@dataclass
class Deps:
    client: QdrantClient


def initialize_qdrant_client() -> QdrantClient:
    client = QdrantClient(location=QDRANT_URL)
    client.set_model(EMBEDDING_MODEL)
    client.set_sparse_model("Qdrant/bm25")
    return client


def create_model() -> OpenAIModel:
    return OpenAIModel(
        model_name=MODEL_NAME,
        provider=OpenAIProvider(base_url=OLLAMA_URL),
    )


def initialize_agents(model: OpenAIModel) -> tuple[Agent, Agent]:
    main_agent = Agent(
        model=model,
        deps_type=Deps,
        output_type=str,
        system_prompt=MAIN_SYSTEM_PROMPT,
    )
    
    intents_agent = Agent(
        model=model,
        output_type=bool,
        system_prompt=INTENT_SYSTEM_PROMPT,
    )
    
    return main_agent, intents_agent


# Initialize resources
client = initialize_qdrant_client()
ollama_model = create_model()
main_agent, intents_agent = initialize_agents(ollama_model)


@main_agent.tool
async def retrieve(context: RunContext[Deps], search_query: str) -> str:
    points = context.deps.client.query(
        collection_name=COLLECTION_NAME,
        query_text=search_query,
        limit=10,
    )
    return "\n".join([f"=== {i} ===\n{point.document}\n" for i, point in enumerate(points)])