from vectordb_handler import load_vectordb
from utils import load_config, timeit
import pypdfium2
import streamlit as st

config = load_config()

def get_pdf_texts(pdfs_bytes_list):
    return [extract_text_from_pdf(pdf_bytes.getvalue()) for pdf_bytes in pdfs_bytes_list]

def extract_text_from_pdf(pdf_bytes):
    pdf_file = pypdfium2.PdfDocument(pdf_bytes)
    return "\n".join(pdf_file.get_page(page_number).get_textpage().get_text_range() for page_number in range(len(pdf_file)))
    
def get_text_chunks(text):
    chunk_size = st.session_state.chunk_size
    chunk_overlap = st.session_state.chunk_overlap
    chunks = []
    
    # Simple text splitting by size with overlap
    for i in range(0, len(text), chunk_size - chunk_overlap):
        chunk = text[i:i + chunk_size]
        chunks.append(chunk)
    
    return chunks

def get_document_chunks(text_list):
    chunks = []
    for text in text_list:
        chunks.extend(get_text_chunks(text))
    return chunks

@timeit
def add_documents_to_db(pdfs_bytes):
    texts = get_pdf_texts(pdfs_bytes)
    chunks = get_document_chunks(texts)
    vector_db = load_vectordb()
    vector_db.add_texts(chunks)
    print("Documents added to db.")