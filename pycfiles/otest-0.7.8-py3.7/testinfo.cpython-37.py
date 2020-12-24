# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/otest/aus/preproc/testinfo.py
# Compiled at: 2017-06-15 02:09:44
# Size of source mod 2**32: 752 bytes
from otest import summation
from otest.events import row

def do_assertions(out):
    return summation.condition(out, True)


def trace_output(events):
    """

    """
    element = [
     '<table class="table table-bordered table-condensed">']
    start = 0
    for event in events:
        if not start:
            start = event.timestamp
        element.append(row(start, event))

    element.append('</table>')
    return '\n'.join(element)


def profile_output(pinfo, version=''):
    element = [
     '<table class="table table-condensed">']
    for key, val in pinfo.items():
        element.append('<tr><th>%s</th><td>%s</td></tr>' % (key, val))

    element.append('</table>')
    return '\n'.join(element)