# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/SRMspinanalysis/_version.py
# Compiled at: 2018-05-09 19:34:23
__version_info__ = (0, 1, 0)
__version__ = ('.').join(map(str, __version_info__[:3]))
if len(__version_info__) == 4:
    __version__ += __version_info__[(-1)]