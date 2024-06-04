from flask import Flask

app = Flask(__name__)

@app.route('/')
def test():
    return 'This is a test!'

if __name__ == '__main__':
    app.run(port=5000)