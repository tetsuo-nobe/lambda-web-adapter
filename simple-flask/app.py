from flask import Flask

app = Flask(__name__)

@app.route('/')
def flask_app():
    return 'こんにちは！Flask'
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
