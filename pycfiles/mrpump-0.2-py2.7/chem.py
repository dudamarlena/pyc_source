# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv5tel/egg/mrpump/chem.py
# Compiled at: 2012-05-05 17:28:32


class Chem(object):

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'unnamed')

    def appliesTo(self, text):
        return False

    def __call__(self, sender_screen_name, text, reply):
        pass

    def __repr__(self):
        return '<Chem %s>' % self.name