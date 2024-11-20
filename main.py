#!/bin/python3
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz/index.html')

if __name__ == '__main__':
    app.run(debug=True)
