from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

def split_pdf_data(pdfs : list[Document]):
    splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
    )
    return splitter.split_documents(pdfs)

def read_pdfs(catalog_path):
    loader = PyPDFDirectoryLoader(catalog_path)
    splitted_data = split_pdf_data(loader.load())
    return splitted_data