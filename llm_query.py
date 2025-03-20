"""
This module defines a function `llm_query` that takes a user input string,
searches for relevant context using a vector store, and generates a response
using a language model. The response is based on the context retrieved from
the vector store and formatted using a predefined template.
"""

from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from generate_embeddings import get_function
from ollama import Client


TEMPLATE = """
You are a highly knowledgeable **RPG Game Master Assistant** specializing in **Dungeons & Dragons** rules and mechanics.

**Your Task**
- Answer **only** using the provided context.  
- If the answer is **not in the context**, say: "I don't know based on the given information."  
- Keep responses **clear and concise**.  

**Game Master's Question**  
{question}  

**Relevant Rules & Information**  
{context}  

**Important:** Do not generate information that is not explicitly stated in the context above.
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



