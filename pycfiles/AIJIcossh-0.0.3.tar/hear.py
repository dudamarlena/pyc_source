# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiio/hear.py
# Compiled at: 2016-09-28 20:22:12
from pocketsphinx import LiveSpeech

def listen(cb):
    for phrase in LiveSpeech():
        p = str(phrase)
        print p
        p and cb(p)