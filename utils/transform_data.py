def camel_case(key: str):
    words = key.lower().split('_')
    first_word = words[0]
    return first_word + "".join(map(lambda w: w.capitalize(), words[1:]))


def scale_monetary(row):
    scale = 1000 if row['escalaMoeda'] == 'UNIDADE' else 1
    return row['vlConta'] * scale
