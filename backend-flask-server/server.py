from flask import Flask

app = Flask(__name__)
app.register_blueprint(op)

@app.route('/')
def test():
    return 'testing works'

if __name__ == '__main__':
    app.run(debug=True)