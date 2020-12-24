# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/Ctrax/codedir.py
# Compiled at: 2016-05-28 20:43:25
import os
codedir = os.path.dirname(__file__)
while 'library.zip' in codedir:
    codedir, tail = os.path.split(codedir)

head, tail = os.path.split(codedir)
if tail == 'site-packages.zip':
    codedir = head