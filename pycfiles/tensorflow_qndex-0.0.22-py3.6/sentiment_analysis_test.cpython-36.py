# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qndex/nlp/sentiment_analysis_test.py
# Compiled at: 2017-04-13 04:52:31
# Size of source mod 2**32: 133 bytes
import typing
from .sentiment_analysis import *

def test_def_read_file():
    assert isinstance(def_read_file(), typing.Callable)