from flask import Blueprint, request
import os
import json
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.chains import create_extraction_chain, RetrievalQAWithSourcesChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from typing import List
# import pprint
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.retrievers.web_research import WebResearchRetriever
from langchain_chroma import Chroma
from langchain_google_community import GoogleSearchAPIWrapper
import logging


web_scraping_bp = Blueprint('web_scraping', __name__)

_ = load_dotenv(find_dotenv())

llm_model = "gpt-3.5-turbo"
chat_llm = ChatOpenAI(temperature=0.0, 
                      model=llm_model, 
                      api_key=os.environ.get('OPEN_API_KEY'),
                      verbose=True)

# Vectorstore
vectorstore = Chroma(
    embedding_function = OpenAIEmbeddings(api_key=os.environ.get('OPEN_API_KEY')), persist_directory="./chroma_db_oai"
)

# Search
search = GoogleSearchAPIWrapper(google_api_key=os.environ.get('GOOGLE_API_KEY'), google_cse_id=os.environ.get('GOOGLE_CSE_ID'))

# Initialize
web_research_retriever = WebResearchRetriever.from_llm(
    vectorstore=vectorstore, llm=chat_llm, search=search
)



logging.basicConfig()
logging.getLogger("langchain_community.retrievers.web_research").setLevel(logging.INFO)

@web_scraping_bp.route('/web_scraping_search', methods = ["POST"])
def test2():
    try:
        data = request.get_json()
        user_input = data.get('strInput')

        qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
        chat_llm, retriever=web_research_retriever)

        result = qa_chain.invoke({"question": user_input})

        if (result.get('sources') == ''):
            direct_search_results = web_research_retriever.invoke(user_input)
            
            response_schemas = [
            ResponseSchema(name="summary_list", 
                            description="List of summary Dictionaries with the following format: [{'summary': str, 'title': str, 'source': str}]")]

            output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

            format_instructions = output_parser.get_format_instructions()

            summary_string = """
            You are a helpful assistant that can create concise summaries. The following is a list of Documents and you \
            need to create short and concise summaries for each document:
            {direct_search_results}
            You can only base your answer with the provided \
            text under the tag 'page_content' and ignore the tag 'metadata' and its contents. If a Document has the exact \
            same 'source' as another Document, combine the summaries together and make sure the combination is seamless. \
            
            Format with the following instructions: {format_instructions}
            """

            summary_template = PromptTemplate(template=summary_string, input_variables=["direct_search_results"], partial_variables={"format_instructions": format_instructions})

            chain = summary_template | chat_llm | output_parser

            direct_result = chain.invoke({"direct_search_results": direct_search_results})

            return direct_result
        return result
    except Exception as e:
        json_object = {"error": str(e)}
        return(json_object)


@web_scraping_bp.route('/web_scraping', methods = ["POST"])
def test():
    try:
        urls = ["https://www.wsj.com/"]
        print(scrape_with_playwright(urls))

        return 'OK'
    except Exception:
        return 'An error has occured'
    
@web_scraping_bp.route('/get_id', methods = ["POST"])
def get_id():
    return vectorstore.get()
    
def scrape_with_playwright(urls):
    #load and transform
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["span"]
    )

    #Create schema
    schema = {
    "properties": {
        "news_article_title": {"type": "string"},
        "news_article_summary": {"type": "string"},
    },
    "required": ["news_article_title", "news_article_summary"],
    }

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)

    # Process the first split
    extracted_content = extract(schema=schema, content=splits[0].page_content)
    return extracted_content

# # Load HTML
# urls = ["https://www.espn.com", "https://lilianweng.github.io/posts/2023-06-23-agent/"]
# loader = AsyncChromiumLoader(urls)
# html = loader.load()

# # Transform
# bs_transformer = BeautifulSoupTransformer()
# docs_transformed = bs_transformer.transform_documents(
#     html, tags_to_extract=["p", "li", "div", "a"]
# )

# Create schema and extract function (provided by LangChain documentation)
# schema = {
#     "properties": {
#         "news_article_title": {"type": "string"},
#         "news_article_summary": {"type": "string"},
#     },
#     "required": ["news_article_title", "news_article_summary"],
# }


def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=chat_llm).run(content)