import os
import sys
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.cluster import KMeans
from decode import *
import numpy as np
from math import sqrt, floor, ceil

if len(sys.argv) >= 2:
    image_path = sys.argv[1]
else:
    image_path = input('Path to image file: ')

if not os.path.exists(image_path):
    print("File doesn't exist")
    exit()

colors = []

if image_path[-4:] != '.cqc':
    if len(sys.argv) >= 3:
        k = int(sys.argv[2])
    else:
        k = int(input('Number of colors (-1 to see all): '))
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size
    flatten_pixels = np.array([pixels[x,y] for x in range(width) for y in range(height)])
    used_colors = np.unique(flatten_pixels, axis=0)
    if k>0:
        if used_colors.shape[0] < k:
            k = used_colors.shape[0]
        kmeans = KMeans(n_clusters=k, init='k-means++')
        kmeans.fit(flatten_pixels)
        kmeans.cluster_centers_ = np.round(kmeans.cluster_centers_).astype(np.uint8)
        colors = kmeans.cluster_centers_
    else:
        colors = used_colors
else:
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
    colors, _ = read_trie(bits,number_of_channels)

colors = list(colors)
width1 = ceil(sqrt(len(colors)*1.618))
height1 = ceil(len(colors)/width1)
width2 = floor(sqrt(len(colors)*1.618))
height2 = ceil(len(colors)/width2)
if len(colors)%width1 == 0:
    width, height = width1, height1
elif len(colors)%width2 == 0:
    width, height = width2, height2
elif len(colors)%width1 >= len(colors)%width2:
    width, height = width1, height1
else:
    width, height = width2, height2
no_color = [255]*len(colors[0])
diff = width * height - len(colors)
print('Number of colors:', len(colors))
print('Colors:', colors)
plt.figure(num=image_path)
if diff > 0:
    plt.scatter(range(len(colors)%width, width), [height-1]*(width-len(colors)%width), marker = 'x', color='red')
plt.title(f'Palette with {len(colors)} colors of image {image_path}')
colors += [no_color]*diff
plt.imshow(np.array([colors]).astype(np.uint8).reshape(height,width,-1))
plt.show()