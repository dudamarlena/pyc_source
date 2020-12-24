# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyhardware\drivers\multiple_choice.py
# Compiled at: 2013-10-09 11:09:05


class MultipleChoice(object):
    """
    a class to choose amongst multiple choices
    """

    def __init__(self, parent, attr_name, **kwds):
        for key, value in kwds.iteritems():
            setattr(self, key, value)

        self.choices = kwds