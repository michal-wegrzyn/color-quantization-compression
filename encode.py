def number_to_bits(number, bits_cnt):
    bits = []
    pow2 = pow(2,bits_cnt-1)
    for i in range(bits_cnt):
        if number >= pow2:
            number -= pow2
            bits.append(1)
        else:
            bits.append(0)
        pow2 //= 2
    return bits

def number_to_bits2(number, min_bits_cnt=1):
    bits = []
    while number > 0:
        bits.append(number%2)
        number //= 2
    bits += [0 for _ in range(len(bits)-min_bits_cnt)]
    return bits[::-1]

def color_to_bits(color):
    bits = []
    BITS_COLOR = 8
    for channel in color:
        bits += number_to_bits(channel, BITS_COLOR)

    return bits

def huffmantrie_to_bits(trie, colors):
    if type(trie) == int:
        return [0]+color_to_bits(colors[trie])
    return [1]+huffmantrie_to_bits(trie[0], colors)+huffmantrie_to_bits(trie[1], colors)

def lzss_match_to_bits(match, min_length_bits_cnt = 1):
    bits = []
    if match[0] < 256:
        bits.append(0)
        bits += number_to_bits(match[0], 8)
    else:
        bits.append(1)
        bits += number_to_bits(match[0], 14)
    bits += number_to_bits2(match[1], min_length_bits_cnt)
    return bits

def lzss_literals_to_bits(literals, codes):
    bits = number_to_bits2(len(literals))
    for i in literals:
        bits += codes[i]
    return bits

def lzss_data_to_bits(data, codes, min_match_length_bits_cnt=1):
    bits = []
    literals = []
    for i in data:
        if type(i) == int:
            literals.append(i)
            continue
        if len(literals) > 0:
            bits.append(0)
            bits += lzss_literals_to_bits(literals, codes)
            literals = []
        bits.append(1)
        bits += lzss_match_to_bits(i, min_match_length_bits_cnt)
    
    if len(literals) > 0:
        bits.append(0)
        bits += lzss_literals_to_bits(literals, codes)
    
    return bits