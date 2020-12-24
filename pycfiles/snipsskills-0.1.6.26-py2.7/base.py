# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskills/commands/base.py
# Compiled at: 2017-09-29 10:30:10
""" The base command. """

class Base(object):
    """ The base command. """

    def __init__(self, options, *args, **kwargs):
        """ Initialisation.

        :param options: command-line options.
        :param *args, **kwargs: extra arguments.
        """
        self.options = options
        self.args = args
        self.kwargs = kwargs
        self.snipsfile = None
        return

    def run(self):
        """ Command runner. """
        raise NotImplementedError('You must implement the run() method yourself!')