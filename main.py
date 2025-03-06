from read_pdf import read_pdfs
from generate_embeddings import add_to_storage

if __name__ == '__main__':
    pdfs = read_pdfs("handbook_by_chapter")
    print(pdfs[0])
    add_to_storage(pdfs)