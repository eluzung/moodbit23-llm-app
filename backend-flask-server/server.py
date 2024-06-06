from flask import Flask
from api import api_bp

app = Flask(__name__)

@app.route('/')
def test():
    return 'testing works'

# import api route
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(debug=True)