import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from scripts.save_input import safe_int_input


def clean_text(texts): 
    """
    Cleans text
    Args:
        texts: text after splitting into chanks using langchain RecursiveCharacterTextSplitter.
    Returns:
        texts: cleaned text 
    """
    
    for text in texts:
        # Remove page numbers with only of numbers (max 4 digits) with optional spaces, hyphens or # around
        text.page_content = re.sub(r'^[\s#-]*\d{1,4}[\s#-]*$', '', text.page_content)
        # Remove suffixes like 'st', 'nd', 'rd', 'th', 'т', 'й' (up to two letters after the number)
        text.page_content = re.sub(r'(\d+)-?([a-zA-Zа-яА-Я]{1,2})', r'\1', text.page_content)
        # Remove # and № in front of numbers
        text.page_content = re.sub(r'[#№](\d+)', r'\1', text.page_content)
         # Remove newline characters
        text.page_content = text.page_content.replace('\n', ' ')

    # Remove empty pages
    texts = [text for text in texts if text.page_content]
    return texts

def FAISS_config(query_to_tune):
    """
    Prompts the user to enter values of some FAISS parameters to tune it.
    Args:
        query_to_tune: a passed request from the user to change or use default parameters ('tune' / any other input)
    Function called inside:
        safe_number_input("Hint", value_by_default)
    Returns:
       config: dictionary with FAISS parameters.
    """
    
    if query_to_tune == 'tune':
        config = {
            "chunk_size": safe_int_input("Input chunk size to split text for RAG (by default 2300): ", 2300),
            "chunk_overlap": safe_int_input("Input chunk overlap (by default 400): ", 400),
            "n_chunks_in_context": safe_int_input("Input number of top chunks retrieved from RAG vector store (by default 2): ", 2)
        }
    else:
        config = {
            "chunk_size": 2300,
            "chunk_overlap": 400,
            "n_chunks_in_context": 2
        }

    return config


def splite_encode_document(document, chunk_size, chunk_overlap):
    """
    Splits and encodes a document into a vector store using OpenAI embeddings and FAISS.
    Args:
        document: a pdf file read using langchain PyPDFLoader.
        chunk_size: text chunk size.
        chunk_overlap: overlap between chunks.
    Function called inside:
        clean_text(texts)
    Returns:
        vectorstore: a FAISS vector store containing the encoded texts.
    """
    # Split document into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )
    texts = text_splitter.split_documents(document)
    texts = clean_text(texts)
    
    # Create embeddings and vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(texts, embeddings)

    return vectorstore