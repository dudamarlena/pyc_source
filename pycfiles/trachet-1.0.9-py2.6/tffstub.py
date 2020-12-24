# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/trachet/tffstub.py
# Compiled at: 2014-07-01 10:29:06
import logging, sys
expected_hash = 'b87c36758a4c3d666c74490b383f483b'
try:
    import ctff as tff
    if not tff.signature == expected_hash:
        raise ImportError('Fail to validate signature hash of TFF library.')
except ImportError:
    e = sys.exc_info()[1]
    logging.exception(e)
    from tff import tff