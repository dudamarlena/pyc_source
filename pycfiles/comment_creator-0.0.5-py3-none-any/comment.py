# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/comment.py
# Compiled at: 2014-10-22 17:02:48
import sys

def print_comment(message, width, java=False, xml=False):
    """Prints the commentmessage."""
    if len(message) > width:
        sys.stderr.write('Warning: "%s": length is %d, wider than %d\n' % (message,
         len(message), width))
    filler_width = (width - len(message) - 2) / 2
    if java:
        filler = '*' * (filler_width - 1)
        filler_start = '/' + filler
        filler_end = filler + '/'
    elif xml:
        filler = ' ' * (filler_width - 3)
        filler_start = '<!--' + filler[:-1]
        filler_end = filler + '-->'
    else:
        filler_start = filler_end = '#' * max(1, filler_width)
    if len(message) % 2 == 1:
        filler_end = filler_end[0] + filler_end
    print filler_start + ' %s ' % message + filler_end