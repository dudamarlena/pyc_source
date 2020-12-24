# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/lib/ascii2cyrillic.py
# Compiled at: 2011-12-23 04:19:50
"""
Created on Oct 11, 2010

@author: KMihajlov
"""
multiAsciiToCyrillic = {'zh': 'ж', 
   'dj': 'џ', 
   'sh': 'ш', 
   'gj': 'ѓ', 
   'lj': 'љ', 
   'kj': 'ќ', 
   'nj': 'њ', 
   'ch': 'ч', 
   'Zh': 'ж', 
   'DJ': 'Џ', 
   'SH': 'Ш', 
   'Gj': 'Ѓ', 
   'Lj': 'Љ', 
   'Kj': 'Ќ', 
   'Nj': 'Њ', 
   'Ch': 'Ч'}
asciiToCyrillic = {'A': 'A', 
   'B': 'B', 
   'C': 'Ц', 
   'D': 'Д', 
   'E': 'E', 
   'F': 'Ф', 
   'G': 'G', 
   'H': 'Х', 
   'I': 'И', 
   'J': 'J', 
   'K': 'К', 
   'L': 'Л', 
   'M': 'М', 
   'N': 'Н', 
   'O': 'О', 
   'P': 'П', 
   'Q': 'Љ', 
   'R': 'Р', 
   'S': 'С', 
   'T': 'Т', 
   'U': 'У', 
   'V': 'В', 
   'W': 'Њ', 
   'X': 'Џ', 
   'Y': 'Ѕ', 
   'Z': 'З', 
   '[': 'ш', 
   '\\': 'ж', 
   ']': 'ѓ', 
   '^': '‘', 
   'a': 'а', 
   'b': 'б', 
   'c': 'ц', 
   'd': 'д', 
   'e': 'е', 
   'f': 'ф', 
   'g': 'г', 
   'h': 'х', 
   'i': 'и', 
   'j': 'ј', 
   'k': 'к', 
   'l': 'л', 
   'm': 'м', 
   'n': 'н', 
   'o': 'о', 
   'p': 'п', 
   'q': 'љ', 
   'r': 'р', 
   's': 'с', 
   't': 'т', 
   'u': 'у', 
   'v': 'в', 
   'w': 'њ', 
   'x': 'џ', 
   'y': 'ѕ', 
   'z': 'з', 
   '{': 'Ш', 
   '|': 'Ж', 
   '}': 'Ѓ'}

def replaceWithCyrillic(text):
    for k, v in multiAsciiToCyrillic.iteritems():
        text = val.replace(k, v)

    for k, v in asciiToCyrillic.iteritems():
        text = text.replace(k, v)

    return text