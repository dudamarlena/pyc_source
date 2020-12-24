# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/felipe/.virtualenvs/morselate/lib/python2.7/site-packages/morselate/morselate.py
# Compiled at: 2017-10-21 20:40:27
"""Morselate coders/decoders"""
from functools import reduce
from collections import defaultdict
MORSECODES = {'.-': 'A', 
   '-...': 'B', 
   '-.-.': 'C', 
   '-..': 'D', 
   '.': 'E', 
   '..-.': 'F', 
   '--.': 'G', 
   '....': 'H', 
   '..': 'I', 
   '.---': 'J', 
   '-.-': 'K', 
   '.-..': 'L', 
   '--': 'M', 
   '-.': 'N', 
   '---': 'O', 
   '.--.': 'P', 
   '--.-': 'Q', 
   '.-.': 'R', 
   '...': 'S', 
   '-': 'T', 
   '..-': 'U', 
   '...-': 'V', 
   '.--': 'W', 
   '-..-': 'X', 
   '-.--': 'Y', 
   '--..': 'Z', 
   '.-.-.-': '.', 
   '--..--': ',', 
   '..--..': '?', 
   '.----.': "'", 
   '-.-.--': '!', 
   '-..-.': '/', 
   '-.--.': '(', 
   '-.--.-': '(', 
   '.-...': '$', 
   '---...': ':', 
   '-.-.-.': ';', 
   '-...-': '=', 
   '-....-': '-', 
   '..--.-': '_', 
   '.-..-.': '"', 
   '...-..-': '$', 
   '.--.-.': '@', 
   '.----': '1', 
   '..---': '2', 
   '...--': '3', 
   '....-': '4', 
   '.....': '5', 
   '-....': '6', 
   '--...': '7', 
   '---..': '8', 
   '----.': '9', 
   '-----': '0', 
   '/': ' '}

def demorse(morse):
    """Decodes a morse code"""
    return reducer(morse, MORSECODES)


def emorse(text):
    """Encodes a text in morse code"""
    text = map(str, (' ').join(text).upper())
    inverted = {}
    for key in MORSECODES:
        inverted[MORSECODES[key]] = key

    return reducer(text, inverted, ' ')


def reducer(source, keydict, joiner=''):
    """Reduce a maped dict based on a source string"""
    return reduce(lambda x, y: x + defaultdict(lambda : ' ', keydict)[y] + joiner, source, '').strip()