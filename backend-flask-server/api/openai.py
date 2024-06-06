from flask import Blueprint, Response, request
import os
from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory


openai_bp = Blueprint('openai', __name__)

_ = load_dotenv(find_dotenv())

llm_model = "gpt-3.5-turbo"
chat_llm = ChatOpenAI(temperature=0.0, 
                      model=llm_model, 
                      api_key=os.environ.get('OPEN_API_KEY'))
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=chat_llm, memory = memory)


@openai_bp.route('/response', methods = ["POST"])
def get_response():
    # Simple get_response chain for general queries
    try:
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
        response = conversation(messages)

        return(response.content)
    except Exception:
        return Response('Error has occured', 500)

@openai_bp.route('/chathistory', methods = ["POST"])
def get_history():
    try:
        return memory.load_memory_variables({})
    except Exception:
        return Response('Error has occured', 500)

@openai_bp.route('/chathistory', methods = ["DELETE"])
def delete_history():
    try:
        return memory.clear()
    except Exception:
        return Response('Error has occured', 500)