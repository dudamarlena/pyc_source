# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/microcsound/helpers.py
# Compiled at: 2017-09-29 23:07:37
# Size of source mod 2**32: 2252 bytes
import re
from math import log, pow
from microcsound.constants import MIDDLE_C_HZ

def octaves(pitch):
    """return a value in log octaves of a pitch expressed as a decimal"""
    return log(pitch, 2)


def solfege2et(text, div):
    """ translate an traditional "abcdefg" plus accidentals notation
    into numerical form. "div" represents the division of the octave
    we are working with. """
    octav = int(round(div))
    tempered_fifth = round(octaves(1.5) * div)
    whole_step = 2 * tempered_fifth % div
    chromatic = 3 * whole_step - -1 * tempered_fifth % div
    half_chromatic = chromatic * 0.5
    syntonic = round(octaves(1.0125) * div)
    septimal = round(octaves(1.0158730158730158) * div)
    undecimal = round(octaves(1.03125) * div)
    tridecimal = round(octaves(1.0283203125) * div)
    pure_fifth = octaves(1.5) * div
    meancomma = pure_fifth - tempered_fifth
    notes = {'=':0, 
     'c':0, 
     'd':whole_step, 
     'e':whole_step * 2, 
     'f':-1 * tempered_fifth % div, 
     'g':tempered_fifth, 
     'a':tempered_fifth + whole_step, 
     'b':tempered_fifth + whole_step * 2, 
     '^':chromatic, 
     '_':-1 * chromatic, 
     '^/2':half_chromatic, 
     '_/2':-1 * half_chromatic, 
     '/':syntonic, 
     '\\':-1 * syntonic, 
     '>':septimal, 
     '<':-1 * septimal, 
     '!':undecimal, 
     '¡':-1 * undecimal, 
     '?':tridecimal, 
     '¿':-1 * tridecimal, 
     '*':meancomma, 
     "'":octav, 
     ',':-1 * octav}
    value_sum = 0
    for i in re.findall("\\^/2|_/2|[a-g',^_=/\\\\<>!?]|\\xc2\\xa1|\\xc2\\xbf|\\*", text):
        value_sum += notes[i]

    return int(value_sum)


def degree2hz(degree, div):
    """return a pitch in HZ from a numerical index
    and a division of the octave"""
    myhz = MIDDLE_C_HZ * pow(2, (degree + 0.0) / div)
    return '%1.5f' % myhz