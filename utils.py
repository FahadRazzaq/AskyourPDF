from PyPDF2 import PdfReader
from langchain.chat_models import ChatAnthropic
from langchain.schema import HumanMessage
import time
import os

# Set the Anthropics API Key
os.environ["ANTHROPIC_API_KEY"] = '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'

def preprocess_uploaded_files(file_path):
    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

def get_response_from_files(input_question, text):
    chat = ChatAnthropic()
    question_message = HumanMessage(content=input_question)
    messages = [HumanMessage(content=text), question_message]

    start_time = time.time()  # Record the start time
    responses = chat(messages)
    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate the execution time
    print(f"Getting responses from file Time: {execution_time:.3f} seconds")

    response_contents = []
    for response in responses:
        if isinstance(response, tuple) and response[0] == "content":
            response_contents.append(response[1])

    formatted_response = "\n\n".join(response_contents)

    return formatted_response
