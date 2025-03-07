from read_pdf import read_pdfs
from generate_embeddings import add_to_storage
from llm_query import llm_query

if __name__ == '__main__':
    pdfs = read_pdfs("handbook_by_chapter")
    add_to_storage(pdfs)
    print(llm_query("How can i cast a spell?"))
