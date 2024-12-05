from tkinter import Tk
from tkinter.filedialog import askopenfilename
from langchain_community.document_loaders import PyPDFLoader

def select_file():
    """
    Allows the user to select a PDF file using the tkinter library's UI and returns the path to the file.
    """

    # Hide the main Tkinter window
    Tk().withdraw()
    # Open file selection dialog
    file_path = askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected")
        file_path = None
    
    return file_path

def read_pdf(path):
    """
    Reads a PDF file from the specified path using langchain PyPDFLoader.
    Args:
        path: The path to the PDF file.
    Returns:
        document: list containing [Document(metadata={'source': '...', 'page': ...}, page_content='...text...', ...] 
    """
    # Load PDF document
    loader = PyPDFLoader(path)
    document = loader.load()

    return document