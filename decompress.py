import sys
import os
from PIL import Image
from read_image import read_from_file

if len(sys.argv) >= 2:
    image_path = sys.argv[1]
else:
    image_path = input('Path to image file: ')

if len(sys.argv) >= 3:
    new_path = sys.argv[2]
else:
    new_path = input('Path to new image file: ')

if not os.path.exists(image_path):
    print("File doesn't exist")
    exit()

pixels = read_from_file(image_path)
assert not pixels is None
image = Image.fromarray(pixels)
image.save(new_path)