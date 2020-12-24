# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/obpds/contact.py
# Compiled at: 2015-11-15 13:26:53
__all__ = [
 'Contact', 'OhmicContact', 'SchottkyContact']

class Contact(object):
    pass


class OhmicContact(Contact):
    pass


class SchottkyContact(Contact):
    """
    A Schottky contact that pins at the "universal pinning level",
    which is approximately 4.9 eV below the vacuum level.
    """

    def __init__(self, work_function=4.9):
        self.work_function = work_function