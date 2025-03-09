"""
This module defines a function `get_function` that returns an embedding function
using the HuggingFace library. The embedding function is configured to use a
specific model and device (CPU or GPU) and normalizes the embeddings.
"""

from langchain_huggingface import HuggingFaceEmbeddings
from torch.cuda import is_available

MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'
DEVICE = 'cuda' if is_available() else 'cpu'

def get_function():
    model_kwargs = {'device': DEVICE}
    encode_kwargs = {'normalize_embeddings': True}

    embedding_function = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embedding_function