import os
from decode import *
from lzss import list_decompression
import numpy as np

def read_from_file(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, 'rb') as f:
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
    
    return pixels