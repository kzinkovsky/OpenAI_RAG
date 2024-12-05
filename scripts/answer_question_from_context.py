from pydantic import BaseModel, Field, ValidationError
from langchain.prompts import PromptTemplate

def retrieve_context(question, query_retriever):
    """
    Retrieves a relevant context.
    Args:
        question: str with user question.
        query_retriever: FAISS query_retriever.
    Returns:
        context: list with str of context.
    """

    # Retrieve relevant chanks for the given question
    retrieved_chanks = query_retriever.invoke(question)

    # Concatenate retrieved chanks in one context
    context = [chank.page_content for chank in retrieved_chanks]

    return context

class QuestionAnswerFromContext(BaseModel):
    """A class for formatting the output data of a model according to a given structure."""
    answer: str = Field(description="Generates an answer to a query based on a given context.")
    context: list[str] = Field(description="The context used to generate the answer.")
    question: str = Field(description="The question that was answered.")


def create_question_answer_from_context_chain(llm):
    """
    Creates a langchain question-answer chain using a given language model.
    Args:
        llm: LLM model used for getting answers.
    Returns:
        question_answer_chain: langchain object - chain for getting GenAI's answer to the user's question based on context.
    """
    
    # Create template for queries
    question_answer_prompt_template = """ 
    For the question below, provide a concise but suffice answer based ONLY on the provided context:
    {context}
    Question:
    {question}
    """

    # Create a PromptTemplate object with the specified template and input variables
    question_answer_from_context_prompt = PromptTemplate(
        template=question_answer_prompt_template,
        input_variables=["context", "question"],
    )

    # Create the chain, which processes the prompt template with the llm
    question_answer_chain = question_answer_from_context_prompt | llm
    
    return question_answer_chain


def answer_question_from_context(question, context, question_answer_chain):
    """
    Answers to user's question using the given context.
    Args:
        question: user's question
        context: retrieved context for user's question
        question_answer_chain: processing chain obtained from create_question_answer_from_context_chai function.
    Returns:
        structured_result: the model output structured as QuestionAnswerFromContext object
        output: the model row output
    """
    
    input_data = {
        "question": question,
        "context": context
    }
    print("Preparing results ...")

    output = question_answer_chain.invoke(input_data) 
    
    raw_result = {
    'answer': output.content,
    'context': input_data['context'],
    'question': input_data['question']
    }
    try:
        structured_result = QuestionAnswerFromContext(**raw_result)  
    except ValidationError as e:
        print("Validation Error:", e)
        structured_result = None

    print("Done!")

    return structured_result, output