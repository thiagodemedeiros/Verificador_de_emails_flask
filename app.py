from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "hellow world"

app.run(debug=True)