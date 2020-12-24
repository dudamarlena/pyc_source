# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kejser/Projects/Pygrametl/Respository/docs/_exts/rtdmockup.py
# Compiled at: 2018-12-08 09:11:17
# Size of source mod 2**32: 2081 bytes
"""Simple mock-up of the external dependencies so documentation can be
   created without requiring the installation of Java and Jython.

   The code used is made publicly available by www.readthedocs.org, under the
   MIT license. For more information see the following links:
   https://github.com/rtfd/readthedocs.org
   https://read-the-docs.readthedocs.org/en/latest/index.html
"""
import sys

class Mock(object):

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        if name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        return Mock()


def mockModules(modules):
    for mod_name in modules:
        sys.modules[mod_name] = Mock()