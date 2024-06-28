from flask import Blueprint, request, jsonify
import os
import json
import re
from dotenv import load_dotenv, find_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
# from langchain_core.pydantic_v1 import BaseModel
# from langchain_text_splitters import RecursiveJsonSplitter

json_bp = Blueprint('json', __name__)

#1. a function that takes a sentence, let's say, and converts it into valid json, as you know, 
# a prompt returns a string, and there are functions to transform it into json, however, if that 
# string doesn't have specific json format, errors can occur, we want to avoid that and ensure the result 
# is 100% valid json

#2. another function that corrects an invalid json, for example, sometimes it might return with extra 
# characters like ```json{ which makes it invalid json format, the idea is to create a function that corrects 
# these errors when they occur

_ = load_dotenv(find_dotenv())

llm_model = "gpt-3.5-turbo"
chat_llm = ChatOpenAI(temperature=0.0, 
                      model=llm_model, 
                      api_key=os.environ.get('OPEN_API_KEY'),
                      verbose=True)

@json_bp.route('/json', methods = ["POST"])
def get_json(): # This is the first function where the user will input a sentence and it will answer and convert it into valid json
    try:
        data = request.get_json()
        user_input = data.get('strInput')

        output_parser = JsonOutputParser()

        format_instructions = output_parser.get_format_instructions()

        template_string = """
        You are a very helpful assistant. Your task is to extract the information from the sentence and format it into valid JSON. \
        You will be given a sentence, and you will do your best to answer the question. \

        Here is a sentence: {user_input}

        Format with the following instructions: {format_instructions}
        """

        prompt_template = PromptTemplate(
            input_variables=["user_input"],
            partial_variables={"format_instructions": format_instructions},
            template=template_string
        )

        chain = prompt_template | chat_llm | output_parser

        result = chain.invoke({"user_input": user_input})

        print(result)
        print(type(result))

        json_string = json.dumps(result)

        return json_string

    except Exception as e:
        print ("Error: ", e)
        return str(e)
    
@json_bp.route('/fix_json', methods = ["POST"])
def fix_invalid_json(): # This is the second function where the user will input an invalid json and it will correct it
    try:
        data = request.get_json()
        user_input = data.get('strInput')

        print(user_input)

        output_parser = JsonOutputParser()

        validate_template_string = """
        you are a very helpful JSON validator. Given an invalid JSON object, you will correct the JSON format \
        and return a valid JSON object.

        Here is an invalid JSON object: {user_input}

        Please correct the JSON format and return a valid JSON object.
        """

        validate_prompt_template = PromptTemplate(template=validate_template_string, input_variables=["user_input"])

        chain = validate_prompt_template | chat_llm | output_parser

        validate_result = chain.invoke({"user_input": user_input})
    
        json_result = json.dumps(validate_result)
        print(type(json_result))

        return json_result
    except Exception as e:
        return ("Error: ", e)