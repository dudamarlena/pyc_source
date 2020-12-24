# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/jupyter.py
# Compiled at: 2018-03-17 09:15:05
from IPython.display import Image

def showpic(ID, w=6, picpath=''):
    """
    display a picture (jpg) in jupyter notebook
    set picture path `picpath`, picture name should ends with numbers
    w ~ width, picpath ~ the folder path contains images
    
    """
    return Image(picpath + ('/{}.jpg').format(ID), width=w * 100)