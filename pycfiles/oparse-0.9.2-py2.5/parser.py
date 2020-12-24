# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/oparse/parser.py
# Compiled at: 2009-11-17 08:28:03
"""
parser.py

Created by Olli Wang (olliwang@ollix.com) on 2009-11-17.
Copyright (c) 2009 Ollix. All rights reserved.
"""

class OptionParser(object):
    """Simulates optparse.OptionParser for adding options in command classes.

    This class should only be used by classes which inherit from Command
    class. These command classes then can add options by instantiating this
    class as a class variable named `parser`, and use it to add group options
    as using optparse.OptionParser.

    For example:
    class SomeCommand(Command):
        parser = OptionParser()
        parser.add_option("-v", "--verbose", action="store_true",
                          default=False, help="run in verbose mode")
    """

    def __init__(self):
        self.__options = []

    def add_option(self, *args, **kw):
        self.__options.append((args, kw))

    def add_options_to_parser(self, parser):
        for (args, kw) in self.__options:
            parser.add_option(*args, **kw)

    def has_options(self):
        if self.__options:
            return True
        else:
            return False