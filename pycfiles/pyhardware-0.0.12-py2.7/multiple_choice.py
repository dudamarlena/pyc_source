# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhardware\drivers\multiple_choice.py
# Compiled at: 2013-10-05 04:00:20


class MultipleChoice(object):
    """
    a class to choose amongst multiple choices
    """

    def __init__(self, parent, attr_name, **kwds):
        for key, value in kwds.iteritems():
            setattr(self, key, value)

        self.choices = kwds