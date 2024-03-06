from huffman_codes import *
from encode import *

def write_to_file(filename, resolution, data, colors, min_lzss_match_length_bits_cnt=1):
    counter = [0 for _ in range(len(colors))]
    for i in data:
        if type(i) == int:
            counter[i] += 1
            
    file_bits = []
    resolution_bits = number_to_bits(resolution[0],16)
    resolution_bits += number_to_bits(resolution[1], 16)
    
    trie = generate_trie(counter)
    codes = generate_codes(counter)
    trie_bits = huffmantrie_to_bits(trie,colors)
    new_color_index = [0 for _ in range(len(colors))]
    for i, v in enumerate(generate_flatten_trie(counter)):
        new_color_index[v] = i

    number_of_channels = len(colors[0])
    assert 3 <= number_of_channels <= 4
    is_alpha_bits = [0]
    if number_of_channels == 4:
        is_alpha_bits = [1]
    min_match_length_bits_cnt_bits = number_to_bits(min_lzss_match_length_bits_cnt, 5)

    data_bits = lzss_data_to_bits(data, codes, min_lzss_match_length_bits_cnt)

    file_bits = is_alpha_bits + min_match_length_bits_cnt_bits + resolution_bits + trie_bits + data_bits
    
    file_bits += [0] * ((-len(file_bits))%8)
    file_bytes = []
    for i in range(0,len(file_bits), 8):
        file_bytes.append(0)
        for j in range(8):
            file_bytes[-1] = file_bytes[-1]*2+file_bits[i+j]
    with open(filename, 'wb') as f:
        f.write(bytes(file_bytes))
