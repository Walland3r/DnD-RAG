from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from generate_embeddings import get_function

TEMPLATE = """
You are an expert RPG game master assistant with deep knowledge of Dungeons & Dragons.  
Answer the questions based **only** on the following context. 
**Game Master asks:** {question}  

**Relevant Rules & Information:**  
{context}  
"""

def llm_query(user_input : str):
    vector_store = Chroma(persist_directory= 'vector_store', embedding_function=get_function())
    
    search_result = vector_store.similarity_search(user_input)
    context_text = "\n\n\n\n\n".join([doc.page_content for doc in search_result])
    prompt_template = ChatPromptTemplate.from_template(TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=user_input)
    
    return(prompt)
