# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/create_score_vector.py
# Compiled at: 2018-08-04 12:32:06
import os, random

def logw(fh, message):
    print message
    fh.write(message)


def create_score_vector(num):
    fh = open('score_vector.txt', 'w')
    for i in range(0, num):
        sample_type = -1
        if random.random() > 0.5:
            sample_type = 1
        score = random.random()
        logw(fh, '%d %f\n' % (sample_type, score))

    fh.close()


create_score_vector(100)