# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/prettyprint/__init__.py
# Compiled at: 2012-02-23 13:28:59
r"""
   This module privides pretty printing for list/dict/tuple/set python object.

   Simple example of usage is followings

       >>> from prettyprint import pp
       >>> target = ['want pretty printing', '望麗出力']
       >>> print target
       ['want pretty printing', '\xe6\x9c\x9b\xe9\xba\x97\xe5\x87\xba\xe5\x8a\x9b']  # what a ugly print especially in japanese
       >>> pp(target)   # now we can see pretty print with pp
       [
           "want pretty printing", 
           "望麗出力"
       ]
       >>> target_dict = {'order': {'en':'pretty print', 'ja':'綺麗に出力せよ'}}
       >>> print target_dict  # what a hell again
       {'order': {'en': 'pretty print', 'ja': '\xe7\xb6\xba\xe9\xba\x97\xe3\x81\xab\xe5\x87\xba\xe5\x8a\x9b\xe3\x81\x9b\xe3\x82\x88'}}
       >>> pp(target_dict)  # pp again
       {
           "order": {
               "en": "print prettily", 
               "ja": "綺麗に出力せよ"
           }
       }
"""
__author__ = 'Matsumoto Taichi'
__version__ = '0.1.5'
__license__ = 'MIT License'
from prettyprint import *