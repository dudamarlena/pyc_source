# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/prettyprint/__init__.py
# Compiled at: 2012-02-23 13:28:59
__doc__ = '\n   This module privides pretty printing for list/dict/tuple/set python object.\n\n   Simple example of usage is followings\n\n       >>> from prettyprint import pp\n       >>> target = [\'want pretty printing\', \'望麗出力\']\n       >>> print target\n       [\'want pretty printing\', \'\\xe6\\x9c\\x9b\\xe9\\xba\\x97\\xe5\\x87\\xba\\xe5\\x8a\\x9b\']  # what a ugly print especially in japanese\n       >>> pp(target)   # now we can see pretty print with pp\n       [\n           "want pretty printing", \n           "望麗出力"\n       ]\n       >>> target_dict = {\'order\': {\'en\':\'pretty print\', \'ja\':\'綺麗に出力せよ\'}}\n       >>> print target_dict  # what a hell again\n       {\'order\': {\'en\': \'pretty print\', \'ja\': \'\\xe7\\xb6\\xba\\xe9\\xba\\x97\\xe3\\x81\\xab\\xe5\\x87\\xba\\xe5\\x8a\\x9b\\xe3\\x81\\x9b\\xe3\\x82\\x88\'}}\n       >>> pp(target_dict)  # pp again\n       {\n           "order": {\n               "en": "print prettily", \n               "ja": "綺麗に出力せよ"\n           }\n       }\n'
__author__ = 'Matsumoto Taichi'
__version__ = '0.1.5'
__license__ = 'MIT License'
from prettyprint import *