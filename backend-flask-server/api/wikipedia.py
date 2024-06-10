from flask import Blueprint, Response, request
import os
from dotenv import load_dotenv, find_dotenv
import wikipedia
from langchain.agents import tool, load_tools, initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
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


# @tool
# def search_wikipedia(query: str) -> str:
#     """Run Wikipedia search and get page summaries."""
#     page_titles = wikipedia.search(query)
#     summaries = []
#     for page_title in page_titles[: 3]:
#         try:
#             wiki_page =  wikipedia.page(title=page_title, auto_suggest=False)
#             summaries.append(f"Page: {page_title}\nSummary: {wiki_page.summary}")
#         except (
#             self.wiki_client.exceptions.PageError,
#             self.wiki_client.exceptions.DisambiguationError,
#         ):
#             pass
#     if not summaries:
#         return "No good Wikipedia Search Result was found"
#     return "\n\n".join(summaries)

tools = load_tools(["wikipedia"], llm=chat_llm)
#tools = tools + [search_wikipedia]

agent = initialize_agent(
    tools, 
    chat_llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    handle_parsing_errors=True,
    verbose = False)


@wiki_bp.route('/wikipedia', methods = ["POST"])
def get_wiki_response():
    try:
        data = request.get_json()
        user_input = data.get('strInput')

        response = agent(user_input)
        return response

    except Exception:
        return "error has occured"
