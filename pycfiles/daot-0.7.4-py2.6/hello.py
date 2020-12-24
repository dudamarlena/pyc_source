# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\samples\hello.py
# Compiled at: 2011-10-18 23:43:28
from dao import word
from samplevars import x

def parse(grammar_element, text):
    x = Var()
    code = grammar_element(x) + x
    return eval([code, text])


def match(grammar_element, text):
    x = Var()
    code = grammar_element(x)
    return eval([code, text])


print parse(word, 'hello')
print match(word, 'hello')

def hello(x):
    return word('hello') + some(space) + word(x)


print parse(hello, 'hello world')
print match(hello, 'hello world')