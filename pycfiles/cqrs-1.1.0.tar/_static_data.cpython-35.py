# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\Programmer\PYTHON\cqrcode\static\_static_data.py
# Compiled at: 2020-04-07 07:38:51
# Size of source mod 2**32: 1672 bytes
import os
data32 = '4CJZ0maWgO6b1cotTMdjU8u3QprVkPRY'
data64 = 'XFSB1wQ2XPKBsVTYdChtz9Gyx4PuYokVvbGX7ai1FYmFHRs2SDIIz39KAiGxkfxL'
rawPath = os.path.abspath(__file__)
dataPath = rawPath[:rawPath.find('static')] + 'static\\'
alphanumeric_mode_table = {'0': 0, 
 '1': 1, 
 '2': 2, 
 '3': 3, 
 '4': 4, 
 '5': 5, 
 '6': 6, 
 '7': 7, 
 '8': 8, 
 '9': 9, 
 'A': 10, 
 'B': 11, 
 'C': 12, 
 'D': 13, 
 'E': 14, 
 'F': 15, 
 'G': 16, 
 'H': 17, 
 'I': 18, 
 'J': 19, 
 'K': 20, 
 'L': 21, 
 'M': 22, 
 'N': 23, 
 'O': 24, 
 'P': 25, 
 'Q': 26, 
 'R': 27, 
 'S': 28, 
 'T': 29, 
 'U': 30, 
 'V': 31, 
 'W': 32, 
 'X': 33, 
 'Y': 34, 
 'Z': 35, 
 ' ': 36, 
 '$': 37, 
 '%': 38, 
 '*': 39, 
 '+': 40, 
 '-': 41, 
 '.': 42, 
 '/': 43, 
 ':': 44}
number_of_bits_in_character_count = 11
version_bit_length = 4
height_length_table = {1: (5, 19), 
 2: (5, 29), 
 3: (7, 19), 
 4: (8, 18), 
 5: (8, 32), 
 6: (9, 29), 
 7: (9, 35), 
 8: (11, 35), 
 9: (12, 26), 
 10: (12, 36), 
 11: (13, 35)}
BOX = 16
BOUNDARY = 1
CAPACITY = [
 (1, 6), (2, 12), (3, 10), (4, 12), (5, 30), (6, 32), (7, 40),
 (8, 52), (9, 42), (10, 62), (11, 66)]