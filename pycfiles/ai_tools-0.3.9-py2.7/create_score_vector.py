# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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