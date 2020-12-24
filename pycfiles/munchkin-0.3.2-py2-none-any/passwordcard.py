# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/gszathmari/munchkin/munchkin/lib/passwordcard/passwordcard.py
# Compiled at: 2016-05-02 03:44:35
import javarandom
CHARSETS = {'original.digits': '0123456789', 
   'original.alphanumeric': '23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ', 
   'original.alphanumeric_with_symbols': '23456789abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ@#$%&*<>?€+{}[]()/\\'}
HEADERS = {'original': '■□▲△○●★☂☀☁☹☺♠♣♥♦♫€¥£$!?¡¿⊙◐◩�'}

def generate_character_sets(symbols, digits):
    characters = {}
    if symbols and not digits:
        characters['top_odd'] = list(CHARSETS['original.alphanumeric'])
        characters['top_even'] = list(CHARSETS['original.alphanumeric_with_symbols'])
        characters['bottom_odd'] = list(CHARSETS['original.alphanumeric'])
        characters['bottom_even'] = list(CHARSETS['original.alphanumeric_with_symbols'])
    elif symbols and digits:
        characters['top_odd'] = list(CHARSETS['original.alphanumeric'])
        characters['top_even'] = list(CHARSETS['original.alphanumeric_with_symbols'])
        characters['bottom_odd'] = list(CHARSETS['original.digits'])
        characters['bottom_even'] = list(CHARSETS['original.digits'])
    elif not symbols and digits:
        characters['top_odd'] = list(CHARSETS['original.alphanumeric'])
        characters['top_even'] = list(CHARSETS['original.alphanumeric'])
        characters['bottom_odd'] = list(CHARSETS['original.digits'])
        characters['bottom_even'] = list(CHARSETS['original.digits'])
    elif not symbols and not digits:
        characters['top_odd'] = list(CHARSETS['original.alphanumeric'])
        characters['top_even'] = list(CHARSETS['original.alphanumeric'])
        characters['bottom_odd'] = list(CHARSETS['original.alphanumeric'])
        characters['bottom_even'] = list(CHARSETS['original.alphanumeric'])
    else:
        raise Exception('Cannot choose charset for password card')
    return characters


def generate_card(seed, width=29, height=8, symbols=False, digits=False):
    characters = generate_character_sets(symbols, digits)
    seed = int('0x%s' % seed, 16)
    rng = javarandom.JavaRandom(seed)
    header = list(HEADERS['original'])
    rng.shuffle(header)
    contents = []
    midheight = 1 + height / 2
    for i in range(1, midheight):
        line = []
        for j in range(width):
            if j % 2 == 0:
                line.append(characters['top_even'][rng.next_int(len(characters['top_even']))])
            else:
                line.append(characters['top_odd'][rng.next_int(len(characters['top_odd']))])

        contents.append(('').join(line))

    for j in range(midheight, height + 1):
        line = []
        for j in range(width):
            if j % 2 == 0:
                line.append(characters['bottom_even'][rng.next_int(len(characters['bottom_even']))])
            else:
                line.append(characters['bottom_odd'][rng.next_int(len(characters['bottom_odd']))])

        contents.append(('').join(line))

    return (('').join(header), contents)