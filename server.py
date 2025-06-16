from flask import Flask, request, send_file
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
TILE_FOLDER = os.path.join(UPLOAD_FOLDER, 'tiles')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TILE_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    print("in generate")
    if 'background' not in request.files or 'tiles' not in request.files:
        return 'Missing files', 400

    bg_file = request.files['background']  # input.png
    bg_filename = secure_filename(bg_file.filename)
    bg_path = os.path.join(UPLOAD_FOLDER, bg_filename) # uploads/background.png OR uploads\\background.png
    bg_file.save(bg_path) # bg_file ->writesInto-> bg_path

    # Clear and recreate tile folder
    for f in os.listdir(TILE_FOLDER): # f -> filename
        os.remove(os.path.join(TILE_FOLDER, f)) # rebuild the path and pass it to the remove function

    tile_files = request.files.getlist('tiles')
    for tile_file in tile_files:
        tile_filename = secure_filename(tile_file.filename)
        tile_path = os.path.join(TILE_FOLDER, tile_filename)
        tile_file.save(tile_path)

    num_tiles = request.form.get('num_tiles')
    pixels_per_tile = request.form.get('pixels_per_tile')

    output_path = os.path.join(UPLOAD_FOLDER, 'mosaic_output.png')

    subprocess.run(['./mosaics', bg_path, TILE_FOLDER, num_tiles, pixels_per_tile, output_path], check=True)

    return send_file(output_path, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
