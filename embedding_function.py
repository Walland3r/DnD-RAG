from langchain_huggingface import HuggingFaceEmbeddings

MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

def get_function():
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': True}

    embedding_function = HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embedding_function