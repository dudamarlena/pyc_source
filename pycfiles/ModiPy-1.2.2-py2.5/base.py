# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modipy/base.py
# Compiled at: 2009-08-25 18:19:45
"""
Some base level classes and definitions.
"""

class XMLConfigurable:
    """
    Something that is XML configurable, i.e.: pretty much
    all the classes in the system, has some common functions
    and attributes that we define here.
    """
    required_tags = []
    optional_tags = []

    def get_required_tags(self):
        return self.required_tags

    def get_optional_tags(self):
        return self.optional_tags

    def get_supported_tags(self):
        return self.required_tags + self.optional_tags