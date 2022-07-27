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

    # generate graph
    high_threshold = 10
    medium_threshold = 5
    show_count = False
    sinking_activity = False
    if 'high_threshold' in request.form:
        high_threshold = int(request.form['high_threshold'])
    if 'medium_threshold' in request.form:
        medium_threshold = int(request.form['medium_threshold'])
    if 'show_count' in request.form:
        show_count = True
    if 'sinking_activity' in request.form:
        sinking_activity = True
    img_file = run_graphing(saved_filename, blue_THRESHOLD=medium_threshold, RED_THRESHOLD=high_threshold, SHOW_COUNT=show_count, SINKING_ACTIVITY=sinking_activity)



    image = ''
    with open(img_file, "rb") as f:
        image_binary = f.read()
        image = base64.b64encode(image_binary).decode("utf-8")
    
    os.remove(saved_filename)
    os.remove(img_file)
    return jsonify({'status': True, 'image': image})

    