import os
from flask import Flask, request, send_file
from werkzeug.utils import secure_filename
import subprocess
import shutil
import atexit


app = Flask(__name__)


@atexit.register
def remove_uploads_on_exit():
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
    source_file_name = secure_filename(source_file.filename)
    source_path = os.path.join(UPLOAD_FOLDER, source_file_name)
    source_file.save(source_path) # save the sourceImg to the path specified by source_path


    for f in os.listdir(TILE_FOLDER):
        print(TILE_FOLDER)
        os.remove(os.path.join(TILE_FOLDER, f))

    
    for tile in request.files.getlist('tileImgs'):
        tile_filename = secure_filename(tile.filename)
        tile.save(os.path.join(TILE_FOLDER, tile_filename))


    num_tiles = request.form.get('num_tiles')
    pixels_per_tile = request.form.get('pixels_per_tile')

    output_path = os.path.join(UPLOAD_FOLDER, "mosaic_output.png")


    subprocess.run(['./mosaics', source_path, TILE_FOLDER, num_tiles, pixels_per_tile, output_path], check=True)

    return send_file(output_path, mimetype='image/png')


if __name__ == "__main__":
    app.run(debug=True)