# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rekog2json2mongo/__init__.py
# Compiled at: 2018-03-03 17:41:04
from .base import face2folder2mango
from .compare import face2compare

def main():
    flag = raw_input('Facial detect API (F) or Compare faces API (C), F/C ?')
    if flag.lower() == 'f':
        print 'starting Facial detect API'
        path = raw_input('path of folder that contains pictures: ')
        face2folder2mango(path)
    elif flag.lower() == 'c':
        print 'starting Compare faces API'
        print 'prepare a folder of images with a collection of somename.jpg, somename_cpr.jpg'
        path = raw_input('path of folder that contains pictures (name.jpg, name_cpr.jpg collections) to compare: ')
        face2compare(path)
    else:
        print 'invalid input'