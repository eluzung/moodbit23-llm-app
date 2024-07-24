from flask import Blueprint, request, jsonify
import os

upload_file_bp = Blueprint('upload_file', __name__)

@upload_file_bp.route('/upload_file', methods=['POST'])
def upload_file():
    try :
        file = request.files['file']
        print("this is the file: ", file)
        print(file.read())


        return "OK"

    except Exception as e:
        return jsonify({'error': str(e)})