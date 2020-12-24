# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/utils/test_importer.py
# Compiled at: 2017-03-22 15:30:24
# Size of source mod 2**32: 237 bytes
from baroque.utils import importer

class Placeholder:
    pass


def test_class_from_dotted_path():
    path = 'tests.utils.test_importer.Placeholder'
    result = importer.class_from_dotted_path(path)
    assert result == Placeholder