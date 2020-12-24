# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/xbuild/errors.py
# Compiled at: 2016-07-03 23:28:12
""" 
Defines the build setup errors.
"""

class XBuildError(StandardError):
    pass


class InvalidBuildPath(XBuildError):

    def __init__(self, buildpath):
        msg = ('{0} is not a valid build path').format(buildpath)
        XBuildError.__init__(self, msg)