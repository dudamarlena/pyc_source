# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bai/anaconda3/lib/python3.6/site-packages/segment/data_util.py
# Compiled at: 2017-06-26 22:44:07
# Size of source mod 2**32: 1111 bytes
"""
author: Leo
date: 2017-4-23
"""
from __future__ import unicode_literals
import codecs, sys
from sys import argv

def character_tagging(input_file, output_file):
    input_data = codecs.open(input_file, 'r', 'utf-8')
    output_data = codecs.open(output_file, 'w', 'utf-8')
    for line in input_data.readlines():
        word_list = line.strip().split()
        for word in word_list:
            words = word.split('/')
            word = words[0]
            if len(word) == 1:
                output_data.write(word + '\tS\n')
            else:
                if len(word) >= 2:
                    output_data.write(word[0] + '\tB\n')
                    for w in word[1:len(word) - 1]:
                        output_data.write(w + '\tM\n')

                    output_data.write(word[(len(word) - 1)] + '\tE\n')

        output_data.write('\n')

    input_data.close()
    output_data.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(argv[0])
        sys.exit(-1)
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    character_tagging(input_file, output_file)