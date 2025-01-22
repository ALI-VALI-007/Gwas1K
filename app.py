from flask import Flask, request, jsonify, send_from_directory
import os
from graphs import userInput
app = Flask(__name__)

# Get the absolute path to the graphs directory
GRAPHS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphs')

@app.route('/')
def home():
    return open('index.html').read()

@app.route('/process', methods=['POST'])
def process():
    input_value = request.form['userInput']
    result = userInput(input_value)
    return jsonify({'filenames': result})

@app.route('/graphs/<path:filename>')
def serve_graph(filename):
    # Use the absolute path to serve files from the graphs directory
    return send_from_directory(GRAPHS_DIR, filename)

if __name__ == '__main__':
    app.run(debug=True)
