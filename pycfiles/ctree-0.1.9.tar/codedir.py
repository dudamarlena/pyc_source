# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/codedir.py
# Compiled at: 2016-05-28 20:43:25
import os
codedir = os.path.dirname(__file__)
while 'library.zip' in codedir:
    codedir, tail = os.path.split(codedir)

head, tail = os.path.split(codedir)
if tail == 'site-packages.zip':
    codedir = head