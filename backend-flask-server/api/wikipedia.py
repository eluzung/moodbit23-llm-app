from flask import Blueprint, request
import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.agent_toolkits.load_tools import load_tools
# from langchain.agents import AgentType, initialize_agent, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.retrievers import WikipediaRetriever
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

from typing import List

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

wiki_bp = Blueprint('wikipedia', __name__)

_ = load_dotenv(find_dotenv())

llm_model = "gpt-3.5-turbo"
chat_llm = ChatOpenAI(temperature=0.0, 
                      model=llm_model, 
                      api_key=os.environ.get('OPEN_API_KEY'))

memory = ConversationSummaryBufferMemory(llm=chat_llm, max_token_limit=100)

convo_with_summary = ConversationChain(llm=chat_llm,memory=memory)

tools = load_tools(["wikipedia"], llm=chat_llm)

# agent = create_react_agent(
#     tools, 
#     chat_llm, 
#     agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
#     handle_parsing_errors=True,
#     verbose = True)


def format_docs(docs: List[Document]):
    return "\n\n".join(str(doc) for doc in docs)

@wiki_bp.route('/wikipedia', methods = ["POST"])
def get_wiki_response():
    try:
        data = request.get_json()
        user_input = data.get('strInput')

        docs = WikipediaLoader(query=user_input, load_max_docs=2).load()

        formatted_docs = format_docs(docs)

        response_schemas = [
            ResponseSchema(name="response", description="Response to the user's question"),
            ResponseSchema(name="link", description="Link of wikipedia page where the response is based off of.")
        ]

        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

        format_instructions = output_parser.get_format_instructions()

        template_string = """
            You are a helpful assistant that when given a question, you will answer with the context provided in the Wikipedia article snippets. Each response should be concise \
            and there is no need to make up answers. If the article snippets do not answer the user's question, just say that you do not know. There may be information that is \
            not needed or is irrelevant to the user's question, simply include only relevant information. 

            This is the User's question:
            {user_input}

            These are the Wikipedia article snippets where you will base your answer off of:
            {context}

            format with the following instructions: {format_instructions}
            """
        
        prompt_template = PromptTemplate(template=template_string, input_variables=["user_input", "context"], partial_variables={"format_instructions": format_instructions})

        chain = prompt_template | chat_llm | output_parser

        response = chain.invoke({"user_input": user_input, "context": formatted_docs})
        # messages = prompt_template.format_messages(user_input=user_input, context=formatted_docs,)
        # response = chat_llm(messages)

        return response
    except Exception:
        return 'error'
    

def get_wiki_response_with_chain():
    try:
        data = request.get_json()
        user_input = data.get('strInput')

        template_string = """
            You are a helpful assistant that when given a question, you will answer with the context provided in the Wikipedia article snippets. Each response should be concise \
            and there is no need to make up answers. If the article snippets do not answer the user's question, just say that you do not know. At the end of your answer, please \
            provide the link to the wikipedia page where your answer refers to. the wikipedia link is in the snippet with the tag 'source'.

            This is the User's question:
            {user_input}

            These are the Wikipedia article snippets where you will base your answer off of:
            {context}
            """
        
        wiki_retriever = WikipediaRetriever(top_k_results=5, doc_content_chars_max=1000)

        prompt_template = ChatPromptTemplate.from_template(template_string)

        rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
            | prompt_template
            | chat_llm
            | StrOutputParser()
        )

        retrieve_docs = (lambda x: x["user_input"]) | wiki_retriever

        print(retrieve_docs)

        chain = RunnablePassthrough.assign(context=retrieve_docs).assign(
            answer=rag_chain_from_docs
        )

        result = chain.invoke(user_input)

        return 'ok'
    except Exception:
        return 'error'

# def get_wiki_response():
#     try:
#         data = request.get_json()
#         user_input = data.get('strInput')

#         response = agent(user_input)
#         print(response)
#         return response

#     except Exception:
#         return "error has occured"

        # docs = WikipediaRetriever(top_k_results=5).ainvoke(query=user_input)
        # print(len(docs))
        # print()
        # print(docs[0].metadata)
        # print()
        # print(docs[1])
        # print()
        # print(docs[1].metadata)
        # print()
        # print(docs[1].metadata.get('source'))
