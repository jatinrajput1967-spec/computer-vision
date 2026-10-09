from flask import Flask, render_template, request, jsonify, url_for, send_from_directory, abort
from werkzeug.utils import secure_filename
import os
import uuid
from detector.detect_shapes import detect_shapes

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'static', 'outputs')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'tif', 'tiff'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique = f"{uuid.uuid4().hex}_{filename}"
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique)
        file.save(input_path)

        output_basename = f"processed_{unique}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_basename)

        try:
            result = detect_shapes(input_path, output_path)
        except Exception as e:
            return jsonify({'error': 'Processing error', 'message': str(e)}), 500

        original_url = url_for('static', filename=f'uploads/{unique}')
        processed_url = url_for('static', filename=f'outputs/{os.path.basename(result.get("output_path"))}')

        response = {
            'original': original_url,
            'processed': processed_url,
            'stats': result.get('counts', {}),
            'total': result.get('total', 0),
            'time': result.get('time', 0.0)
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Unsupported file type'}), 400


@app.route('/download')
def download():
    filename = request.args.get('file')
    if not filename:
        abort(400)
    safe = secure_filename(filename)
    dirpath = app.config['OUTPUT_FOLDER']
    if not os.path.exists(os.path.join(dirpath, safe)):
        abort(404)
    return send_from_directory(dirpath, safe, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
