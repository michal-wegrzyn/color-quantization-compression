# Color Quantization Compression

Color Quantization Compression (CQC) is a project that compresses images by reducing the number of colors using the K-means clustering algorithm and then applies LZSS and Huffman coding for further compression. The compressed images are saved with a `.cqc` extension.

## Requirements

```bash
pip install -r requirements.txt
```

## Usage

### Compress image

```bash
python3 compress.py image_path K 
```

### Decompress image

```bash
python3 decompress.py image_path.cqc new_image_path
```

### Show color palette

```bash
python3 show_color_palette.py image_path
```