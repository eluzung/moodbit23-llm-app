from flask import Blueprint, request
import os
from dotenv import load_dotenv, find_dotenv
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain.chains import create_extraction_chain, RetrievalQAWithSourcesChain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
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
            chat_llm, retriever=web_research_retriever,
        )
        result = qa_chain.invoke({"question": user_input})
        return result
    except Exception:
        return 'Error occured'


@web_scraping_bp.route('/web_scraping', methods = ["POST"])
def test():
    try:
        urls = ["https://www.wsj.com/"]
        print(scrape_with_playwright(urls))

        return 'OK'
    except Exception:
        return 'An error has occured'
    
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