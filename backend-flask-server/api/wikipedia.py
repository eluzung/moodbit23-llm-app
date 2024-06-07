from flask import Blueprint, Response, request
import os
from dotenv import load_dotenv, find_dotenv
import wikipedia
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain

wiki_bp = Blueprint('wikipedia', __name__)

_ = load_dotenv(find_dotenv())

llm_model = "gpt-3.5-turbo"
chat_llm = ChatOpenAI(temperature=0.0, 
                      model=llm_model, 
                      api_key=os.environ.get('OPEN_API_KEY'))
memory = ConversationSummaryBufferMemory(llm=chat_llm, max_token_limit=100)
convo_with_summary = ConversationChain(llm=chat_llm,memory=memory)

tools = load_tools(["wikipedia"], llm=chat_llm)
agent = initialize_agent(
    tools, 
    chat_llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = False)

@wiki_bp.route('/wikipedia', methods = ["POST"])
def get_wiki_response():
 return "1"