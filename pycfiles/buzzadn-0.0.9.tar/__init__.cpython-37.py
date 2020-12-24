# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/buzz/__init__.py
# Compiled at: 2020-05-05 18:08:11
# Size of source mod 2**32: 537 bytes
import warnings
from .corpus import Corpus
from .dataset import Dataset
from .file import File
from .parse import Parser
warnings.filterwarnings('ignore', message='numpy.dtype size changed')
warnings.filterwarnings('ignore', message='numpy.ufunc size changed')
warnings.filterwarnings('ignore', message='registration of accessor')
warnings.filterwarnings('ignore', message="Attribibute 'is_copy")
warnings.filterwarnings('ignore')
__version__ = '3.1.4'