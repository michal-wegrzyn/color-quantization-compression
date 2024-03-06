def list_compression(data, window_size, kmp_min_result, min_to_save=5):
    MOD = 223609732146239
    P = 1031
    INV_P = pow(P, -1, MOD)
    pow_P = [1]
    inv_pow_P = [1]
    prefix_hash = [0]
    for i in data:
        if i >= P:
            raise ValueError
        prefix_hash.append((prefix_hash[-1]+(i+1)*pow_P[-1])%MOD)
        pow_P.append(pow_P[-1]*P % MOD)
        inv_pow_P.append(inv_pow_P[-1]*INV_P % MOD)

    def substring_hash(start, end):
        return (prefix_hash[end+1]-prefix_hash[start])*inv_pow_P[start]%MOD

    res = []
    d = {}
    pos = 0
    print_pos = 0
    while pos < len(data):
        if pos - print_pos > len(data)//10:
            print(pos*100//len(data), '%', sep='')
            print_pos = pos
        hshkmp = -1
        do_kmp = 0
        if len(data)-pos >= kmp_min_result:
            hshkmp = substring_hash(pos, pos+kmp_min_result-1)
            if hshkmp in d:
                do_kmp = 1
        if do_kmp:
            ind = max(0, pos-window_size)
            longest_prefsuf = [0]
            best_index = ind
            best_len = 0
            curr_len = 0
            pattern_len = 0
            while pos+curr_len < len(data) and ind-curr_len < pos:
                while curr_len > 0 and data[pos+curr_len] != data[ind]:
                    while curr_len > len(longest_prefsuf):
                        while pattern_len>0 and data[pos+pattern_len] != data[pos+len(longest_prefsuf)]:
                            pattern_len = longest_prefsuf[pattern_len-1]
                        if data[pos+pattern_len] == data[pos+len(longest_prefsuf)]:
                            pattern_len += 1
                        longest_prefsuf.append(pattern_len)
                    curr_len = longest_prefsuf[curr_len - 1]
                
                if data[pos+curr_len] == data[ind]:
                    curr_len += 1
                
                if curr_len > best_len:
                    best_len = curr_len
                    best_index = ind-curr_len+1
                
                ind += 1

            res.append((pos-best_index, best_len))

        else:
            st = 0
            en = min(kmp_min_result, len(data)-pos+1)
            while st+1<en:
                middle = (st+en)//2
                if substring_hash(pos, pos+middle-1) in d:
                    st = middle
                else:
                    en = middle
            if st == 0:
                res.append(data[pos])
            else:
                res.append((pos - d[substring_hash(pos, pos+st-1)], st))
        
        r = res[-1]
        new_pos = pos + 1
        if type(res[-1]) == tuple:
            new_pos = pos + r[1]
            if r[1] < min_to_save:
                res.pop()
                for i in range(r[1]):
                    res.append(data[pos+i])
        
        for ppos in range(pos, new_pos):
            for i in range(min(kmp_min_result, len(data)-ppos)):
                d[substring_hash(ppos, ppos+i)] = ppos
            if ppos >= window_size:
                for i in range(min(kmp_min_result, len(data)-ppos+window_size)):
                    hsh = substring_hash(ppos-window_size, ppos-window_size+i)
                    if hsh in d:
                        if d[hsh] <= ppos - window_size:
                            del d[hsh]

        pos = new_pos        
    
    return res

def list_decompression(compressed_data):
    data = []
    for i in compressed_data:
        if type(i) == tuple:
            for _ in range(i[1]):
                data.append(data[-i[0]])
        else:
            data.append(i)
    return data
