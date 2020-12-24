# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/canossa/stub.py
# Compiled at: 2014-04-25 02:25:24
import logging
expected_hash = 'b87c36758a4c3d666c74490b383f483b'
try:
    import ctff as tff
    if not tff.signature == expected_hash:
        raise ImportError('Fail to validate signature hash of TFF library.')
except ImportError, e:
    logging.exception(e)
    from tff import tff