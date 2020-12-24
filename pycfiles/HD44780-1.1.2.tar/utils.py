# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mezgrman/projects/HD44780/hd44780/utils.py
# Compiled at: 2013-03-13 06:06:08


def bool_list_to_mask(list):
    mask = 0
    for i in range(len(list)):
        if bool(int(list[i])):
            mask += 2 ** i

    return mask


def nibble_to_mask(backend, nibble, data):
    l = [
     False] * 8
    l[backend.PIN_D4 - 1] = nibble[3]
    l[backend.PIN_D5 - 1] = nibble[2]
    l[backend.PIN_D6 - 1] = nibble[1]
    l[backend.PIN_D7 - 1] = nibble[0]
    if data:
        l[backend.PIN_RS - 1] = True
    mask = bool_list_to_mask(l)
    return mask


def value_to_nibbles(value):
    assert value >= 0
    assert value <= 255
    b = bin(value)[2:10]
    b = '0' * (8 - len(b)) + b
    bits = tuple([ bit == '1' for bit in list(b) ])
    nibbles = (bits[:4], bits[4:])
    return nibbles