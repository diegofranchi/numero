# web/routes.py

from flask import render_template, request
from web import app
from core_logic.processor import process_data

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_data = request.form['input_data']
    output = process_data(input_data)
    return render_template('index.html', result=output)