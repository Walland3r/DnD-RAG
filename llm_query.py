from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from generate_embeddings import get_function
from ollama import Client


TEMPLATE = """
You are an expert RPG game master assistant with deep knowledge of Dungeons & Dragons.  
Answer the questions based **only** on the following context. 
**Game Master asks:** {question}  

**Relevant Rules & Information:**  
{context}  
"""

def llm_query(user_input : str) -> str:
    vector_store = Chroma(persist_directory= 'vector_store', embedding_function=get_function())
    
    search_result = vector_store.similarity_search(user_input)
    context_text = "\n\n".join([doc.page_content for doc in search_result])
    prompt_template = ChatPromptTemplate.from_template(TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=user_input)
    
    client = Client(
    host='http://localhost:11434',
    headers={'x-some-header': 'some-value'}
    )
    response = client.chat(model='hf.co/bartowski/Llama-3.2-3B-Instruct-GGUF:Q6_K_L', messages=[
    {
        'role': 'user',
        'content': prompt,
    },])

    return response['message']['content']



