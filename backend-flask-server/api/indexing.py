from flask import Blueprint, request
import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader
from langchain_community.document_loaders import WikipediaLoader

from langchain.indexes import SQLRecordManager, index
from langchain_core.documents import Document
from langchain.output_parsers import ResponseSchema, StructuredOutputParser


indexing_bp = Blueprint('indexing', __name__)

_ = load_dotenv(find_dotenv())

llm_model = "gpt-3.5-turbo"
chat_llm = ChatOpenAI(temperature=0.0, 
                      model=llm_model, 
                      api_key=os.environ.get('OPEN_API_KEY'),
                      verbose=True)

# embedding = OpenAIEmbeddings(api_key=os.environ.get('OPEN_API_KEY'))

vectorstore = Chroma(
    embedding_function = OpenAIEmbeddings(api_key=os.environ.get('OPEN_API_KEY'))
)

collection_name = "wiki_docs"
namespace = f"chromadb/{collection_name}"

record_manager = SQLRecordManager(namespace=namespace, db_url="sqlite:///record_manager_cache.sql")

record_manager.create_schema()

response_schemas = [
ResponseSchema(name="response", 
                description="Response to the user's question")]

output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

def _clear():
    """Hacky helper method to clear content. See the `full` mode section to to understand why it works."""
    index([], record_manager, vectorstore, cleanup="full", source_id_key="source")

# This route will load up the initial Document files that the user specifies
@indexing_bp.route('/load_docs', methods = ["POST"])
def load_docs():
    try:
        data = request.get_json()
        user_input = data.get('strInput')

        docs = WikipediaLoader(query=user_input, load_max_docs=7).load()

        print(index(docs, record_manager, vectorstore, cleanup=None, source_id_key="source"))

        return "ok"
    except Exception as e:
        return str(e)
    
#This route will manage the user's follow up questions that will retrieve answers from the documents
@indexing_bp.route('/response_with_indexing', methods = ["POST"])
def get_response():
    try:
        data = request.get_json()
        user_input = data.get('strInput')

        related_docs = vectorstore.similarity_search(user_input)

        template_string = """
        You are a very helpful assistant. You will base your answer with the given context. Do not make up any answer or \
        context. If not enough context can answer the user's question, just say that you do not know.

        Here is the context: {context}
        Here i is the user's question: {user_input}
        """

        prompt_template = PromptTemplate.from_template(template=template_string, input_variables=["context", "user_input"])

        chain = prompt_template | chat_llm | output_parser

        response = chain.invoke({"context": related_docs, "user_input": user_input})

        print(response)

        return "response OK"
    except Exception as e:
        return str(e)
    
@indexing_bp.route('/clear_index', methods = ["POST"])
def clear_index():
    try:
        _clear()
        return "OK"
    except Exception as e:
        return str(e)



# EXAMPLE FROM DOCUMENTATION
# collection_name = "test_index"

# embedding = OpenAIEmbeddings()

# vectorstore = ElasticsearchStore(
#     es_url="http://localhost:9200", index_name="test_index", embedding=embedding
# )
# namespace = f"elasticsearch/{collection_name}"
# record_manager = SQLRecordManager(
#     namespace, db_url="sqlite:///record_manager_cache.sql"
# )
# record_manager.create_schema()
# doc1 = Document(page_content="kitty", metadata={"source": "kitty.txt"})
# doc2 = Document(page_content="doggy", metadata={"source": "doggy.txt"})
# index(
#     [doc1, doc1, doc1, doc1, doc1],
#     record_manager,
#     vectorstore,
#     cleanup=None,
#     source_id_key="source",
# )
# output : {'num_added': 1, 'num_updated': 0, 'num_skipped': 0, 'num_deleted': 0}