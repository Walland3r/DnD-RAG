from langchain_chroma import Chroma
from langchain.schema import Document
from embedding_function import get_function

def encapsulate_id(data_chunks: list[Document]):
    current_page = None
    chunk_number = 0
    for chunk in data_chunks:
        filename = chunk.metadata.get('source', 'unknown')
        page = chunk.metadata.get('page', 'unknown')
        if page != current_page:
            current_page = page
            chunk_number = 0
        chunk.metadata['id'] = f"{filename}-{page}-{chunk_number}"
        chunk_number += 1
    return data_chunks

def add_to_storage(data_chunks: list[Document]):
    vector_store = Chroma(embedding_function=get_function(), persist_directory= 'vector_store')
    existing_items = vector_store.get()
    existing_ids = set(existing_items['ids'])
    
    data_chunks = encapsulate_id(data_chunks)
    new_chunks = []
    for chunk in data_chunks:
         if chunk.metadata['id'] not in existing_ids:
            new_chunks.append(chunk)

    if(len(new_chunks) > 0):
        print(f"Adding {len(new_chunks)} new chunks to the storage.")
        vector_store.add_documents(new_chunks, ids = [chunk.metadata['id'] for chunk in new_chunks])
    else:
        print("No new chunks to add to the storage.")