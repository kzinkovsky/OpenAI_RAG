# Import all needed libraries
import os
import sys
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*NSOpenPanel.*")

from langchain_openai import ChatOpenAI

from scripts.save_input import safe_float_input, safe_int_input
from scripts.read_pdf import select_file, read_pdf
from scripts.splite_encode_document import splite_encode_document, FAISS_config
from scripts.answer_question_from_context import (
    retrieve_context, create_question_answer_from_context_chain, answer_question_from_context
)

# Load .env file with your OpenAI API key
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print(f"API Key loaded")
else:
    print("Error: API Key not found")
    sys.exit("Program terminated: API Key is required.")


# Main function to run the AI assistant
def main():
    print("\n=== AI Assistant for Answering Questions about Texts ===\n=== OpenAI with Retrieval-Augmented Generation (RAG) ===\n")

    # Request path to PDF file with text, load and read it
    user_query1 = ""
    while True:
        print("Please select a pdf file in the window that appears")
        file_path = select_file()
        if file_path:
            print(f"Selected PDF file loading and reading...")
            try:
                document = read_pdf(file_path)
                print("Document uploaded successfully!")
                break
            except Exception as e:
                print(f"Error loading file: {e}")
        else:
            print("File not selected or not found. Please, make again a choice in the window that appears.")
            user_query1 = input("To try again type any symbol, to exit type exit: ").strip().lower()
            if user_query1 in {"exit"}:
                break

    if user_query1 in {"exit"}:
        return "The program has been successfully completed. Bye!"
    
    # Request for RAG tuning parameters
    user_query2 = input("To tune RAG type 'tune'. To use tuning by defolt type any symbol: ").strip().lower()
    RAG_config = FAISS_config(user_query2)
    chunk_size = RAG_config['chunk_size']
    chunk_overlap = RAG_config['chunk_overlap']
    n_chunks_in_context = RAG_config['n_chunks_in_context']
    
    print("Preparing a retriever with your text...")
    # split document and create FAISS vectorestore 
    vectorestore = splite_encode_document(document, chunk_size, chunk_overlap)

    # Create retriever
    query_retriever = vectorestore.as_retriever(search_kwargs={"k": n_chunks_in_context})
    print("The retriever is ready to work")

    # Basic workflow: user request – AI response
    while True:
        print("\nYou can ask the AI assistant in the window that appears. To exit the program, type 'exit'.\n")
        user_query_toAI = input("Your question: ").strip()
        
        if user_query_toAI.lower() in {"exit"}:
            return "Thank you for using the AI assistant. Bye!"
        
        # LLM object with parameters by default
        llm = ChatOpenAI(temperature=0.7, model_name="gpt-4o", max_tokens=2000)
        
        # Code for the hidden ability to change LLM parameters. 
        if user_query_toAI.lower() in {"tune llm"}:
            print("You just requested 'tune llm' for llm tuning\n")
            temperature = safe_float_input("temperature (0.7 by default): ", 0.7)
            model_name = input("model name (press enter for gpt-4o by default): ")
            if not model_name: 
                model_name = "gpt-4o"
            max_tokens = safe_int_input("max tokens (2000 by default): ", 2000)
            llm = ChatOpenAI(temperature=temperature, model_name=model_name, max_tokens=max_tokens)
            user_query_toAI = input("LLM tuning done\nYour question to the AI assistant: ").strip()

        try:
            question_answer_chain = create_question_answer_from_context_chain(llm)
            context = retrieve_context(user_query_toAI, query_retriever)

            structured_result, raw_result = answer_question_from_context(user_query_toAI, context, question_answer_chain)
            print(f"{'Your question:':<15}{user_query_toAI}")
            print(f"{'AI answer:':<15}{structured_result.answer}")
        
        except Exception as e:
            print(f"Error processing request: {e}")


if __name__ == "__main__":
    main()