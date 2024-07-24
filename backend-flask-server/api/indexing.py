from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pypdf import PdfReader 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import TextLoader, DirectoryLoader, PyPDFLoader
from langchain_community.document_loaders import WikipediaLoader

from langchain.indexes import SQLRecordManager, index
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

        print(index(docs, record_manager, vectorstore, cleanup="full", source_id_key="source"))

        print("Documents loaded!")

        return "success"
    except Exception as e:
        print("error: " + str(e))
        return "error"
    
@indexing_bp.route('/file_upload', methods=['POST'])
def upload_file():
    try :
        file = request.files['file']

        curr_path = os.getcwd()
        first_lvl = os.path.join(curr_path, os.pardir)
        second_lvl = os.path.join(first_lvl, os.pardir)
        third_lvl = os.path.join(second_lvl, os.pardir)
        fourth_lvl = os.path.join(third_lvl, os.pardir)

        file_in_desktop = os.path.join(fourth_lvl, 'Desktop')
        file_in_documents = os.path.join(fourth_lvl, 'Documents')
        file_in_downloads = os.path.join(fourth_lvl, 'Downloads')

        files_path = os.path.join(os.getcwd(), 'files')

        with open(os.path.join(files_path, file.filename), 'wb') as f:
            if ".pdf" in file.filename:
                try:
                    reader = PdfReader(f"{os.path.join(os.path.abspath(file_in_downloads), file.filename)}")
                    for page in reader.pages:
                        f.write(page.extract_text().encode('utf-8'))
                except Exception as e:
                    try:
                        reader = PdfReader(f"{os.path.join(os.path.abspath(file_in_documents), file.filename)}")
                        for page in reader.pages:
                            f.write(page.extract_text().encode('utf-8'))
                    except Exception as e:
                        try:
                            reader = PdfReader(f"{os.path.join(os.path.abspath(file_in_desktop), file.filename)}")
                            for page in reader.pages:
                                f.write(page.extract_text().encode('utf-8'))
                        except Exception as e:
                            print("File not found in Downloads, Documents or Desktop")
                            print("error: " + str(e))
            else:
                f.write(file.read())

        if ".txt" in file.filename:
            doc = TextLoader(f"{files_path}/{file.filename}").load()
            text_splitter = CharacterTextSplitter(chunk_size=150, chunk_overlap=25)

        if ".pdf" in file.filename:
            doc = PyPDFLoader(f"{files_path}/{file.filename}").load()
            text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)

        documents = text_splitter.split_documents(doc)

        print("documents: ", documents)

        print(index(documents, record_manager, vectorstore, cleanup="full", source_id_key="source"))
        return "OK"

    except Exception as e:
        return jsonify({'error': str(e)})
    
@indexing_bp.route('/indexing/response', methods = ["POST"])
def get_response():
    try:
        data = request.get_json()
        user_input = data.get('strInput')

        # embedding_vector = OpenAIEmbeddings(api_key=os.environ.get('OPEN_API_KEY')).embed_query(user_input)
        # related_docs = vectorstore.similarity_search_by_vector(embedding_vector, k=1)
        related_docs = vectorstore.similarity_search(user_input, k=2)

        format_instructions = output_parser.get_format_instructions()

        template_string = """
        You are a very helpful assistant. You will base your answer with the given context. Do not make up any answer or \
        context. If not enough context can answer the user's question, just say that you do not know.

        Here is the context: {context}
        Here is the user's question: {user_input}

        format with the following instructions: {format_instructions}
        """

        prompt_template = PromptTemplate(template=template_string, input_variables=["user_input", "context"], partial_variables={"format_instructions": format_instructions})

        chain = prompt_template | chat_llm | output_parser

        response = chain.invoke({"user_input": user_input, "context": related_docs})

        print(response)
        return response

    except Exception as e:
        print(str(e))
        return "error"

#This route will manage the user's follow up questions that will retrieve answers from the documents
@indexing_bp.route('/response_with_indexing', methods = ["POST"])
def get_response_with_indexing():
    try:
        data = request.get_json()
        print("getting user input")
        user_input = data.get('strInput')

        print("searching for relevant docs")
        related_docs = vectorstore.similarity_search(user_input)
        print(related_docs[0].page_content)

        print("this is before the template string")
        template_string = """
        You are a very helpful assistant. You will base your answer with the given context. Do not make up any answer or \
        context. If not enough context can answer the user's question, just say that you do not know.

        Here is the context: {context}
        Here is the user's question: {user_input}
        """

        print("this is after the template string and before the prompt template")

        prompt_template = PromptTemplate.from_template(template=template_string, input_variables=["user_input"])
        prompt_template.format(user_input=user_input)

        print("this is after the prompt template and before the chain")

        chain = prompt_template | chat_llm | output_parser

        print("this is after the chain")

        print("retrieving response")
        response = chain.invoke({"user_input": user_input})

        print("response retrieved")

        print(response)

        return user_input
    except Exception as e:
        return str(e)
    
@indexing_bp.route('/clear_index', methods = ["POST"])
def clear_index():
    try:
        _clear()
        return "index cleared"
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