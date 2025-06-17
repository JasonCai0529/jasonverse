from PIL import Image
import os

def convert_to_PNG(file, output_path, resize_num=None):
    img = Image.open(file.stream).convert('RGB')
    if resize_num:
        img.thumbnail((resize_num, resize_num))
    img.save(output_path, format='PNG', optimize=True)


def rescale(path, scale_factor):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image file not found: {path}")
    with Image.open(path) as img:
        new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
        resized = img.resize(new_size, Image.Resampling.LANCZOS)
        resized.save(path, format='PNG', optimize=True)