# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/pythonipsum/__init__.py
# Compiled at: 2013-03-30 00:22:37
__title__ = 'pythonipsum'
__version__ = '0.2'
__author__ = 'Mike Pirnat'
__license__ = 'GPLv3+'
__copyright__ = 'Copyright 2013 Mike Pirnat'
from .api import get_sentence, get_sentences
from .api import get_paragraph, get_paragraphs
from .api import dictionary, sample