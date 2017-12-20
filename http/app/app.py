from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Files Converter 0.0.1.'

@app.route('/v1/add')
def add():
    return 'TODO'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
