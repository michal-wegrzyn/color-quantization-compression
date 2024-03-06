import heapq

def generate_trie(counter):
    h = []
    tries = [i for i in range(len(counter))]
    for i, v in enumerate(counter):
        heapq.heappush(h, (v,i))
    while len(h) >= 2:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        tries[a[1]] = (tries[a[1]], tries[b[1]])
        heapq.heappush(h,(a[0]+b[0], a[1]))

    return tries[h[0][1]]

def generate_flatten_trie(counter):
    h = []
    for i, v in enumerate(counter):
        heapq.heappush(h, (v,(i,)))
    while len(h) >= 2:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        heapq.heappush(h,(a[0]+b[0], (*a[1],*b[1])))

    return h[0][1]

def generate_codes(counter):
    h = []
    codes  = [[] for _ in counter]
    for i, v in enumerate(counter):
        heapq.heappush(h, (v,(i,)))
    while len(h) >= 2:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        for i in a[1]:
            codes[i].append(0)
        for i in b[1]:
            codes[i].append(1)
        heapq.heappush(h,(a[0]+b[0],(*a[1], *b[1])))
    
    for i in range(len(counter)):
        codes[i] = codes[i][::-1]

    return codes

def get_code_lengths(counter):
    h = []
    lengths  = [0 for _ in counter]
    for i, v in enumerate(counter):
        heapq.heappush(h, (v,(i,)))
    while len(h) >= 2:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        for i in a[1]:
            lengths[i] += 1
        for i in b[1]:
            lengths[i] += 1
        heapq.heappush(h,(a[0]+b[0],(*a[1], *b[1])))
    
    return lengths
