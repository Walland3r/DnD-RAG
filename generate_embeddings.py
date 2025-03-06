from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

def generate_embeddings(model_name):
    model_kwargs = {'device': 'cuda'}
    encode_kwargs = {'normalize_embeddings': True}

    embedding_function = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embedding_function

def encapsulate_id(data_chunks: list[Document]):
    current_page = None
    chunk_number = 0
    for chunk in data_chunks:
        filename = chunk.metadata.get('filename', 'unknown')
        page = chunk.metadata.get('page', 'unknown')
        if page != current_page:
            current_page = page
            chunk_number = 0
        chunk.metadata['id'] = f"{filename}-{page}-{chunk_number}"
        chunk_number += 1
    return data_chunks

def add_to_storage(data_chunks: list[Document]):
    embedding_function  = generate_embeddings('sentence-transformers/all-MiniLM-L6-v2')
    vector_store = Chroma(embedding_function=embedding_function, persist_directory= 'vector_store')
    existing_items = vector_store.get()
    #existing_ids = set(existing_items['id'])
    
    data_chunks = encapsulate_id(data_chunks)
    print(data_chunks[1].metadata)

    # non_existing_chunk = []
    # for chunk in data_chunks:
    #     if chunk.metadata['id'] not in existing_ids:
    #         non_existing_chunk.append(chunk)
