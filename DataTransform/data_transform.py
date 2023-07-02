def data_transform(data, data_map):
    res = []
    for letter in data:
        if letter in data_map:
            res.append(data_map[letter])
            continue
        res.append(letter)
    return ''.join(res)
