from flask import Flask, render_template, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
from graph import run_graphing
import base64
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/graph', methods=['POST'])
def generate_graph():
    print("received input")
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    filename = secure_filename(file.filename)
    saved_filename = 'test_'+filename
    file.save(saved_filename)
    img_file = run_graphing(saved_filename)
    image = ''
    with open(img_file, "rb") as f:
        image_binary = f.read()
        image = base64.b64encode(image_binary).decode("utf-8")
    
    os.remove(saved_filename)
    os.remove(img_file)
    return jsonify({'status': True, 'image': image})

    