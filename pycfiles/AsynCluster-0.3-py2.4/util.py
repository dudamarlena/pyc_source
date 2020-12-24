# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/asyncluster/util.py
# Compiled at: 2007-07-24 13:41:18
"""
Utility functions
"""
VERBOSE = True

def log(msg):
    """
    Logs to stdout, if in verbose mode.
    """
    if VERBOSE:
        msgProto = '\n%s\n%s\n'
        dashes = '-' * 40
        print msgProto % (dashes, msg)


def biggerFont(widget, scale):
    font = widget.font()
    font.setPointSizeF(scale * font.pointSizeF())
    widget.setFont(font)