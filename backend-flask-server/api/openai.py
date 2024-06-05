from flask import Blueprint, request
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

# openai_bp = Blueprint('openai_bp', __name__)
# @openai_bp.route('/openai', methods = ["POST"])
def get_response():
    # Note: backend receives from frontend User input, in the form of a string
    _ = load_dotenv(find_dotenv())

    llm_model = "gpt-3.5-turbo"
    chat_llm = ChatOpenAI(temperature=0.0, model=llm_model, api_key=os.environ.get('OPEN_API_KEY'))

    # Simple get_response chain for general queries
    user_input = request

    template_string = """
    You are a very helpful assistant. You answer questions in a concise \
    and respecful manner. If you don't know or do not have enough \
    information to answer the question, do not make up an answer. Just \
    say that you do not know.

    Here is a question: {input}
    """

    prompt_template = ChatPromptTemplate.from_template(template_string)
    messages = prompt_template.format_messages(text=user_input)
    response = chat_llm(messages)
    print(response.content)