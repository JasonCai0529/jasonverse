import os
from flask import Flask, request, send_file
import subprocess
import shutil
import atexit

from utils.image_utils import convert_to_PNG


app = Flask(__name__)


@atexit.register
def remove_uploads_on_exit(): # upon exit, clear out the whole uploads folder
    shutil.rmtree(UPLOAD_FOLDER, ignore_errors=True)
    print("Cleaned up uploads directory.")

UPLOAD_FOLDER = 'uploads'
TILE_FOLDER = os.path.join(UPLOAD_FOLDER, 'tiles')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TILE_FOLDER, exist_ok=True)

@app.route('/')
def sendIndex():
    return app.send_static_file('index.html')


@app.route('/generate', methods=['POST'])
def generateMosaic():
    print("Starting the process of generating photo mosaic")
    if ("sourceImg" not in request.files or "tileImgs" not in request.files):
        return "Missing source or tile image", 400
    

    source_file = request.files['sourceImg']
    # source_file_name = secure_filename(source_file.filename)
    source_path = os.path.join(UPLOAD_FOLDER, "source.png")
    convert_to_PNG(source_file, source_path, 1200)

    
    for i, tile in enumerate(request.files.getlist('tileImgs')):
        tile_filename = f'tile{i}.png'
        tile_path = os.path.join(TILE_FOLDER, tile_filename)
        convert_to_PNG(tile, tile_path, 100)


    num_tiles = request.form.get('num_tiles')
    pixels_per_tile = request.form.get('pixels_per_tile')

    output_path = os.path.join(UPLOAD_FOLDER, "mosaic_output.png")

    subprocess.run(['./mosaics', source_path, TILE_FOLDER, num_tiles, pixels_per_tile, output_path], check=True)

    return send_file(output_path, mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)