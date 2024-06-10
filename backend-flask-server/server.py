from flask import Flask
from flask_cors import CORS
from api import api_bp

app = Flask(__name__)
CORS(app, origins=["*"])

@app.route('/')
def test():
    return 'testing works'

@app.route('/ngrok', methods=['POST'])
def test2():
    print("This is in the console")
    return 'ngrok'

# import api route
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(port=8080)