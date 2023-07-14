from flask import Flask, request, jsonify, render_template, session
from werkzeug.utils import secure_filename
from utils import preprocess_uploaded_files, get_response_from_files
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '!@#$%'  # replace with your own secret key

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/get_filenames', methods=['GET'])
def get_filenames():
    files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], f))]
    return jsonify(files)

@app.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('files')
    filenames = []

    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        filenames.append(filename)

    session['uploaded_files'] = filenames

    return jsonify(filenames)

@app.route('/ask', methods=['POST'])
def ask():
    filenames = session.get('uploaded_files', [])
    messageText = request.form.get('messageText')

    combined_text = ""
    for filename in filenames:
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(full_filename):
            combined_text += preprocess_uploaded_files(full_filename)

    response = get_response_from_files(combined_text, messageText)

    return response

@app.route('/cleanup', methods=['POST'])
def cleanup():
    uploaded_files = session.get('uploaded_files', [])

    for filename in uploaded_files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f'{filename} removed')

    session.pop('uploaded_files', None)

    return "Cleanup done"

if __name__ == "__main__":
    app.run(debug=True, port=5000)
