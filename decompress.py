import sys
import os
from PIL import Image
from decode import *
from lzss import list_decompression
import numpy as np
from pathlib import Path

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

with open(image_path, 'rb') as f:
    file_bytes = f.read()

file_bits = []
for i in file_bytes:
    for v in [128,64,32,16,8,4,2,1]:
        if i >= v:
            i -= v
            file_bits.append(1)
        else:
            file_bits.append(0)

bits = [file_bits, 0]
number_of_channels = read_number(bits,1)+3
min_lzss_match_bits_cnt = read_number(bits,5)
width = read_number(bits, 16)
height = read_number(bits, 16)
colors, trie = read_trie(bits,number_of_channels)
data = read_lzss_data(bits, width*height, trie, 3)

decompressed = list_decompression(data)
pixels = np.zeros((height,width,number_of_channels),dtype=np.uint8)

for y in range(height):
    for x in range(width):
        pixels[y,x] = colors[decompressed[y+height*x]]
image = Image.fromarray(pixels)
image.save(new_path)