import sys
import os
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans
from lzss import list_compression
from save_image import write_to_file
from pathlib import Path

if len(sys.argv) >= 2:
    image_path = sys.argv[1]
else:
    image_path = input('Path to image file: ')

if not os.path.exists(image_path):
    print("File doesn't exist")
    exit()

if len(sys.argv) >= 3:
    k = int(sys.argv[2])
else:
    k = int(input('Number of colors: '))

if len(sys.argv) >= 4:
    min_match_length = int(sys.argv[3])
else:
    min_match_length = int(input('Min match length: '))

temp  = min_match_length
min_match_length_bits_cnt = 0
while temp > 0:
    temp //= 2
    min_match_length_bits_cnt += 1

image = Image.open(image_path)
pixels = image.load()
width, height = image.size
flatten_pixels = np.array([pixels[x,y] for x in range(width) for y in range(height)])
used_colors = np.unique(flatten_pixels, axis=0)
if used_colors.shape[0] < k:
    k = used_colors.shape[0]

kmeans = KMeans(n_clusters=k, init='k-means++')
kmeans.fit(flatten_pixels)
kmeans.cluster_centers_ = np.round(kmeans.cluster_centers_)
labels = kmeans.predict(flatten_pixels)

compressed = list_compression([int(i) for i in labels], 4096, 64, min_match_length)

for i in range(len(flatten_pixels)):
    flatten_pixels[i] = kmeans.cluster_centers_[labels[i]]

new_image_path = Path(image_path).with_suffix('.pwfc')
write_to_file(new_image_path, (width, height),compressed, kmeans.cluster_centers_, min_match_length_bits_cnt)