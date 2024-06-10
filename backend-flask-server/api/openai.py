from flask import Blueprint, Response, request, jsonify
import asyncio
import traceback
import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from langchain_community.chat_models import ChatOpenAI
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


# @openai_bp.route('/response', methods = ["POST"])
# def test():
#     print("This is connected with ngrok")
#     print(request)
#     data = request.get_json()
#     print(data.get('strInput'))
#     #messages = [{"role": "user", "content": data.get('strInput')}]
#     print(chat_llm.invoke(data.get('strInput')))
#     return "OK"



# def get_completion(prompt, model=llm_model):
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0, 
#     )
#     return response.choices[0].message["content"]

    
@openai_bp.route('/response', methods = ["POST"])
async def get_response():
    if request.method == "POST":
    # Simple get_response chain for general queries
        try:
            data = request.get_json()
            user_input = data.get('strInput')

            template_string = """
            You are a very helpful assistant. You answer questions in a concise \
            and respecful manner. If you don't know or do not have enough \
            information to answer the question, do not make up an answer. Just \
            say that you do not know.

            Here is a question: {text}
            """

            prompt_template = ChatPromptTemplate.from_template(template_string)
            messages = prompt_template.format_messages(text=user_input)
            response = chat_llm(messages)
            return response.content

        except Exception:
            return "NOT OK"

@openai_bp.route('/chathistory', methods = ["POST"])
def get_history():
    try:
        return memory.load_memory_variables({})
    except Exception:
        return 'Error has occured'

@openai_bp.route('/chathistory', methods = ["DELETE"])
def delete_history():
    try:
        return memory.clear()
    except Exception:
        return 'Error has occured'