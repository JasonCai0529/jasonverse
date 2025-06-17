from PIL import Image
import os

def convert_to_PNG(file, output_path, resize_num=None):
    img = Image.open(file.stream).convert('RGB')
    if resize_num:
        img.thumbnail((resize_num, resize_num))
    img.save(output_path, format='PNG', optimize=True)
