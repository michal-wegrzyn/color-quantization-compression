def read_number(bits, number_of_bits):
    number = 0
    for i in range(bits[1], bits[1]+number_of_bits):
        number = number * 2 + bits[0][i]
    bits[1] += number_of_bits
    return number

def read_number2(bits, min_bits_cnt=1):
    b, pos = bits
    a = min_bits_cnt - 1
    ans = 1
    while b[pos] == 0:
        a += 1
        pos += 1
    pos += 1
    for _ in range(a):
        ans = ans*2+b[pos]
        pos += 1
    bits[1] = pos
    return ans

def read_trie(bits, number_of_channels, colors_cnt=-1):
    b, pos = bits
    bits[1] += 1
    if b[pos] == 0:
        a = []
        for _ in range(number_of_channels):
            a.append(read_number(bits,8))
        return [a], colors_cnt+1
    l = read_trie(bits, number_of_channels, colors_cnt)
    r = read_trie(bits,number_of_channels,colors_cnt+len(l[0]))
    return l[0]+r[0], (l[1],r[1])

def read_code(bits, trie):
    while isinstance(trie, tuple):
        trie = trie[bits[0][bits[1]]]
        bits[1] += 1
    return trie

def read_lzss_literals(bits, trie):
    cnt = read_number2(bits)
    literals = []
    for _ in range(cnt):
        literals.append(read_code(bits, trie))
    return literals

def read_lzss_match(bits, min_match_length_bits_cnt=1):
    is_long = read_number(bits,1)
    l = 0
    if is_long:
        l = read_number(bits, 14)
    else:
        l = read_number(bits,8)
    cnt = read_number2(bits, min_match_length_bits_cnt)
    return (l, cnt)

def read_lzss_data(bits, pixels_cnt, trie, min_match_length_bits_cnt=1):
    data = []
    cnt = 0
    while cnt < pixels_cnt:
        is_match = read_number(bits,1)
        if is_match:
            data.append(read_lzss_match(bits,min_match_length_bits_cnt))
            cnt += data[-1][1]
        else:
            l = read_lzss_literals(bits,trie)
            cnt += len(l)
            data += l
    return data
